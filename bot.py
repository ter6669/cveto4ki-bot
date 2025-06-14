from aiogram import Bot, Dispatcher, types, executor
import json, os, random
from PIL import Image, ImageOps
from moviepy.editor import ImageSequenceClip, AudioFileClip
from instagrapi import Client

with open("config.json") as f:
    config = json.load(f)

bot = Bot(token=config["bot_token"])
dp = Dispatcher(bot)

VIDEO_FOLDER = config.get("video_folder", "video")
MUSIC_FOLDER = config.get("music_folder", "music")

def make_bw_frames(image_folder, size=(720, 720)):
    files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    bw_frames = []
    for f in sorted(files):
        img = Image.open(f)
        img = ImageOps.grayscale(img)
        img = img.resize(size)  # изменяем размер
        bw_frames.append(img)
    return bw_frames

def create_video(frames, audio_path, output_path="output.mp4"):
    clip = ImageSequenceClip([frame for frame in frames], fps=1)
    audio = AudioFileClip(audio_path).subclip(0, min(clip.duration, 10))
    clip = clip.set_audio(audio)
    clip.write_videofile(output_path, codec="libx264", audio_codec="aac", verbose=False, logger=None)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Цветочки 🌸 запускаю процесс создания Reels...")
    try:
        frames = make_bw_frames(VIDEO_FOLDER)
        if not frames:
            await message.answer("В папке видео нет подходящих фото!")
            return
        music_files = [os.path.join(MUSIC_FOLDER, f) for f in os.listdir(MUSIC_FOLDER) if f.lower().endswith((".mp3", ".wav"))]
        if not music_files:
            await message.answer("В папке музыка нет аудиофайлов!")
            return
        audio_path = random.choice(music_files)

        video_path = "output.mp4"
        create_video(frames, audio_path, video_path)

        cl = Client()
        cl.login(config["inst_username"], config["inst_password"])
        cl.video_upload(video_path, caption="Сделано ботом Цветочки 🌸")
        await message.answer("Видео успешно загружено на Instagram!")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

if __name__ == "__main__":
    executor.start_polling(dp)
