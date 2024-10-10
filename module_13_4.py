from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start_massage(message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью.')


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text='Calories')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(chosen_age=message.text)
    await message.answer('Введите свой  рост в сантиметрах:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(chosen_growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(chosen_weight=message.text)
    data = await state.get_data()
    recommended_calories = 10 * int(data['chosen_weight']) + 6.25 * int(data['chosen_growth']) - 5 * int(
        data['chosen_age']) - 5
    await message.answer(f'Ваша норма калорий {recommended_calories}')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
