from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import requests
from bs4 import BeautifulSoup
import app.keyboards as kb

from jokeapi import Jokes  # Import the Jokes class


router = Router()


class Survey(StatesGroup):
    name = State()
    surname = State()
    age = State()
    fav_thing = State()
    fav_film = State()
    fav_food = State()
    fav_game = State()


# def get_films():
#     url = "https://cinematica.kg/cinema/6"
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#     }
#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.text, 'lxml')
#
#     movies = []
#     movie_section = soup.find_all('div', class_="halls")
#
#     for film in movie_section:
#         title = film.find_all('div', class_='hall-item')
#         if title:
#             movies.append(title.text.strip())
#
#     return movies


# print(get_films())






def get_weather():
    url = 'https://www.gismeteo.ru/weather-bishkek-5327/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    temperature = soup.find('temperature-value', {'from-unit': 'c'})
    if temperature:
        temperature = temperature['value']
    else:
        temperature = "Температура не найдена"

    feel_temperature = soup.find('div', class_='weather-feel')
    if feel_temperature:
        feel_temperature = feel_temperature.find('temperature-value', {'from-unit': 'c'})['value']
    else:
        feel_temperature = "Не указано"

    weather_info = f"В Бишкеке\nТемпература: {temperature}°C\nПо ощущениям: {feel_temperature}°C"
    return weather_info

def get_exchange_rates():
    url = 'https://valuta.kg/'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')

        rates = {}

        table = soup.find('div', class_="kurs-bar__rates")

        rows = table.find_all('tr')

        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:
                currency = cols[0].text.strip()
                rate = cols[1].text.strip()
                rates[currency] = rate

        return rates
    else:
        return f"Ошибка загрузки данных: {response.status_code}"

@router.message(F.text == 'Шутки')
async def send_jokes_catalog(message: Message):
    await message.answer('Выберите тему шуток', reply_markup=kb.jokes_catalog)

async def send_joke(callback: CallbackQuery, categories=None):
    j = await Jokes()
    joke = await j.get_joke(category=categories)

    text = joke["joke"] if joke["type"] == "single" else f"{joke['setup']}\n{joke['delivery']}"
    await callback.message.answer(text)

@router.callback_query(F.data == 'common')
async def send_jokes_common(callback: CallbackQuery):
    await send_joke(callback, [])

@router.callback_query(F.data == 'blackjoke')
async def send_jokes_black(callback: CallbackQuery):
    await send_joke(callback, ['dark', 'programming'])

@router.message(F.text == 'Фильмы')
async def send_films(message: Message):
    await message.answer('Фильмы на сегодня:\n'
                         'Белоснежка\n'
                         'Микки 17\n'
                         'Өч\n'
                         'Новокаин\n'
                         'Ашыгым\n'
                         'Астрал. Спуск к дьяволу\n'
                         'Novocaine (ENG.)\n'
                         'Сырдуу Самарканд\n'
                         'Чёрный чемодан – двойная игра')
    # films = get_films()
    # if films:
    #     await message.answer("\n".join(films))
    # else:
    #     await message.answer("Не удалось найти расписание фильмов.")



@router.message(F.text == 'Погода')
async def send_weather(message: Message):
    weather = get_weather()
    await message.answer(weather, reply_markup=kb.main)


@router.message(F.text == 'Курс валют')
async def currency_command(message: Message):
    rates = get_exchange_rates()
    if rates:
        response = "Курсы валют:\n"
        for currency, rate in rates.items():
            response += f"{currency}: {rate}\n"
        await message.answer(response, reply_markup=kb.main)
        await message.answer('вот сайт https://valuta.kg/')
    else:
        await message.answer("Не удалось получить данные о курсах валют. Попробуйте позже.")

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет!', reply_markup=kb.main)

@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('вы нажали на кнопку помощи')



@router.message(F.text == 'Картинка')
async def picture_catalog(message: Message):
    await message.answer('Выберите тему картинки', reply_markup=kb.picture_catalog)

@router.callback_query(F.data == 'football')
async def football(callback: CallbackQuery):
    await callback.message.answer_photo(
        photo='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ0Bo65iyb1kapzIMtEdcirNvxzyfMosgAwWQ&s'
    )
    await callback.message.answer('Вы выбрали футбол')

@router.callback_query(F.data == 'box')
async def box(callback: CallbackQuery):
    await callback.message.answer_photo(
        photo='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQMU85wlVLAK-TWd7W7ZXE85xxH0IehcXC8TA&s'
    )
    await callback.message.answer('Вы выбрали бокс')

@router.callback_query(F.data == 'basketball')
async def basketball(callback: CallbackQuery):
    await callback.message.answer_photo(
        photo='https://i.pinimg.com/736x/dd/df/f6/dddff62dae60cc4c3a063df2d6494d47.jpg'
    )
    await callback.message.answer('Вы выбрали баскетбол')




@router.message(F.text == 'Опрос')
async def survey(message: Message, state: FSMContext):
    await state.set_state(Survey.name)
    await message.answer('Введите ваше имя')

@router.message(Survey.name)
async def survey_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Survey.surname)
    await message.answer('Введите вашу фамилию')

@router.message(Survey.surname)
async def survey_name(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await state.set_state(Survey.age)
    await message.answer('Введите ваш возраст')

@router.message(Survey.age)
async def survey_name(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Survey.fav_thing)
    await message.answer('Введите ваш любимый предмет в школе')

@router.message(Survey.fav_thing)
async def survey_name(message: Message, state: FSMContext):
    await state.update_data(fav_thing=message.text)
    await state.set_state(Survey.fav_film)
    await message.answer('Введите ваш любимый фильм')

@router.message(Survey.fav_film)
async def survey_name(message: Message, state: FSMContext):
    await state.update_data(film=message.text)
    await state.set_state(Survey.fav_food)
    await message.answer('Введите вашу любимую еду')

@router.message(Survey.fav_food)
async def survey_name(message: Message, state: FSMContext):
    await state.update_data(food=message.text)
    await state.set_state(Survey.fav_game)
    await message.answer('Введите вашу любимую игру')

@router.message(Survey.fav_game)
async def survey_fav_game(message: Message, state: FSMContext):
    await state.update_data(game=message.text)
    data = await state.get_data()
    await message.answer(f'Имя: {data["name"]}\n'
                         f'Фамилия: {data["surname"]}\n'
                         f'Возраст: {data["age"]}\n'
                         f'Любимый предмет в школе: {data["fav_thing"]}\n'
                         f'любимый фильм: {data["film"]}\n'
                         f'Любимая еда: {data["food"]}\n'
                         f'Любимая игра: {data["game"]}')
    await state.clear()





