from aiogram import Bot, Dispatcher, executor, types

from pprint import pprint

from token_bot import *


API_TOKEN: str = API_TOKEN_ECHO_BOT

bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher(bot)


# @dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer(
        '''Привет! 
Меня зовут эхо-бот! 
Напиши мне что-нибудь!''')


# @dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.answer('Напиши мне что-нибудь и в ответ я пришлю тебе твоё сообщение!')


async def send_photo_echo(message: types.Message):
    await message.answer_photo(message.photo[0].file_id)


async def send_sticker_echo(message: types.Message):
    pprint(message.to_python())
    await message.answer_sticker(message.sticker.file_id)


# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения, кроме команд "/start" и "/help"
# @dp.message_handler()
async def send_echo(message: types.Message):
    await message.reply(message.text)


dp.register_message_handler(process_start_command, commands='start')
dp.register_message_handler(process_help_command, commands='help')
dp.register_message_handler(send_photo_echo, content_types=['photo'])
dp.register_message_handler(send_sticker_echo, content_types=['sticker'])
dp.register_message_handler(send_echo)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
