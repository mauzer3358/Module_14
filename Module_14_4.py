from aiogram import Bot, Dispatcher,executor,types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import crud_fuctions
import asyncio
import config, products

api = config.API
bot = Bot(token= api)
dp = Dispatcher(bot, storage= MemoryStorage())

#initate = crud_fuctions.initate_db()
prod = crud_fuctions.get_all_products()

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text= 'Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
kb.row(button,button2)
kb.add(button3)

kb_inline = InlineKeyboardMarkup()
button_product1 = InlineKeyboardButton(text= 'Product1', callback_data='product_buying')
button_product2 = InlineKeyboardButton(text= 'Product2', callback_data='product_buying')
button_product3 = InlineKeyboardButton(text= 'Product3', callback_data='product_buying')
button_product4 = InlineKeyboardButton(text= 'Product4', callback_data='product_buying')
kb_inline.row(button_product1,button_product2,button_product3,button_product4)

@dp.message_handler(commands = ['start'])
async def start(message):
    await message.answer('Привет, Я бот, помогающий твоему здоровью!',
                         reply_markup = kb) # после этого появится клавиатура)

@dp.message_handler(text = "Информация")
async def info(message):
    await message.answer("Формула Миффлина - Сан Жеора:"
                         "количество каллорий = 10 x вес (кг)+6,25 x рост (см) – 5 x возраст (г) – 161)'")

@dp.message_handler(text = "Купить")
async def get_buying_list(message):
    global products
    for i in range(0,4):
         with open(f'{i+1}.jpeg', "rb") as foto:
           await message.answer_photo(foto, f'Название: {prod[i][1]} | Описание: {prod[i][2]} | '
                                            f'Цена: {prod[i][3]}',)
    await message.answer('Выберите продукт для покупки: ',reply_markup = kb_inline)

@dp.callback_query_handler(text = 'product_buying')
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()

@dp.message_handler(text = "Рассчитать")
async def set_age(message):
    await message.answer("Введите свой возраст:")
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async  def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    # 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161
    # (10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) + 5) x A
    colories = round(10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161)
    #colories = round(10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5)
    await message.answer(f'Ваша норма каллорий: {colories}')
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)