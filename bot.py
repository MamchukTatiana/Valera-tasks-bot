import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

tasks = []

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    if message.from_user.id != OWNER_ID:
        return
    await message.reply("Привет! Я твой Валера Task Bot!")

@dp.message_handler(commands=["add"])
async def add_task(message: types.Message):
    if message.from_user.id != OWNER_ID:
        return
    task = message.get_args()
    if task:
        tasks.append(task)
        await message.reply(f"Задача добавлена: {task}")
    else:
        await message.reply("Пожалуйста, укажи задачу после команды /add")

@dp.message_handler(commands=["list"])
async def list_tasks(message: types.Message):
    if message.from_user.id != OWNER_ID:
        return
    if not tasks:
        await message.reply("Список задач пуст.")
    else:
        reply = "\n".join([f"{i+1}. {t}" for i, t in enumerate(tasks)])
        await message.reply(reply)

@dp.message_handler(commands=["clear"])
async def clear_tasks(message: types.Message):
    if message.from_user.id != OWNER_ID:
        return
    tasks.clear()
    await message.reply("Список задач очищен.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
