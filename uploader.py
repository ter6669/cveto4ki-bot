import os
from moviepy.editor import ImageSequenceClip, AudioFileClip, vfx

def create_video_with_music(images_folder, music_folder, output_path):
    # Берём изображения из папки
    image_files = sorted([os.path.join(images_folder, f) for f in os.listdir(images_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    if not image_files:
        raise Exception("В папке videos нет фотографий!")

    # Создаём видео из фото с fps=2 (примерно 5 секунд на 10 фото)
    clip = ImageSequenceClip(image_files, fps=2)

    # Делаем видео чёрно-белым
    clip = clip.fx(vfx.blackwhite)

    # Берём первый mp3 из папки music
    music_files = [os.path.join(music_folder, f) for f in os.listdir(music_folder) if f.lower().endswith('.mp3')]
    if not music_files:
        raise Exception("В папке music нет mp3 файлов!")

    audio = AudioFileClip(music_files[0]).subclip(0, clip.duration)

    # Добавляем аудио к видео
    final_clip = clip.set_audio(audio)

    # Сохраняем видео
    final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

def upload_reels(username, password, video_folder):
    output_video = "output_video.mp4"
    create_video_with_music(video_folder, "music", output_video)

    # Здесь добавить логику загрузки видео в Instagram, например:
    # from instagrapi import Client
    # cl = Client()
    # cl.login(username, password)
    # cl.video_upload(output_video, caption="Автоматический Reels от Цветочки 🌸")
