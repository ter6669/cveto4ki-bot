import os
from aiogram import Bot, Dispatcher, types, executor
from uploader import upload_reels

bot_token = os.getenv("BOT_TOKEN")
inst_username = os.getenv("INST_USERNAME")
inst_password = os.getenv("INST_PASSWORD")
video_folder = "/app/videos"

bot = Bot(token=bot_token)
dp = Dispatcher(bot)

photos = []

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.answer("Привет! Отправляй фото, а я сделаю из них Reels.")

@dp.message_handler(commands=["makevideo"])
async def makevideo(msg: types.Message):
    if not photos:
        await msg.answer("Нет фото для видео!")
        return
    await msg.answer("Начинаю создавать видео и загружать в Instagram...")
    upload_reels(inst_username, inst_password, photos, video_folder)
    await msg.answer("Видео создано и загружено!")

@dp.message_handler(content_types=["photo"])
async def handle_photo(msg: types.Message):
    photo = msg.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    file_path = file_info.file_path
    file = await bot.download_file(file_path)
    if not os.path.exists(video_folder):
        os.makedirs(video_folder)
    photo_path = os.path.join(video_folder, f"{photo.file_id}.jpg")
    with open(photo_path, "wb") as f:
        f.write(await file.read())
    photos.append(photo_path)
    await msg.answer("Фото сохранено!")

if __name__ == "__main__":
    executor.start_polling(dp)
