import os
import tempfile
from PIL import Image, ImageOps
from moviepy.editor import ImageSequenceClip, AudioFileClip
import random
from instagrapi import Client

def make_bw_frames_and_save(image_folder, size=(720, 720)):
    files = [os.path.join(image_folder, f) for f in os.listdir(image_folder)
             if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    temp_dir = tempfile.mkdtemp()
    saved_files = []
    for i, f in enumerate(sorted(files)):
        img = Image.open(f)
        img = ImageOps.grayscale(img)
        img = img.resize(size, Image.ANTIALIAS)
        save_path = os.path.join(temp_dir, f"frame_{i}.png")
        img.save(save_path)
        saved_files.append(save_path)
    return saved_files

def pick_random_music(music_folder):
    music_files = [os.path.join(music_folder, f) for f in os.listdir(music_folder)
                   if f.lower().endswith(".mp3")]
    if not music_files:
        raise Exception("Нет музыки в папке music!")
    return random.choice(music_files)

def create_video(image_folder, music_folder, output_path="output.mp4"):
    frames = make_bw_frames_and_save(image_folder)
    audio_path = pick_random_music(music_folder)
    
    clip = ImageSequenceClip(frames, fps=1)  # 1 кадр в секунду, можно менять
    audio = AudioFileClip(audio_path).subclip(0, min(clip.duration, 10))  # максимум 10 секунд
    
    clip = clip.set_audio(audio)
    clip.write_videofile(output_path, codec="libx264", audio_codec="aac", verbose=False, logger=None)
    
    return output_path

def upload_reels(username, password, video_folder, music_folder):
    video_path = create_video(video_folder, music_folder)
    print(f"Видео готово: {video_path}")

    cl = Client()
    cl.login(username, password)
    print("Вход в Instagram выполнен")

    cl.clip_upload(video_path, caption="Это сгенерировано ИИ #авто #техно #цветочки")
    print("Видео загружено в Instagram")
