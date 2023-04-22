# from config import set_city


async def norilsk(update, context):
    """Позволяет выбрать Норильск текущим городом. Командой /norilsk"""
    await update.message.reply_text("Норильск выбран основным городом.")
