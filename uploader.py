import os
from PIL import Image, ImageOps
from moviepy.editor import ImageSequenceClip, AudioFileClip
from instagrapi import Client
import random

def make_bw_frames_and_save(image_folder, output_size=(720, 1280)):
    output_folder = os.path.join(image_folder, "frames")
    os.makedirs(output_folder, exist_ok=True)

    frames = []
    for filename in sorted(os.listdir(image_folder)):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(image_folder, filename)
            img = Image.open(img_path)

            img = ImageOps.fit(img, output_size, method=Image.Resampling.LANCZOS)
            img = ImageOps.grayscale(img)

            frame_path = os.path.join(output_folder, filename)
            img.save(frame_path)
            frames.append(frame_path)

    return frames

def create_video(image_folder, music_folder, output_file="output.mp4"):
    frames = make_bw_frames_and_save(image_folder)
    clip = ImageSequenceClip(frames, fps=1.5)

    music_files = [f for f in os.listdir(music_folder) if f.endswith('.mp3')]
    if not music_files:
        raise Exception("Нет музыкальных файлов в папке music")
    music_path = os.path.join(music_folder, random.choice(music_files))

    audio = AudioFileClip(music_path).subclip(0, clip.duration)
    final = clip.set_audio(audio)

    final.write_videofile(output_file, codec="libx264", audio_codec="aac")
    return output_file

def upload_reels(username, password, video_folder, music_folder):
    video_path = create_video(video_folder, music_folder)

    cl = Client()
    cl.login(username, password)
    cl.clip_upload(video_path, caption="Это сгенерировал ИИ 🤖")
