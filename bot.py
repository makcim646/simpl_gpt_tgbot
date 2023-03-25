
import aiohttp
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from db_sql import get_message, save_message, clean_message, creat_db, get_config, add_gift, check_client
import aiogram.utils.markdown as fmt
import re
import os
import ffmpeg
import speech_recognition as sr

setting = get_config()
bot = Bot(setting['bot_token']) #Telegram bot token
dp = Dispatcher(bot)


async def ask(text, id_user):
    # Замените YOUR_API_KEY на свой ключ
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
            token_len = resp['usage']['total_tokens']
            if token_len > 3300:
                clean_message(id_user)
                save_message(id_user, data[-3])
                save_message(id_user, data[-2])
                save_message(id_user, data[-1])
            message = resp['choices'][0]['message']
            save_message(id_user, message)

            return resp['choices'][0]['message']['content']

            

        
def convert(file_id):
    if os.name == 'nt':
        input_file = f"voice\\{file_id}.oga"
        output_file = f"voice\\{file_id}.wav"
    else:
        input_file = f"voice/{file_id}.oga"
        output_file = f"voice/{file_id}.wav"
    
    (ffmpeg
    .input(input_file)
    .output(output_file)
    .overwrite_output()
    .run()
    )
    os.remove(input_file)
    return output_file
    
    
def audio_to_text(file_id):
    input_file = convert(file_id)
    r = sr.Recognizer()
    message = sr.AudioFile(input_file)
    with message as source:
        audio = r.record(source)
    result = r.recognize_google(audio, language="ru-RU,en-US")
    os.remove(input_file)
    return result


@dp.message_handler(commands=['clean'])
async def see_client(message: types.Message):
    if clean_message(message.chat.id):
        await message.answer("История диалога с ботом очищена")
        return
    else:
        await message.answer("Не удалось очистить историю")
        
        
@dp.message_handler(commands=['img'])
async def see_client(message: types.Message):
    await message.answer('генерирую картинку')
    text = message.text.split('/img')[1].strip()
    response = openai.Image.create(prompt=text, n=1, size="1024x1024")
    image_url = response['data'][0]['url']

    await message.answer(fmt.hide_link(image_url), parse_mode=types.ParseMode.HTML)
        

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
    if not check_client(msg.chat.id):
        add_gift(msg.chat.id)

    file_id = msg.voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    if os.name == 'nt':
        file_save = f'voice\\{file_id}.oga'
    else:
        file_save = f'voice/{file_id}.oga'
    await bot.download_file(file_path, destination=file_save)
    
    text = audio_to_text(file_id)
    match = re.search(r"\b(с)?генерируй\b", text)
    
    if match:
        st = match.end()
        await msg.answer(text[st:])
        response = openai.Image.create(prompt=text[st:], n=1, size="1024x1024")
        image_url = response['data'][0]['url']

        await msg.answer(fmt.hide_link(image_url), parse_mode=types.ParseMode.HTML)
    else:
        print(text)
        await msg.answer(f'Ищу ответ на вопрос: {text}')
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
