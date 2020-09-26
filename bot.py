from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor

import config

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


class UserCityAge(StatesGroup):
    userCity = State()
    userAge = State()


async def questions(message: types.Message, i):
    if i == 'city':
        await UserCityAge.userCity.set()
        await message.answer("Из какого ты города?")
    if i == 'age':
        await UserCityAge.userAge.set()
        await message.answer("Сколько тебе лет?")


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.first_name}')
    await questions(message, 'city')


@dp.message_handler(state=UserCityAge.userCity)
async def user_city(message: types.Message, state=FSMContext):
    answer = message.text
    await state.update_data(usercity=answer)
    await questions(message, 'age')


@dp.message_handler(state=UserCityAge.userAge)
async def user_age(message: types.Message, state=FSMContext):
    data = await state.get_data()
    userage = message.text
    usercity = data.get("usercity")
    if int(userage) > 18:
        await message.answer(f"Твой город: {usercity}")
        await message.answer(f"Твой возраст: {userage}")





if __name__ == '__main__':
    executor.start_polling(dp)
