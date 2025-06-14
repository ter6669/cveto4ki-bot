import os
from moviepy.editor import ImageSequenceClip, AudioFileClip, CompositeAudioClip
from instagrapi import Client
from PIL import Image, ImageOps
import random
import urllib.request

def download_techno_music(dest_path="techno.mp3"):
    # Пример скачивания бесплатной музыки с URL (замени на рабочий URL)
    url = "https://files.freemusicarchive.org/storage-freemusicarchive-org/music/no_curator/Scott_Holmes/Corporate__Motivational_Music/Scott_Holmes_-_Techno_Workout.mp3"
    urllib.request.urlretrieve(url, dest_path)

def create_bw_images(folder):
    files = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(('.jpg','.jpeg','.png'))]
    bw_folder = os.path.join(folder, "bw")
    if not os.path.exists(bw_folder):
        os.makedirs(bw_folder)
    bw_files = []
    for f in files:
        img = Image.open(f).convert("L")  # ч/б
        bw_path = os.path.join(bw_folder, os.path.basename(f))
        img.save(bw_path)
        bw_files.append(bw_path)
    return bw_files

def create_video_from_images(images, output_path="output.mp4", fps=1):
    clip = ImageSequenceClip(images, fps=fps)
    # Скачиваем музыку
    music_path = "techno.mp3"
    if not os.path.exists(music_path):
        download_techno_music(music_path)
    audio_clip = AudioFileClip(music_path).subclip(0, len(images)*5)
    clip = clip.set_audio(audio_clip)
    clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    return output_path

def upload_reels(username, password, video_folder):
    cl = Client()
    cl.login(username, password)
    bw_images = create_bw_images(video_folder)
    video_path = create_video_from_images(bw_images, "reels.mp4")
    cl.video_upload(video_path, "Авто-бот загружает Reels с техно и ч/б фото")
    os.remove(video_path)
    # Очистка ч/б папки
    bw_folder = os.path.join(video_folder, "bw")
    if os.path.exists(bw_folder):
        for f in os.listdir(bw_folder):
            os.remove(os.path.join(bw_folder, f))
