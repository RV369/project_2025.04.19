import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, executor, types

from utils.config_reader import config
from utils.core import read_file_excel
from utils.db_map import Repozitory, Zuzubliks

UPLOAD_FOLDER = 'documents/'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)

bot = Bot(token=config.bot_token.get_secret_value())


dp = Dispatcher(bot)


async def data_zuzublik(document: dict) -> dict:
    file_id = document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    filename = document.file_name
    destination = os.path.join(UPLOAD_FOLDER, filename)
    await bot.download_file(file_path, destination)
    zuzublik = await read_file_excel(destination)
    await Repozitory.get_or_create(Zuzubliks, **zuzublik)
    return zuzublik


@dp.message_handler(commands=['start'])
async def send_file(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(keyboard=[['/start']])
    file = open('documents/Лист Microsoft Excel.xlsx', 'rb')
    answer = await read_file_excel(file)
    await Repozitory.get_or_create(Zuzubliks, **answer)
    await message.reply_document(file, reply_markup=keyboard)
    await message.reply(
        f'title {answer["title"]} url {answer["url"]} '
        f'xpath {answer["xpath"]}',
    )


@dp.message_handler(content_types=['document'])
async def get_docs(message: types.Message):
    answer = await data_zuzublik(message.document)
    await message.reply(
        f'title {answer["title"]} url {answer["url"]} '
        f'xpath {answer["xpath"]}',
    )


async def main():
    await Repozitory.create_tables()


asyncio.run(main())
executor.start_polling(dp)
