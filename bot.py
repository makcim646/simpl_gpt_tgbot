
import aiohttp
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from db_sql import get_message, save_message, clean_message, creat_db, get_config, add_gift, check_client
import os
from stt import STT


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
stt = STT()

@dp.message_handler(commands=['clean'])
async def see_client(message: types.Message):
    if clean_message(message.chat.id):
        await message.answer("История диалога с ботом очищена")
        return
    else:
        await message.answer("Не удалось очистить историю")
        

@dp.message_handler(commands=['start'])
async def see_client(message: types.Message):
    if not check_client(message.chat.id):
        add_gift(message.chat.id)
    
    text ="""Привет, я - искусственный интеллект, разработанный для выполнения различных заданий и помощи людям в решении разнообразных вопросов. Вот несколько примеров того, что я умею делать:
1. Отвечать на вопросы по различным темам, таким как наука, медицина, искусство, спорт и т.д.
2. Предлагать подходящие рецепты блюд на основе данных о ингредиентах.
3. Помогать переводить тексты с одного языка на другой.
4. Выполнять простые математические операции, решать уравнения и т.д.
5. Предоставлять информацию о погоде в определенном регионе.
6. Помогать находить места, где можно купить определенные товары и услуги в конкретном районе.
7. Выполнять задачи, связанные с управлением временем, планированием и напоминаниями о важных событиях.
8. Искать определенные факты, цитаты или события в истории.
В целом, я стараюсь быть полезной и помочь вам найти информацию и получить поддержку в различных сферах."""
        
    await message.answer(text)

@dp.message_handler(content_types=[types.ContentType.VOICE])
async def get_voice(msg: types.Message):
    file_id = msg.voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_save = f'voice\\{file_id}.oga'
    await bot.download_file(file_path, destination=file_save)
    text = stt.audio_to_text(file_save)
    if os.path.exists(file_save):
        os.remove(file_save)

    if not check_client(msg.chat.id):
        add_gift(msg.chat.id)
    await msg.answer('Ищу ответ')

    answer = await ask(text, msg.chat.id)

    if answer is None:
        answer = 'Не получилось найти'

    await msg.reply(answer)

        
        
@dp.message_handler()
async def send_msg(msg: types.Message):
    if not check_client(msg.chat.id):
        add_gift(msg.chat.id)
    
    await msg.answer('Ищу ответ')

    text = await ask(msg.text, msg.chat.id)

    if text == None:
        text = 'Не получилось найти'

    await msg.reply(text)


if __name__ == '__main__':
    creat_db()
    executor.start_polling(dp)
    #asyncio.run(dp)
