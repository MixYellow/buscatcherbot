from aiogram import Router
from config import bot
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from random import randint
import json
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
from keyboards import start_builder, list_builder, help_builder, donate_builder
from messages import *

router = Router()


# ========================Создаём многоcтраничное, цикличное меню через колбеки============================================

@router.message(Command("start"))
async def start(message: Message):
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    try:
        with open("Users_settings.json", 'r+', encoding='utf-8') as f:
            dic = json.load(f)
            if str(message.from_user.id) not in dic:
                dic[message.from_user.id] = ['Норильск', [], 10, 'Free',
                                             'No']  # Город, Часто запрашиваемые остановки, Страница в листе всех остановок, Тариф, Дата конца тарифа
        with open('Users_settings.json', 'w', encoding='utf-8') as f:
            json.dump(dic, f, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        return message.answer('⁉️Что-то пошло не так, код ошибки: 5. Сообщите администрации об этом.')
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=FSInputFile(f'img/main_cat{randint(1, 7)}.jpg'),
        caption=start_message,
        reply_markup=start_builder.as_markup()
    )


@router.callback_query(Text("help"))
async def help_callback(callback: CallbackQuery):
    await bot.edit_message_caption(
        caption=help_message,
        parse_mode='HTML',
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=help_builder.as_markup(),
    )


@router.callback_query(Text("donate"))
async def donate_callback(callback: CallbackQuery):
    await bot.edit_message_caption(
        caption="Доната пока что нет😊",
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=donate_builder.as_markup()
    )


@router.callback_query(Text("back"))
async def start_callback(callback: CallbackQuery):
    await bot.edit_message_caption(
        caption=start_message,
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=start_builder.as_markup()
    )


@router.callback_query(Text("list"))
async def show_list_of_station(callback: CallbackQuery):
    with suppress(TelegramBadRequest):
        try:
            with open('Users_settings.json', 'r', encoding='utf-8') as f:
                users_dic = json.load(f)
        except FileNotFoundError:
            return callback.message.answer(
                '⁉️Что-то пошло не так, код ошибки: 5. Сообщите администрации об этом.'
            )
        try:
            with open('Norilsk_numbers_of_route.json', 'r', encoding='utf-8') as f:
                dic = list(json.load(f))
        except FileNotFoundError:
            return callback.message.answer(
                '⁉️Что-то пошло не так, код ошибки: 4. Сообщите администрации об этом.'
            )
        try:
            lst_message = f'В городе {users_dic[str(callback.from_user.id)][0]} мне известно' \
                          f' об этих остановках (нажмите чтобы скопировать):\n---------------------------\n'
            num_of_page = users_dic[str(callback.from_user.id)][2]
            if num_of_page < 10:
                num_of_page = 10
            for num in range(num_of_page - 10, num_of_page):
                if num > 0 and num < len(dic):
                    lst_message += '🚏' + f"`{dic[num]}`\n---------------------------\n"
        except KeyError:
            return callback.answer(
                '⁉️Что-то пошло не так, пожалуйста, откройте главное меню командой /start и попробуйте ещё раз.\n'
                ' Если ничего не изменится - сообщите администрации. Код ошибки: 6.'
            )
        await bot.edit_message_caption(
            caption=lst_message,
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=list_builder.as_markup(),
            parse_mode='Markdown'
        )


@router.callback_query(Text("minus"))
async def show_list_of_station(callback: CallbackQuery):
    with suppress(TelegramBadRequest):
        try:
            with open('Users_settings.json', 'r', encoding='utf-8') as f:
                users_dic = json.load(f)
                if users_dic[str(callback.from_user.id)][2] - 10 >= 10:
                    users_dic[str(callback.from_user.id)][2] -= 10
            with open('Users_settings.json', 'w', encoding='utf-8') as f:
                json.dump(users_dic, f, ensure_ascii=False, indent=4)
        except FileNotFoundError:
            return callback.message.answer(
                '⁉️Что-то пошло не так, код ошибки: 5. Сообщите администрации об этом.'
            )
        try:
            with open('Norilsk_numbers_of_route.json', 'r', encoding='utf-8') as f:
                dic = list(json.load(f))
        except FileNotFoundError:
            return callback.message.answer(
                '⁉️Что-то пошло не так, код ошибки: 4. Сообщите администрации об этом.'
            )
        try:
            lst_message = f'В городе {users_dic[str(callback.from_user.id)][0]} мне известно' \
                          f' об этих остановках (нажмите чтобы скопировать):\n---------------------------\n'
            num_of_page = users_dic[str(callback.from_user.id)][2]
            if num_of_page < 10:
                num_of_page = 10
            for num in range(num_of_page - 10, num_of_page):
                if num > 0 and num < len(dic):
                    lst_message += '🚏' + f"`{dic[num]}`\n---------------------------\n"
        except KeyError:
            return callback.answer(
                '⁉️Что-то пошло не так, пожалуйста, откройте главное меню командой /start и попробуйте ещё раз.\n'
                ' Если ничего не изменится - сообщите администрации. Код ошибки: 6.'
            )
        await bot.edit_message_caption(
            caption=lst_message,
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=list_builder.as_markup(),
            parse_mode='Markdown'
        )


@router.callback_query(Text("plus"))
async def show_list_of_station(callback: CallbackQuery):
    with suppress(TelegramBadRequest):
        try:
            with open('Norilsk_numbers_of_route.json', 'r', encoding='utf-8') as f:
                dic = list(json.load(f))
        except FileNotFoundError:
            return callback.message.answer(
                '⁉️Что-то пошло не так, код ошибки: 4. Сообщите администрации об этом.'
            )
        try:
            with open('Users_settings.json', 'r', encoding='utf-8') as f:
                users_dic = json.load(f)
                if users_dic[str(callback.from_user.id)][2] + 10 - len(dic) <= 10:
                    users_dic[str(callback.from_user.id)][2] += 10
            with open('Users_settings.json', 'w', encoding='utf-8') as f:
                json.dump(users_dic, f, ensure_ascii=False, indent=4)
        except FileNotFoundError:
            return callback.message.answer(
                '⁉️Что-то пошло не так, код ошибки: 5. Сообщите администрации об этом.'
            )
        try:
            lst_message = f'В городе {users_dic[str(callback.from_user.id)][0]} мне известно' \
                          f' об этих остановках (нажмите чтобы скопировать):\n---------------------------\n'
            num_of_page = users_dic[str(callback.from_user.id)][2]
            if num_of_page < 10:
                num_of_page = 10
            for num in range(num_of_page - 10, num_of_page):
                if num > 0 and num < len(dic):
                    lst_message += '🚏' + f"`{dic[num]}`\n---------------------------\n"
        except KeyError:
            return callback.answer(
                '⁉️Что-то пошло не так, пожалуйста, откройте главное меню командой /start и попробуйте ещё раз.\n'
                ' Если ничего не изменится - сообщите администрации. Код ошибки: 6.'
            )
        await bot.edit_message_caption(
            caption=lst_message,
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=list_builder.as_markup(),
            parse_mode='Markdown'
        )
