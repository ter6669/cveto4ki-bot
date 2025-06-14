from aiogram import Bot, Dispatcher, types, executor
import json
from uploader import upload_reels

with open("config.json") as f:
    config = json.load(f)

bot = Bot(token=config["bot_token"])
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.answer("Цветочки 🌸 запустились! Заливаю Reels...")

    try:
        upload_reels(
            username=config["inst_username"],
            password=config["inst_password"],
            video_folder="videos"
        )
        await msg.answer("Готово! Видео загружены.")
    except Exception as e:
        await msg.answer(f"Ошибка: {e}")

if __name__ == "__main__":
    executor.start_polling(dp)
