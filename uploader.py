
from instagrapi import Client
import os, time

def upload_reels(username, password, video_folder):
    cl = Client()
    cl.login(username, password)

    videos = sorted([v for v in os.listdir(video_folder) if v.endswith(".mp4")])
    count = 0
    for video in videos:
        if count >= 100:
            break
        try:
            cl.clip_upload(os.path.join(video_folder, video), caption="Ч/Б Reels by Цветочки 🌸")
            time.sleep(60)  # пауза 1 минута между загрузками
            count += 1
        except Exception as e:
            print(f"Ошибка с {video}: {e}")
