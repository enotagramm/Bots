from pprint import pprint


BOOK_PATH = '/Users/enotagramm/PycharmProjects/Bots/book_bot/book/book.txt'
PAGE_SIZE = 1050

book: dict[int, str] = {}


# Функция возвращает строку с тексом страницы и её размер
def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    while 1:
        text_result = text[start:][:size]
        if text_result.split()[-1] not in text.split() or text_result[-1] not in '.,!?;:':
            size -= 1
        else:
            break
    return text_result, len(text_result)


# Фунция формирующая словарь книги
def prepare_book(path: str) -> None:
    with open(path, 'r', encoding='utf-8') as f:
        book_read = f.read()
        key: int = 1
        indx_letter: int = 0
        while 1:
            page, length_string = _get_part_text(book_read, indx_letter, PAGE_SIZE)
            book[key] = page.lstrip()
            key += 1
            if indx_letter + length_string < len(book_read):
                indx_letter += length_string
            else:
                break


# Вызов функции prepare_book для подготовки книги из текстового файла
prepare_book(BOOK_PATH)
