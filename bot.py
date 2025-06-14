
from aiogram import Bot, Dispatcher, types, executor
import json, os
from uploader import upload_reels

with open("config.json") as f:
    config = json.load(f)

bot = Bot(token=config["bot_token"])
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.answer("Цветочки 🌸 запустились! Заливаю Reels...")

    upload_reels(
        username=config["inst_username"],
        password=config["inst_password"],
        video_folder=config["video_folder"]
    )
    await msg.answer("Готово! 100 видео начали загружаться.")

if __name__ == "__main__":
    executor.start_polling(dp)
