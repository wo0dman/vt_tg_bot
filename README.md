# Telegram Voice to Text Bot

Бот для преобразования голосовых и видео сообщений в текст с использованием Google Speech-to-Text API.

## Требования

- Python 3.8+
- FFmpeg (для обработки аудио/видео)
- Аккаунт Google Cloud с включенным Speech-to-Text API
- Telegram бот (получить токен у @BotFather)

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-repo/vt_tg_bot.git
cd vt_tg_bot
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/Scripts/activate  # Linux/macOS
.\venv\Scripts\activate      # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Настройте конфигурацию:
- Создайте файл `.env` на основе `.env.example`
- Укажите токен бота и путь к ключу Google Cloud

## Запуск

```bash
python -m bot.core
```

## Поддерживаемые форматы

- Аудио: MP3, WAV, OGG, WEBM
- Видео: MP4, WEBM

Максимальный размер файла: 20MB

## Настройка Google Cloud

1. Создайте проект в [Google Cloud Console](https://console.cloud.google.com/)
2. Включите Speech-to-Text API
3. Создайте сервисный аккаунт и скачайте JSON-ключ
4. Укажите путь к ключу в `.env` файле

## Лицензия

MIT
