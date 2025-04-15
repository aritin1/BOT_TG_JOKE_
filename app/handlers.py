from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import requests
from bs4 import BeautifulSoup
import app.keyboards as kb
import sqlite3



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
    fav_color = State()

def get_db_connection():
    conn = sqlite3.connect("survey.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS survey (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            surname TEXT,
            age INTEGER,
            fav_thing TEXT,
            fav_film TEXT,
            fav_food TEXT,
            fav_game TEXT,
            fav_color TEXT
            
        )
    ''')
    conn.commit()
    return conn




def get_movies():
    url = "https://kg.kinoafisha.info/bishkek/movies/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            movies = [
                movie.text.strip()
                for movie in soup.select(".movieItem_title")
                if movie.text.strip()
            ]

            return (
                "Фильмы в прокате:\n" + "\n".join(movies)
                if movies else "Не удалось найти фильмы."
            )
        return "Ошибка соединения."
    except Exception:
        return "Ошибка. Не удалось загрузить фильмы."




def get_weather():
    url = 'https://wttr.in/Bishkek?format=%C|%t|%w|%h'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            weather, temp, wind, humidity = response.text.strip().split("|")
            return (f"Погода в Бишкеке сейчас:\n"
                    f"Температура: {temp}\n"
                    f"Влажность: {humidity}\n"
                    f"Ветер: {wind}\n")
        else:
            return "Ошибка при запросе погоды."
    except Exception:
        return "Не удалось получить прогноз."

def get_exchange_rates():
    url = 'https://valuta.kg/'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')

        tables = soup.find_all("table", class_="kurs-table")
        if not tables:
            return "Не удалось найти таблицу с курсами валют."

        currencies = []
        currency_table = tables[1] if len(tables) > 1 else None
        if currency_table is None:
            return "Не удалось найти таблицу с нужными курсами."

        rows = currency_table.find_all("tr")
        currency_names = [".","USD", "EUR", "RUB", "KZT", "CNY", "GBP"]

        currency_info = []
        for i, row in enumerate(rows):
            cols = row.find_all("td")
            if len(cols) == 2 and i < len(currency_names):
                buy_rate = cols[0].text.strip()
                sell_rate = cols[1].text.strip()
                currency_info.append(f"{currency_names[i]}: Покупка {buy_rate} / Продажа {sell_rate}")

        if not currency_info:
            return "Не удалось найти данные по валютам."

        return '\n'.join(currency_info)
    else:
        return f"Ошибка при запросе данных: {response.status_code}"

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
    films = get_movies()
    if films:
        await message.answer(films)
    else:
        await message.answer("Не удалось найти расписание фильмов.")



@router.message(F.text == 'Погода')
async def send_weather(message: Message):
    weather = get_weather()
    await message.answer(weather, reply_markup=kb.main)


@router.message(F.text == 'Курс валют')
async def currency_command(message: Message):
    currencies = get_exchange_rates()

    if isinstance(currencies, str):
        await message.answer(currencies, reply_markup=kb.main)
    else:
        response = "Доступные валюты:\n"
        for currency in currencies:
            response += f"{currency}\n"
        await message.answer(response, reply_markup=kb.main)

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
    conn = get_db_connection()
    cursor = conn.cursor()
    user_id = message.from_user.id

    cursor.execute("SELECT * FROM survey WHERE user_id = ?", (user_id,))
    existing_data = cursor.fetchone()
    if existing_data:
        await message.answer("Вы уже проходили опрос. Вот ваши ответы:")
        result_text = (
            f"1. Имя: {existing_data[2]}\n"
            f"2. Фамилия: {existing_data[3]}"
            f"2. Возраст: {existing_data[4]}\n"
            f"3. Любимый предмет: {existing_data[5]}\n"
            f"4. Любимый фильм: {existing_data[6]}\n"
            f"5. Любимая еда: {existing_data[7]}\n"
            f"6. Любимая игра: {existing_data[8]}\n"
            f"7. Любимое блюдо: {existing_data[9]}\n"

        )
        await message.answer(result_text)
        conn.close()
        return

    await message.answer("Как вас зовут?")
    await state.set_state(Survey.name)
    conn.close()

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
async def survey_name(message: Message, state: FSMContext):
    await state.update_data(game=message.text)
    await state.set_state(Survey.fav_color)
    await message.answer('Введите ваш любимый цвет')

@router.message(Survey.fav_color)
async def survey_fav_game(message: Message, state: FSMContext):
    await state.update_data(color=message.text)
    data = await state.get_data()
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
                INSERT INTO survey (user_id, name, surname, age, fav_thing, fav_film, fav_food, fav_game, fav_color)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
            message.from_user.id,
            data.get('name'),
            data.get('surname'),
            data.get('age'),
            data.get('fav_thing'),
            data.get('film'),
            data.get('food'),
            data.get('color'),
            message.text
        ))
        conn.commit()

        result_answers = (f'Имя: {data["name"]}\n'
                         f'Фамилия: {data["surname"]}\n'
                         f'Возраст: {data["age"]}\n'
                         f'Любимый предмет в школе: {data["fav_thing"]}\n'
                         f'любимый фильм: {data["film"]}\n'
                         f'Любимая еда: {data["food"]}\n'
                         f'Любимая игра: {data["game"]}\n'
                         f'Любимый цвет: {data["color"]}')
        await message.answer(result_answers, parse_mode="Markdown")
    except Exception as e:
        await message.answer("Произошла ошибка при сохранении данных")
        print(f"Database error: {str(e)}")

    finally:
        conn.close()
        await state.clear()





