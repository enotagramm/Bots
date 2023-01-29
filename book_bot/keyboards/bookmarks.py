from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from book_bot.lexicon.lexicon_ru import LEXICON
from book_bot.services.file_handling import book


def create_bookmarks_keyboard(*args: int) -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    bookmarks_kb: InlineKeyboardMarkup = InlineKeyboardMarkup()
    # Наполняем клавиатуру кнопками-закладками по возрастанию
    for button in sorted(args):
        bookmarks_kb.add(InlineKeyboardButton(text=f'{button} - {book[button][:100]}',
                                              callback_data=str(button)))
    # Добавляем в клавиатуру в конец две кнопки, редактировать и отменить
    bookmarks_kb.add(InlineKeyboardButton(text=LEXICON['edit_bookmarks_button'],
                                          callback_data='edit_bookmarks'),
                     InlineKeyboardButton(text=LEXICON['cancel'],
                                          callback_data='cancel'))
    return bookmarks_kb


def create_edit_keyboard(*args: int) -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    bookmarks_kb: InlineKeyboardMarkup = InlineKeyboardMarkup()
    # Наполняем клавиатуру кнопками-закладками по возрастанию
    for button in sorted(args):
        bookmarks_kb.add(InlineKeyboardButton(text=f'{LEXICON["del"]} {button} - {book[button][:100]}',
                                              callback_data=str(button) + 'del'))
    # Добавляем в конец кнопку отменить
    bookmarks_kb.add(InlineKeyboardButton(text=LEXICON['cancel'],
                                          callback_data='cancel'))
    return bookmarks_kb
