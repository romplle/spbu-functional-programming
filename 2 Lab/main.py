import re
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
import tkinter as tk
from tkinter import scrolledtext

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import vk_api
import praw

from my_token import VK_TOKEN, REDDIT_APP_ID, REDDIT_APP_SECRET

# import nltk
# nltk.download('stopwords')
# nltk.download('punkt_tab')
stop_words = set(stopwords.words('russian'))

# VK access
token = VK_TOKEN
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()

# Reddit access
reddit = praw.Reddit(
    client_id=REDDIT_APP_ID,
    client_secret=REDDIT_APP_SECRET,
    user_agent='Functional programming lab 2'
)

def fetch_vk_posts(group_id, count=100):
    try:
        posts = vk.wall.get(owner_id=-group_id, count=count)
        return [post['text'] for post in posts['items'] if 'text' in post]
    except Exception as e:
        print(f"Error fetching vk posts: {e}")
        return []

def fetch_reddit_posts(subreddit_name, count=100):
    try:
        subreddit = reddit.subreddit(subreddit_name)
        posts = subreddit.hot(limit=count)
        return [post.selftext for post in posts]
    except Exception as e:
        print(f"Error fetching reddit posts: {e}")
        return []

def preprocess_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    tokens = word_tokenize(text.lower())
    return " ".join([t for t in tokens if t not in stop_words])

def analyze_texts(texts):
    words_counter = Counter()
    for text in texts:
        words = text.split()
        words_counter.update(words)
    return words_counter.most_common(5)

def run_analysis():
    vk_ids = [int(id.strip()) for id in vk_input.get("1.0", tk.END).splitlines() if id.strip()]
    reddit_subreddits = [sub.strip() for sub in reddit_input.get("1.0", tk.END).splitlines() if sub.strip()]

    with ThreadPoolExecutor(max_workers=None) as executor:
        vk_posts = list(executor.map(fetch_vk_posts, vk_ids))
        reddit_posts = list(executor.map(fetch_reddit_posts, reddit_subreddits))

        vk_processed_texts = [preprocess_text(post) for posts in vk_posts for post in posts]
        reddit_processed_texts = [preprocess_text(post) for posts in reddit_posts for post in posts]

        vk_words = analyze_texts(vk_processed_texts)
        reddit_words = analyze_texts(reddit_processed_texts)

        display_results(vk_output, vk_words)
        display_results(reddit_output, reddit_words)

def display_results(output_widget, words):
    output_widget.configure(state='normal')
    output_widget.delete("1.0", tk.END)
    output_widget.insert(tk.END, "Топ 5 слов:\n")
    for word, count in words:
        output_widget.insert(tk.END, f"{word}: {count}\n")
    output_widget.configure(state='disabled')

root = tk.Tk()
root.title("Анализ популярных тем в ВК и Reddit")

tk.Label(root, text="Введите ID групп ВК:").grid(row=0, column=0)
vk_input = scrolledtext.ScrolledText(root, width=30, height=10)
vk_input.grid(row=1, column=0)

tk.Label(root, text="Введите субреддиты Reddit:").grid(row=0, column=1)
reddit_input = scrolledtext.ScrolledText(root, width=30, height=10)
reddit_input.grid(row=1, column=1)

analyze_button = tk.Button(root, text="Запустить анализ", command=run_analysis)
analyze_button.grid(row=2, column=0, columnspan=2)

tk.Label(root, text="Результаты для ВК:").grid(row=3, column=0)
vk_output = scrolledtext.ScrolledText(root, width=30, height=10, state='disabled')
vk_output.grid(row=4, column=0)

tk.Label(root, text="Результаты для Reddit:").grid(row=3, column=1)
reddit_output = scrolledtext.ScrolledText(root, width=30, height=10, state='disabled')
reddit_output.grid(row=4, column=1)

root.mainloop()