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


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['/upload_a_file']
    keyboard.add(*buttons)
    await message.reply('Загрузить файл>>', reply_markup=keyboard)


@dp.message_handler(commands=['upload_a_file'])
async def send_file(message: types.Message):
    file = open('documents/Лист Microsoft Excel.xlsx', 'rb')
    kwargs = await read_file_excel(file)
    await Repozitory.get_or_create(Zuzubliks, **kwargs)
    await message.reply_document(file)
    await message.reply(
        f'title {kwargs["title"]} url {kwargs["url"]} '
        f'xpath {kwargs["xpath"]}',
    )


@dp.message_handler(content_types=['document'])
async def get_docs(message: types.Message):
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    filename = message.document.file_name
    destination = os.path.join(UPLOAD_FOLDER, filename)
    await bot.download_file(file_path, destination)
    kwargs = await read_file_excel(destination)
    await Repozitory.get_or_create(Zuzubliks, **kwargs)
    await message.reply(
        f'title {kwargs["title"]} url {kwargs["url"]} '
        f'xpath {kwargs["xpath"]}',
    )


async def main():
    await Repozitory.create_tables()


asyncio.run(main())
executor.start_polling(dp)
