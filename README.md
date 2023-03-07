# simpl_gpt_tgbot
telegaram bot for using GPTchat

### Технологии
aiogram, vosk, ffmpeg

### Команды
- /start - Приветствие, появляется при первом старте бота
- /clean - удаление истории общения. Бот забывает то о чем вы говорили раньше

git clone https://github.com/tochilkinva/simpl_gpt_tgbot.git
cd simpl_gpt_tgbot

Установите зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Модели Vosk, а также FFmpeg

*Vosk* - оффлайн-распознавание аудио и получение из него текста. Модели доступны на сайте [проекта](https://alphacephei.com/vosk/models "Vosk - оффлайн-распознавание аудио"). Скачайте модель, разархивируйте и поместите папку model с файлами в папку models/vosk/model.
- [vosk-model-small-ru-0.22 - 45 Мб](https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip "Модель vosk-model-small-ru-0.22 - 45 Мб") - хуже распознает, но быстрее и весит мало.

*FFmpeg* - набор open-source библиотек для конвертирования аудио- и видео в различных форматах.
Скачайте набор exe файлов с сайта [проекта](https://ffmpeg.org/download.html "FFmpeg - набор open-source библиотек для конвертирования аудио- и видео в различных форматах.") и поместите файл ffmpeg.exe в папки models/vosk и models/silero.

author stt.py https://github.com/tochilkinva/tg_bot_stt_tts
