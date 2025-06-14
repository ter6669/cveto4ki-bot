import os
import random
from PIL import Image, ImageOps
from moviepy.editor import ImageSequenceClip, AudioFileClip
from instagrapi import Client


def make_bw_frames_and_save(image_folder: str):
    frames = []
    output_dir = "frames"
    os.makedirs(output_dir, exist_ok=True)

    files = [f for f in os.listdir(image_folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    if not files:
        print("❌ Нет изображений в папке.")
        return []

    for i, file in enumerate(sorted(files)):
        img_path = os.path.join(image_folder, file)
        img = Image.open(img_path).convert("L")  # Чёрно-белое
        img = ImageOps.fit(img, (720, 1280))     # Пропорции под Reels
        frame_path = os.path.join(output_dir, f"frame_{i}.jpg")
        img.save(frame_path)
        frames.append(frame_path)

    return frames


def create_video(image_folder: str, music_folder: str):
    frames = make_bw_frames_and_save(image_folder)
    if not frames:
        raise ValueError("❌ Не удалось создать кадры. Проверь папку с фото.")

    clip = ImageSequenceClip(frames, fps=1.5)

    music_files = [f for f in os.listdir(music_folder) if f.endswith((".mp3", ".wav"))]
    if not music_files:
        raise ValueError("❌ В папке 'music' нет музыки.")

    music_file = os.path.join(music_folder, random.choice(music_files))
    audio = AudioFileClip(music_file).subclip(0, clip.duration)
    final = clip.set_audio(audio)

    os.makedirs("ready", exist_ok=True)
    out_path = os.path.join("ready", "final.mp4")
    final.write_videofile(out_path, codec="libx264", audio_codec="aac")
    return out_path


def upload_reels(username: str, password: str, video_folder: str, music_folder: str):
    print("📦 Создаём видео...")
    video_path = create_video(video_folder, music_folder)

    print("🔐 Логинимся в Instagram...")
    cl = Client()
    cl.login(username, password)

    print("📤 Загружаем Reels...")
    cl.clip_upload(video_path, caption="Это сгенерировал ИИ 🤖")
    print("✅ Reels загружен!")
