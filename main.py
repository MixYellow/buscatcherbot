import asyncio
import logging
from aiogram import Dispatcher
import Start
import wherethebus
from config import bot

# Запуск процесса поллинга новых апдейтов
async def main():
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO)
    # Объект бота
    # Диспетчер
    dp = Dispatcher()

    dp.include_router(Start.router)
    dp.include_router(wherethebus.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())