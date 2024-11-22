# Цепочка вопросов
from config import api     # файл с api

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    data = {}
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text='Calories')
async def set_age(message):
    await message.answer('Введите свой возраст')
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
    result = int(UserState.data["weight"]) * 10 + int(UserState.data["growth"]) * 6.25 + int(UserState.data["age"]) * 5 + 5
    await message.answer(f'Ваш норма каллорий: {result}')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)