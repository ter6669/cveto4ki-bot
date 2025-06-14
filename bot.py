import os
from aiogram import Bot, Dispatcher, types, executor
from uploader import upload_reels

config = {
    "bot_token": os.getenv("BOT_TOKEN"),
    "inst_username": os.getenv("INST_USERNAME"),
    "inst_password": os.getenv("INST_PASSWORD"),
    "video_folder": os.getenv("VIDEO_FOLDER", "videos/")
}

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
