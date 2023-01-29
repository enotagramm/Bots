import asyncio
import logging

from aiogram import Dispatcher, Bot

from config_data.config import load_config, Config
from handlers.user_handlers import register_user_handlers
from handlers.other_handlers import register_other_handlers
from keyboards.main_menu import set_main_menu


# Инициализируем logger
logger = logging.getLogger(__name__)


# Функция для регистрации всех хэндлеров
def register_all_handlers(dp: Dispatcher) -> None:
    register_user_handlers(dp)
    register_other_handlers(dp)


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s'
    )

    # Выводим в консоль о начале запуска бота
    logger.info('Starting bot!')

    # Загружаем конфиг в переменную config
    config: Config = load_config(None)

    # Инициализируем bot и Dispatcher
    bot: Bot = Bot(token=config.bot.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher(bot)

    # Регистрируем все хэндлеры
    register_all_handlers(dp)

    # Регистрируем меню
    await set_main_menu(dp)

    # Запускаем пуллинг
    try:
        await dp.start_polling()
    finally:
        await bot.close()


if __name__ == '__main__':
    try:
        # Запускаем функцию main
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        # Выводим в консоль сообщение об ошибке
        logger.error('Bot stopped!')
