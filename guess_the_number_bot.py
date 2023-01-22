from random import randint

from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
from aiogram.dispatcher.filters import Text

from token import *


API_TOKEN: str = API_TOKEN_GUESS_BOT
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher(bot)

user = {
    'game': False,
    'secret_number': 0,
    'attempts': 0,
    'total_games': 0,
    'wins': 0,
}

my_dict = {1: 'попытка'}


def get_random_number():
    return randint(1, 100)


#   Количество попыток доступное пользователю в игре
ATTEMPTS: int = 5


async def process_start_command(message: Message):
    await message.answer('Привет!\n'
                         'Давай сыграем в игру "Угадай число"?\n\n'
                         'Чтобы получить правила игры и список доступных команд - отправьте команду /help')


async def process_help_command(message: Message):
    await message.answer(f'Правила игры:\n\n'
                         f'Я загадываю число от 1 до 100, а вам нужно его угадать\n'
                         f'У вас есть {ATTEMPTS} попыток\n\n'
                         f'Доступные команды:\n'
                         f'/help - правила игры и список команд\n'
                         f'/cancel - выйти из игры\n'
                         f'/stat - посмотреть статистику\n\n'
                         f'Давай сыграем?')


async def process_stat_command(message: Message):
    await message.answer(f'Всего игр сыграно: {user["total_games"]}\nИгр выиграно: {user["wins"]}')


async def process_cancel_command(message: Message):
    if user['game']:
        await message.answer('Вы вышли из игры. Если захотите сыграть снова - напишите об этом')
        user['game'] = False
    else:
        await message.answer('А мы итак с вами не играем. Может, сыграем разок')


async def process_positive_answer(message: Message):
    if not user['game']:
        await message.answer('Ура!\n\n Я загадал число от 1 до 100.\n У тебя 5 попыток, чтобы отгадать!')
        user['game'] = True
        user['secret_number'] = get_random_number()
        user['attempts'] = ATTEMPTS
    else:
        await message.answer('Пока мы играем в игру я могу реагировать только на числа от 1 до 100 и команды /cancel и /stat')


async def process_negative_answer(message: Message):
    if not user['game']:
        await message.answer('Больно и хотелось')
    else:
        await message.answer('Ты лучше числа загадывай!')


async def process_number_answer(message: Message):
    if user['game']:
        limit = f'У тебя осталось {user["attempts"] - 1} {my_dict.get(user["attempts"] - 1, "попытки")}'
        if int(message.text) == user['secret_number']:
            user['game'] = False
            user['total_games'] += 1
            user['wins'] += 1
            await message.answer('Ура!!! Вы угадали число!\n\nМожет, сыграем еще?')
        elif int(message.text) < user['secret_number']:
            user['attempts'] -= 1
            await message.answer('Моё число больше... ' + limit)
        elif int(message.text) > user['secret_number']:
            user['attempts'] -= 1
            await message.answer('Моё число меньше... ' + limit)

        if user['attempts'] == 0:
            user['game'] = False
            user['total_games'] += 1
            await message.answer(f'К сожалению, у вас больше не осталось попыток. Вы проиграли :(\n\n'
                                 f'Мое число было {user["secret_number"]}\n\n'
                                 f'Давайте сыграем еще?')
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')


async def process_other_text_answer(message: Message):
    if user['game']:
        await message.answer('Мы же сейчас с вами играем. Присылайте, пожалуйста, числа от 1 до 100')
    else:
        await message.answer('Я довольно ограниченный бот, давайте просто сыграем в игру?')


lst_positive = ['Да', 'Давай', 'Сыграем', 'Игра', 'Играть', 'Хочу играть', 'Хочу']
lst_negative = ['Нет', 'Не', 'Не хочу']

dp.register_message_handler(process_start_command, commands='start')
dp.register_message_handler(process_help_command, commands='help')
dp.register_message_handler(process_stat_command, commands='stat')
dp.register_message_handler(process_cancel_command, commands='cancel')
dp.register_message_handler(process_positive_answer, Text(equals=lst_positive, ignore_case=True))
dp.register_message_handler(process_negative_answer, Text(equals=lst_negative, ignore_case=True))
dp.register_message_handler(process_number_answer, lambda x: x.text.isdigit() and 1 <= int(x.text) <= 100)
dp.register_message_handler(process_other_text_answer)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
