import logging
from telegram.ext import Application, MessageHandler, filters
from config import TOKEN
from telegram.ext import CommandHandler
from Start import start
from Help import help_command
from wherethebus import wherethebus
from telegram import ReplyKeyboardMarkup


# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("wherethebus", wherethebus))

    application.run_polling()


if __name__ == '__main__':
    main()
