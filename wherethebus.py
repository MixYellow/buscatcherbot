from telegram import ReplyKeyboardMarkup

async def wherethebus(update, context):
    """основная функция бота. Позволяет показывать какие автобусы и как скоро придут на вашу остановку"""
    await update.message.reply_text("Для какой остановки вас интересует расписание?")


