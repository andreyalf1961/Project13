from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.add(button1)
kb.add(button2)

in_kb = InlineKeyboardMarkup()
button1_i = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button2_i = InlineKeyboardButton(text='Формулы расчета', callback_data='formulas')
in_kb.add(button1_i)
in_kb.add(button2_i)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start_massage(message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию', reply_markup=in_kb)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
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


@dp.message_handler()
async def start_massage(message):
    await message.answer('Введите команду /start, чтобы начать общение. ')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
