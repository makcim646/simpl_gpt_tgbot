
import aiohttp
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from db_sql import get_message, save_message, clean_message, creat_db, get_config

setting = get_config()

async def ask(text, id_user):

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {setting['api_key']}",
    }

    data = get_message(id_user)
    save_message(id_user, {"role": "user", "content": f"{text}"})
    data.append({"role": "user", "content": f"{text}"})

    json = {
        "model": "gpt-3.5-turbo",
        "messages": data
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=json) as response:
            if response.status != 200:
                return None
            resp = await response.json()
            message = resp['choices'][0]['message']
            save_message(id_user, message)

            return resp['choices'][0]['message']['content']



bot = Bot(setting['bot_token']) #Telegram bot token
dp = Dispatcher(bot)

@dp.message_handler(commands=['clean'])
async def see_client(message: types.Message):
    if clean_message(message.chat.id):
        await message.answer("История диалога с ботом очищена")
        return
    else:
        await message.answer("Не удалось очистить историю")


@dp.message_handler()
async def send_curs(msg: types.Message):
    await msg.answer('Ищу ответ')

    text = await ask(msg.text, msg.chat.id)

    if text == None:
        text = 'Не получилось найти'

    await msg.reply(text)


if __name__ == '__main__':
    creat_db()
    executor.start_polling(dp)
    #asyncio.run(dp)
