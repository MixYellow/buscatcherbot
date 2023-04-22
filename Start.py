async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Здравствуйте, {user.mention_html()}! Я BusCATcherbot, ваш карманный помощник в перемещении на общественном транспорте. Из какого вы города?No",
    )
