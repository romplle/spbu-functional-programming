import asyncio
import os
import threading
import tkinter as tk
from tkinter import scrolledtext, filedialog

asyncio_event_loop = None
reader = None
writer = None
user_name = None
active_room = None
chat_server_address = '127.0.0.1'
chat_server_port = 20000


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    position_top = int(screen_height / 2 - height / 2)
    position_left = int(screen_width / 2 - width / 2)

    window.geometry(f'{width}x{height}+{position_left}+{position_top}')


async def send_message(writer, message):
    writer.write((message + '\n').encode())
    await writer.drain()


async def send_file(writer, file_path):
    file_header = f"FILE:{os.path.basename(file_path)}\n"
    writer.write(file_header.encode())
    await writer.drain()

    file_size = os.path.getsize(file_path)
    writer.write(f"{file_size}\n".encode())
    await writer.drain()

    with open(file_path, 'rb') as file:
        while chunk := file.read(1024):
            writer.write(chunk)
            await writer.drain()

    completion_message = f"Finished sending file: {os.path.basename(file_path)}\n"
    writer.write(completion_message.encode())
    await writer.drain()


async def receive_messages(reader, chat_display_widget):
    while True:
        data = await reader.read(100)
        if not data:
            break

        message = data.decode().strip()
        print(f"Received message: {message}")
        chat_display_widget.insert(tk.END, f"{message}\n")
        chat_display_widget.see(tk.END)


async def register_client(chat_server_address, user_name, room_name):
    global reader, writer, active_room

    if writer:
        writer.close()
        await writer.wait_closed()

    reader, writer = await asyncio.open_connection(chat_server_address, chat_server_port)

    writer.write(f"{user_name}\n".encode())
    await writer.drain()

    writer.write(f"{room_name}\n".encode())
    await writer.drain()

    active_room = room_name
    print(f"Client {user_name} registered in room: {room_name}")

    asyncio.create_task(receive_messages(reader, chat_display_widget))


async def disconnect_client():
    global writer
    if writer:
        writer.close()
        await writer.wait_closed()
        root.destroy()


def start_chat(chat_server_address, user_name, room_name):
    asyncio.run_coroutine_threadsafe(register_client(chat_server_address, user_name, room_name), asyncio_event_loop)
    root.deiconify()


def start_client():
    global asyncio_event_loop
    asyncio_event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(asyncio_event_loop)
    asyncio_event_loop.run_forever()


def open_registration_dialog():
    registration_dialog = tk.Toplevel(root)
    registration_dialog.title("Connect to Chat Server")

    form_frame = tk.Frame(registration_dialog, padx=10, pady=10)
    form_frame.pack(padx=10, pady=10)

    tk.Label(form_frame, text="Username:").grid(row=0, column=0, sticky="w", pady=5)
    username_entry = tk.Entry(form_frame)
    username_entry.grid(row=0, column=1)

    tk.Label(form_frame, text="Room Name:").grid(row=1, column=0, sticky="w", pady=5)
    room_entry = tk.Entry(form_frame)
    room_entry.grid(row=1, column=1)

    def on_confirm():
        global user_name
        user_name = username_entry.get()
        room_name = room_entry.get()

        if user_name and room_name:
            start_chat(chat_server_address, user_name, room_name)
            registration_dialog.destroy()

    connect_button = tk.Button(form_frame, text="Connect", command=on_confirm)
    connect_button.grid(row=3, columnspan=2, pady=(10, 0))


def clear_placeholder(event):
    if message_entry_widget.get() == "Enter your message...":
        message_entry_widget.delete(0, "end")
        message_entry_widget.config(fg="black")


def restore_placeholder(event):
    if message_entry_widget.get() == "":
        message_entry_widget.insert(0, "Enter your message...")
        message_entry_widget.config(fg="grey")


def on_send_button_click():
    message = message_entry_widget.get()
    message_entry_widget.delete(0, tk.END)
    if message:
        asyncio.run_coroutine_threadsafe(send_message(writer, message), asyncio_event_loop)


def on_send_file_button_click():
    file_path = filedialog.askopenfilename()
    if file_path:
        asyncio.run_coroutine_threadsafe(send_file(writer, file_path), asyncio_event_loop)


root = tk.Tk()
root.geometry("800x450")
root.title("Chat Client")
center_window(root, 800, 450)
root.withdraw()

main_frame = tk.Frame(root)
main_frame.pack(padx=10, pady=10)

chat_frame = tk.LabelFrame(main_frame, text="Chat Messages", padx=10, pady=10)
chat_frame.pack(fill="both", expand=True)

chat_display_widget = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, height=20, bg="#ffffff", fg="black")
chat_display_widget.pack(fill="both", expand=True)

input_frame = tk.Frame(main_frame)
input_frame.pack(padx=5)

message_entry_widget = tk.Entry(input_frame, width=110)
message_entry_widget.pack(side="left", fill="x", expand=True)
message_entry_widget.insert(0, "Enter your message...")
message_entry_widget.config(fg="grey")

message_entry_widget.bind("<FocusIn>", clear_placeholder)
message_entry_widget.bind("<FocusOut>", restore_placeholder)
message_entry_widget.bind("<Return>", lambda event: on_send_button_click())

send_button = tk.Button(input_frame, text="Send", command=on_send_button_click)
send_button.pack(side="right", padx=(5, 0))

send_file_button = tk.Button(input_frame, text="Send File", command=lambda: on_send_file_button_click())
send_file_button.pack(side="right", padx=(5, 0))

client_thread = threading.Thread(target=start_client, daemon=True)
client_thread.start()

open_registration_dialog()

root.protocol("WM_DELETE_WINDOW", lambda: asyncio.run_coroutine_threadsafe(disconnect_client(), asyncio_event_loop))
root.mainloop()
