from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher.filters import Text

from cuefa_bot.lexicon.lexicon_ru import LEXICON_RU
from cuefa_bot.keyboards.keyboards import yes_no_kb, game_kb
from cuefa_bot.services.services import get_bot_choice, get_winner


# Этот хэндлер срабатывает на команду /start
async def process_start_handler(message: Message):
    await message.answer(text=LEXICON_RU['/start'], reply_markup=yes_no_kb)


# Этот хэндлер срабатывает на команду /help
async def process_help_handler(message: Message):
    await message.answer(text=LEXICON_RU['/help'], reply_markup=yes_no_kb)


# Этот хэндлер срабатывает на согласие пользователя играть в игру
async def process_yes_answer(message: Message):
    await message.answer(text=LEXICON_RU['yes'], reply_markup=game_kb)


# Этот хэндлер срабатывает на отказ пользователя играть в игру
async def process_no_answer(message: Message):
    await message.answer(text=LEXICON_RU['no'])


# Этот хэндлер срабатывает на любую из игровых кнопок
async def process_game_button(message: Message):
    bot_choice = get_bot_choice()
    await message.answer(text=f'{LEXICON_RU["bot_choice"]} - {LEXICON_RU[bot_choice]}')
    winner = get_winner(message.text, bot_choice)
    await message.answer(text=LEXICON_RU[winner], reply_markup=yes_no_kb)


# Функция для регистрации хэндлеров в диспетчере. Вызывается в исполняемом файле bot.py
def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(process_start_handler, commands='start')
    dp.register_message_handler(process_help_handler, commands='help')
    dp.register_message_handler(process_yes_answer, text=LEXICON_RU['yes_button'])
    dp.register_message_handler(process_no_answer, text=LEXICON_RU['no_button'])
    dp.register_message_handler(process_game_button, Text(equals=[
        LEXICON_RU['rock'],
        LEXICON_RU['paper'],
        LEXICON_RU['scissors']
    ]))
