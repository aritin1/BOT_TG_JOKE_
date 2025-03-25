from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Картинка')],
                                      [KeyboardButton(text='Опрос')],
                                     [KeyboardButton(text='Курс валют')],
                                     [KeyboardButton(text='Погода')],
                                      [KeyboardButton(text='Фильмы'),
                                     KeyboardButton(text='Шутки')]
                                     ],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню...')


picture_catalog = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Футбол', callback_data='football')],
    [InlineKeyboardButton(text='Бокс', callback_data='box')],
    [InlineKeyboardButton(text='Баскетбол', callback_data='basketball')]])


jokes_catalog = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Черный юмор и про программистов', callback_data='blackjoke')],
    [InlineKeyboardButton(text='Обычный юмор', callback_data='common')]])
