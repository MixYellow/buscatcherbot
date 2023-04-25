from aiogram import Router
from aiogram.types import Message
from datetime import datetime
import json
from config import bot

router = Router()


@router.message()
async def wherethebus(message: Message):
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    '''Приводим запрос пользователя к нужному нам формату.'''
    name_of_station = message.text.capitalize().replace('"', '').replace('«', '').replace('»', '')
    '''Собираем данные'''
    time_now = datetime.now().strftime('%H:%M:%S')
    day_today = datetime.today().weekday()
    output_text = f'К остановке {message.text} скоро подойдут маршруты:\n'
    try:
        with open('Norilsk_numbers_of_route.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            if name_of_station in data:
                routes = data[name_of_station]
            else:
                return message.answer(
                    f'Станции {name_of_station} нет в нашей базе данных.🛄 Убедитесь что она написана правильно,'
                    f' в частности в том, что пробелы вокруг символа № стоят с двух сторон.🔃'
                )
    except FileNotFoundError:
        return message.answer(
            '⁉️Что-то пошло не так, код ошибки: 1. Сообщите администрации об этом.'
        )
    try:
        with open('Norilsk_routes.json', 'r') as f:
            data = json.load(f)
            if day_today == 6 or day_today == 5:
                today = 'Weekend'
            else:
                today = 'Weekday'
            '''Обрабатываем данные'''
            for route in routes:
                try:
                    time_lst = data[today][route][name_of_station]
                except KeyError:
                    continue
                except Exception as error:
                    return message.answer(
                        '⁉️Что-то пошло не так, код ошибки: 3. Сообщите администрации об этом.'
                    )
                flag_new_day = False
                for i, time_without_mod in enumerate(time_lst):
                    h, m, s = time_without_mod.split(':')
                    if len(h) == 1: h = '0' + h
                    if len(m) == 1: m = '0' + m
                    if len(s) == 1: s = '0' + s
                    time = ':'.join([h, m, s])
                    if i != 0:
                        if time < time_lst[i - 1]:
                            flag_new_day = True
                    if time_now >= time is True and flag_new_day is True:
                        if i + 1 == len(time_lst):
                            j = 0
                        else:
                            j = i + 1
                        output_text += f'\n🚍{route}: ближайший автобус подойдёт в {time}.' \
                                       f'\n🚌Следующий автобус этого же маршрута подойдёт в {time_lst[j]}\n'
                        break
                    elif time_now < time:
                        if i + 1 == len(time_lst):
                            j = 0
                        else:
                            j = i + 1
                        output_text += f'\n🚍{route}: ближайший автобус подойдёт в {time}.' \
                                       f'\n🚌Следующий автобус этого же маршрута подойдёт в {time_lst[j]}\n'
                        break
        if output_text == f'К остановке {message.text} скоро подойдут маршруты:\n':
            output_text = f'В ближайшие 30 часов к остановке {message.text} не прибудет' \
                          f' ни один автобус.🚕\nЕсли я ошибаюсь - напишите об этом администрации.'
        await message.answer(
            text=output_text
        )

    except Exception as error:
        return message.answer(
            '⁉️Что-то пошло не так, код ошибки: 2. Сообщите администрации об этом.'
        )
