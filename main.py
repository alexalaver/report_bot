from aiogram import Bot, Dispatcher, executor, types
from data import DataBas
import config as cfg

bot = Bot(cfg.TOKEN)
dp = Dispatcher(bot)
db = DataBas("report_data")

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        user_id = message.from_user.id
        if(not db.check_user(user_id)):
            pass

if __name__ == "__main__":
    executor.start_polling(dp)
