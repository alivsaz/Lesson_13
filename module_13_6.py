# Ещё больше выбора
from config import api     # файл с api

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb_start = ReplyKeyboardMarkup(resize_keyboard=True)
kb_start_button = KeyboardButton('Рассчитать')
kb_start_button_2 = KeyboardButton('Информация')
kb_start.add(kb_start_button, kb_start_button_2)

kb_calories = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
            InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')]],
            resize_keyboard=True)


class UserState(StatesGroup):
    data = {}
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb_start)

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb_calories)

@dp.callback_query_handler(text='formulas')
async def formula(call):
    await call.message.answer('10 * вес(кг) + 6.25 * рост(см) + 5 * возраст(лет) - 161')

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст',)
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    UserState.data = await state.get_data()
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    UserState.data = await state.get_data()
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def set_calories(message, state):
    await state.update_data(weight=message.text)
    UserState.data = await state.get_data()
    result = int(UserState.data["weight"]) * 10 + int(UserState.data["growth"]) * 6.25 + int(UserState.data["age"]) * 5 - 161
    await message.answer(f'Ваш норма каллорий: {result}')
    await state.finish()

@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
