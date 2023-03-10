from copy import deepcopy

from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery

from book_bot.lexicon.lexicon_ru import LEXICON
from book_bot.database.database import users_bd, user_dict_template
from book_bot.services.file_handling import book
from book_bot.keyboards.pagination_kb import create_pagination_keyboard
from book_bot.keyboards.bookmarks import create_edit_keyboard, create_bookmarks_keyboard


# Этот хэндлер будет срабатывать на команду "/start" -
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
async def process_start_command(message: Message):
    await message.answer(text=LEXICON[message.text])
    if message.from_user.id not in users_bd:
        users_bd[message.from_user.id] = deepcopy(user_dict_template)


# Этот хэндлер будет срабатывать на команду "/help"
# и отправлять пользователю сообщение со списком доступных команд в боте
async def process_help_command(message: Message):
    await message.answer(text=LEXICON[message.text])


# Этот хэндлер будет срабатывать на команду "/beginning"
# и отправлять пользователю первую страницу книги с кнопками пагинации
async def process_beginning_command(message: Message):
    users_bd[message.from_user.id]['page'] = 1
    text = book[users_bd[message.from_user.id]['page']]
    await message.answer(
            text=text,
            reply_markup=create_pagination_keyboard(
                    'backward',
                    f'{users_bd[message.from_user.id]["page"]}/{len(book)}',
                    'forward'))


# Этот хэндлер будет срабатывать на команду "continue"
# и отправлять пользователю страницу книги, на которой пользователь
# остановился в процессе взаимодействия с ботом
async def process_continue_command(message: Message):
    text = book[users_bd[message.from_user.id]['page']]
    await message.answer(text=text,
                         reply_markup=create_pagination_keyboard(
                             'backward',
                             f'{users_bd[message.from_user.id]["page"]}/{len(book)}',
                             'forward'))


# Этот хэндлер будет срабатывать на команду "/bookmarks"
# и отправлять пользователю список сохраненных закладок,
# если они есть или сообщение о том, что закладок нет
async def process_bookmarks_command(message: Message):
    if users_bd[message.from_user.id]['bookmarks']:
        await message.answer(text=LEXICON[message.text],
                             reply_markup=create_bookmarks_keyboard(
                                 *users_bd[message.from_user.id]['bookmarks']))
    else:
        await message.answer(text=LEXICON['no_bookmarks'])


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "вперед"
# во время взаимодействия пользователя с сообщением-книгой
async def process_forward_press(callback: CallbackQuery):
    if users_bd[callback.from_user.id]['page'] < len(book):
        users_bd[callback.from_user.id]['page'] += 1
        text = book[users_bd[callback.from_user.id]['page']]
        await callback.message.edit_text(text=text,
                                         reply_markup=create_pagination_keyboard(
                                             'backward',
                                             f'{users_bd[callback.from_user.id]["page"]}/{len(book)}',
                                             'forward'))
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "назад"
# во время взаимодействия пользователя с сообщением-книгой
async def process_backward_press(callback: CallbackQuery):
    if users_bd[callback.from_user.id]['page'] > 1:
        users_bd[callback.from_user.id]['page'] -= 1
        text = book[users_bd[callback.from_user.id]['page']]
        await callback.message.edit_text(text=text,
                                         reply_markup=create_pagination_keyboard(
                                             'backward',
                                             f'{users_bd[callback.from_user.id]["page"]}/{len(book)}',
                                             'forward'))
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с номером текущей страницы и добавлять текущую страницу в закладки
async def process_page_press(callback: CallbackQuery):
    users_bd[callback.from_user.id]['bookmarks'].add(
        users_bd[callback.from_user.id]['page']
    )
    await callback.answer('Страница добавлена в закладки!')


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с закладкой из списка закладок
async def process_bookmark_press(callback: CallbackQuery):
    text = book[int(callback.data)]
    users_bd[callback.from_user.id]['page'] = int(callback.data)
    await callback.message.edit_text(text=text,
                                     reply_markup=create_pagination_keyboard(
                                         'backward',
                                         f'{users_bd[callback.from_user.id]["page"]}/{len(book)}',
                                         'forward'))
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "редактировать" под списком закладок
async def process_edit_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON[callback.data],
                                     reply_markup=create_edit_keyboard(
                                         *users_bd[callback.from_user.id]['bookmarks']
                                     ))
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "отменить" во время работы со списком закладок (просмотр и редактирование)
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['cancel_text'])
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с закладкой из списка закладок к удалению
async def process_del_bookmark_press(callback: CallbackQuery):
    users_bd[callback.from_user.id]['bookmarks'].remove(int(callback.data[:-3]))
    if users_bd[callback.from_user.id]['bookmarks']:
        await callback.message.edit_text(text=LEXICON['/bookmarks'],
                                         reply_markup=create_edit_keyboard(
                                             *users_bd[callback.from_user.id]['bookmarks']
                                         ))
    else:
        await callback.message.edit_text(text=LEXICON['no_bookmarks'])
    await callback.answer()


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(process_start_command, commands=['start'])
    dp.register_message_handler(process_help_command, commands=['help'])
    dp.register_message_handler(process_beginning_command, commands=['beginning'])
    dp.register_message_handler(process_bookmarks_command, commands=['bookmarks'])
    dp.register_message_handler(process_continue_command, commands=['continue'])
    dp.register_callback_query_handler(process_forward_press, text='forward')
    dp.register_callback_query_handler(process_backward_press, text='backward')
    dp.register_callback_query_handler(process_page_press,
                                       lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
    dp.register_callback_query_handler(process_bookmark_press, lambda x: x.data.isdigit())
    dp.register_callback_query_handler(process_edit_press, text='edit_bookmarks')
    dp.register_callback_query_handler(process_cancel_press, text='cancel')
    dp.register_callback_query_handler(process_del_bookmark_press,
                                       lambda x: 'del' in x.data and x.data[:-3].isdigit())
