import os
import moviepy.editor as mp
from PIL import Image, ImageOps
from instagrapi import Client
import uuid
import urllib.request

def make_black_white_photos(photo_paths, temp_folder):
    bw_paths = []
    for i, path in enumerate(photo_paths):
        img = Image.open(path)
        bw = ImageOps.grayscale(img)
        output_path = os.path.join(temp_folder, f"bw_{i}.jpg")
        bw.save(output_path)
        bw_paths.append(output_path)
    return bw_paths

def download_techno_music(output_path):
    url = "https://filesamples.com/samples/audio/mp3/sample3.mp3"
    urllib.request.urlretrieve(url, output_path)

def create_video(photo_paths, audio_path, output_video_path):
    clips = [mp.ImageClip(p).set_duration(1.5) for p in photo_paths]
    video = mp.concatenate_videoclips(clips, method="compose")
    audio = mp.AudioFileClip(audio_path)
    video = video.set_audio(audio)
    video.write_videofile(output_video_path, fps=24)

def upload_reels(username, password, photo_paths, video_folder):
    temp_folder = os.path.join(video_folder, "temp")
    os.makedirs(temp_folder, exist_ok=True)
