from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

# ===============================Start_keyboard======================
start_builder = InlineKeyboardBuilder()
start_button1 = InlineKeyboardButton(
    text="👀" + "Помощь",
    callback_data="help"
)
start_button2 = InlineKeyboardButton(
    text="🍩" + "Донат",
    callback_data="donate"
)
start_button3 = InlineKeyboardButton(
    text="🚌Список всех остановок",
    callback_data="list"
)
start_builder.row(start_button1, start_button2)
start_builder.row(start_button3)
# ===================================================================

# ===========================List_keyboard=============================
list_builder = InlineKeyboardBuilder()
list_button1 = InlineKeyboardButton(
    text="⬅️" + 'Назад',
    callback_data='minus'
)
list_button2 = InlineKeyboardButton(
    text='Вперёд' + "➡️",
    callback_data='plus'
)
list_button3 = InlineKeyboardButton(
    text='🆗' + 'Меню',
    callback_data='back'
)
list_builder.row(list_button1, list_button2)
list_builder.row(list_button3)

# ====================================================================