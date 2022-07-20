from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN
from eazy_parser import WikiParser
from sqlighter import SQLighter


"""Получаем данные с парсера"""
data = WikiParser.parser()

"""Инициализация БД и обновление данных"""
db = SQLighter('db.db')
db.clear_date()
db.put_date(data)

"""Инициализация бота и диспетчера сообщений"""
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

"""Логика работы чат-бота"""
@dp.message_handler(commands=['start', 'help'])
async def commands_start(message: types.Message):
    if message.text == "/start":
        await bot.send_message(message.from_user.id,
                               "Привет! Этот бот парсит данные со странички Википедии.\nЧтобы узнать больше введи команду /help")

    if message.text == "/help":
        await bot.send_message(message.from_user.id, "Если готов, напиши мне название города, который ты ищешь.\n")
        await bot.send_message(message.from_user.id,  "Вводи запрос с большой буквы, если помнишь начало названия города. Например:  Моск\n")                                   
        await bot.send_message(message.from_user.id,  "Если не помнишь как начинается город, введи его часть с маленькой буквы. Например:  град\n Удачи!")

async def main(message, db):
    if message != "":
        answer = db.get_names(message)
        if len(answer) > 1:
            return f"Какой именно город ты ищешь?\n{'; '.join(str(x[0]) for x in answer)}"
        elif len(answer) == 0:
            return f"Города: {message} нет в Московской области, исходя из информации с Вики."
        else:
            finish_answer = db.get_data(answer[0])
            return f"Город: {answer[0][0]}\nСсылка на вики: {finish_answer[0]}\nНаселение составляет {finish_answer[1]} человек."


@dp.message_handler()
async def start_bot(message: types.Message):
    answer = await main(str(message.text), db)
    await bot.send_message(message.from_user.id, answer)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
