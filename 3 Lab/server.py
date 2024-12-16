import asyncio

room_clients = {}
clients_lock = asyncio.Lock()
room_chat_histories = {}


async def handle_client(reader, writer):
    client_address = writer.get_extra_info('peername')
    print(f"New connection: {client_address}")

    try:
        user_name = (await reader.readline()).decode().strip()
        room_name = (await reader.readline()).decode().strip()

        await disconnect_user_from_previous_room(user_name)

        if room_name not in room_clients:
            room_clients[room_name] = []
        room_clients[room_name].append((user_name, writer))
        print(f"Client {user_name} {client_address} joined the room {room_name}")

        await send_chat_history_to_client(writer, room_name)

        while True:
            data = await reader.readline()
            if not data:
                break

            client_message = data.decode().strip()

            if client_message.startswith("FILE:"):
                await handle_file_transfer(reader, client_message[5:], user_name, room_name)
            else:
                print(f"{user_name} ({client_address}) in room {room_name}: {client_message}")
                await send_message_to_room(room_name, f"{user_name}: {client_message}")

    except Exception as e:
        print(f"Client error {user_name}: {e}")

    finally:
        async with clients_lock:
            if room_name in room_clients:
                room_clients[room_name] = [client for client in room_clients[room_name] if client[1] != writer]
                if not room_clients[room_name]:
                    del room_clients[room_name]

        print(f"Client {user_name} {client_address} left the room {room_name}")
        writer.close()
        await writer.wait_closed()


async def disconnect_user_from_previous_room(user_name):
    for room_name in list(room_clients.keys()):
        for client in room_clients[room_name]:
            if client[0] == user_name:
                room_clients[room_name].remove(client)

                await send_message_to_room(room_name, f"{user_name} has left the room.")

                if not room_clients[room_name]:
                    del room_clients[room_name]
                return


async def handle_file_transfer(reader, file_name, user_name, room_name):
    await send_message_to_room(room_name, f"{user_name} is sending a file: {file_name}")

    size_data = await reader.readline()

    try:
        file_size = int(size_data.decode().strip())
    except ValueError:
        print(f"Invalid file size received from {user_name}.")
        return

    with open(file_name, 'wb') as file:
        bytes_received = 0
        while bytes_received < file_size:
            chunk = await reader.read(1024)
            if not chunk:
                break
            file.write(chunk)
            bytes_received += len(chunk)

    await send_message_to_room(room_name, f"File received: {file_name}")


async def send_chat_history_to_client(writer, room_name):
    if room_name in room_chat_histories:
        for message in room_chat_histories[room_name]:
            writer.write(f"{message}\n".encode())
            await writer.drain()


async def send_message_to_room(room_name, message):
    if room_name in room_clients:
        if room_name not in room_chat_histories:
            room_chat_histories[room_name] = []
        room_chat_histories[room_name].append(message)

        for _, writer in room_clients[room_name]:
            writer.write(f"{message}\n".encode())
            await writer.drain()


async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 20000)
    server_address = server.sockets[0].getsockname()
    print(f"Server works on {server_address}")
    async with server:
        await server.serve_forever()


asyncio.run(main())
