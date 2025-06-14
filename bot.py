from aiogram import Bot, Dispatcher, types, executor
import json
from uploader import upload_reels
import asyncio

with open("config.json") as f:
    config = json.load(f)

bot = Bot(token=config["bot_token"])
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.answer("Цветочки 🌸 запустились! Заливаю Reels...")

    # Запускаем в отдельном потоке, чтобы не блокировать бота
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, upload_reels,
                               config["inst_username"],
                               config["inst_password"],
                               config["video_folder"],
                               config["music_folder"])

    await msg.answer("Готово! Видео созданы и залиты (если реализовано).")

if __name__ == "__main__":
    executor.start_polling(dp)
