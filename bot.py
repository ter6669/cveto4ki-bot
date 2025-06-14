import os
import asyncio
from aiogram import Bot, Dispatcher, types, executor
from uploader import upload_reels
import json

with open("config.json") as f:
    config = json.load(f)

bot = Bot(token=config["bot_token"])
dp = Dispatcher(bot)

PHOTO_DIR = config["video_folder"]

if not os.path.exists(PHOTO_DIR):
    os.makedirs(PHOTO_DIR)

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.answer("Привет! Отправляй фото, а я сделаю из них Reels.")

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def photo_handler(msg: types.Message):
    photo = msg.photo[-1]
    file_name = f"{PHOTO_DIR}/{photo.file_id}.jpg"
    await photo.download(destination_file=file_name)
    await msg.answer(f"Фото сохранено ({len(os.listdir(PHOTO_DIR))} шт.)")
    if len(os.listdir(PHOTO_DIR)) >= 5:
        await msg.answer("Начинаю создавать Reels из фото...")
        await asyncio.to_thread(upload_reels,
                               username=config["inst_username"],
                               password=config["inst_password"],
                               video_folder=PHOTO_DIR)
        await msg.answer("Reels загружены! Папка очищается.")
        for f in os.listdir(PHOTO_DIR):
            os.remove(os.path.join(PHOTO_DIR, f))

if __name__ == "__main__":
    executor.start_polling(dp)
