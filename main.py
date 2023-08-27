from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data import DataBas
import config as cfg
import logging

logging.basicConfig(level=logging.INFO)

bot = Bot(cfg.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db = DataBas("report_data")

class SQL_Command(StatesGroup):
    sql_1 = State()
    sql_add = State()
    sql_one = State()
    sql_all = State()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        user_id = message.from_user.id
        first_name = message.from_user.first_name
        username = message.from_user.username
        if(not db.check_user(user_id)):
            db.add_user(user_id, first_name, username)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)


            if db.check_rang(user_id) is not None:
                button1 = types.KeyboardButton("Сдать отчёт")
                button2 = types.KeyboardButton("Руководящий состав")
                markup.add(button1, button2)
                await message.answer(cfg.START_TEXT, reply_markup=markup)
            else:
                button1 = types.KeyboardButton("Руководящий состав")
                markup.add(button1)
                await message.answer(cfg.START_TEXT, reply_markup=markup)

@dp.message_handler(commands='sql')
async def sql_commands(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        user_id = message.from_user.id
        if db.check_rang(user_id) == 10:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            button1 = types.KeyboardButton("Добавить")
            button2 = types.KeyboardButton("Выбрать одно")
            button3 = types.KeyboardButton("Выбрать все")
            markup.add(button1, button2, button3)
            await message.answer(cfg.SQL_BEGIN_TEXT, reply_markup=markup)
            await SQL_Command.sql_1.set()

@dp.message_handler(state=SQL_Command.sql_1)
async def sql_1_text(message: types.Message, state: FSMContext):
    if message.chat.type == types.ChatType.PRIVATE:
        if message.text == "Добавить":
            await SQL_Command.sql_add.set()
            await message.answer(cfg.SQL_ADD_TEXT, reply_markup=types.ReplyKeyboardRemove())
        elif message.text == "Выбрать одно":
            await SQL_Command.sql_one.set()
            await message.answer(cfg.SQL_SELECT_ONE_TEXT, reply_markup=types.ReplyKeyboardRemove())
        elif message.text == "Выбрать все":
            await SQL_Command.sql_all.set()
            await message.answer(cfg.SQL_SELECT_ALL_TEXT, reply_markup=types.ReplyKeyboardRemove())
        elif message.text == "/cancel":
            await state.reset_state()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            button1 = types.KeyboardButton("Сдать отчёт")
            button2 = types.KeyboardButton("Руководящий состав")
            markup.add(button1, button2)
            await message.answer(cfg.START_TEXT, reply_markup=markup)

@dp.message_handler(state=SQL_Command.sql_add)
async def sql_add_text(message: types.Message, state: FSMContext):
    if message.chat.type == types.ChatType.PRIVATE:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button1 = types.KeyboardButton("Сдать отчёт")
        button2 = types.KeyboardButton("Руководящий состав")
        markup.add(button1, button2)
        if message.text == "/cancel":
            await state.reset_state()
            await message.answer(cfg.START_TEXT, reply_markup=markup)
        else:
            try:
                db.add_with_bot(message.text)
                await message.answer(cfg.SQL_CORRECT, reply_markup=markup)
                await state.finish()
            except Exception as es:
                print(f"[ERROR] {es}")
                await message.answer(cfg.SQL_ERROR)
                await state.reset_state()

@dp.message_handler(state=SQL_Command.sql_one)
async def sql_add_text(message: types.Message, state: FSMContext):
    if message.chat.type == types.ChatType.PRIVATE:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button1 = types.KeyboardButton("Сдать отчёт")
        button2 = types.KeyboardButton("Руководящий состав")
        markup.add(button1, button2)
        if message.text == "/cancel":
            await state.reset_state()
            await message.answer(cfg.START_TEXT, reply_markup=markup)
        else:
            try:
                await message.answer(db.select_one(message.text))
            except Exception as es:
                print(f"[ERROR] {es}")
                await message.answer(cfg.SQL_ERROR)


@dp.message_handler(state=SQL_Command.sql_all)
async def sql_add_text(message: types.Message, state: FSMContext):
    if message.chat.type == types.ChatType.PRIVATE:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button1 = types.KeyboardButton("Сдать отчёт")
        button2 = types.KeyboardButton("Руководящий состав")
        markup.add(button1, button2)
        if message.text == "/cancel":
            await state.reset_state()
            await message.answer(cfg.START_TEXT, reply_markup=markup)
        else:
            try:
                await message.answer(db.select_all(message.text))
            except Exception as es:
                print(f"[ERROR] {es}")
                await message.answer(cfg.SQL_ERROR)

if __name__ == "__main__":
    executor.start_polling(dp)
