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

prod = crud_fuctions.get_all_products()

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = 1000

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_reg = KeyboardButton(text='Регистрация')
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
kb.add(button_reg)
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

@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    user_test= crud_fuctions.is_icluded(str(message.text))
    if user_test:
        await message.answer("Пользователь существует, введите другое имя")
        await RegistrationState.username.set()
    else:
        await state.update_data(username=message.text)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message,state):
    await state.update_data(age=message.text)
    reg_use = await state.get_data()
    reg_use = crud_fuctions.add(f"{reg_use['username']}",
                                f"{reg_use['email']}", f"{reg_use['age']}")
    await state.finish()







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
    colories = round(10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161)
    #colories = round(10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5)*A
    await message.answer(f'Ваша норма каллорий: {colories}')
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)