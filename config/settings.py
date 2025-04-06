import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

class Config:
    # Токен Telegram бота
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    
    # Настройки Google Cloud
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    # Максимальный размер файла (20MB)
    MAX_FILE_SIZE = 20 * 1024 * 1024
    
    # Поддерживаемые форматы файлов
    SUPPORTED_MIME_TYPES = {
        'audio/mp3': 'mp3',
        'audio/wav': 'wav',
        'audio/ogg': 'ogg', 
        'audio/webm': 'webm',
        'video/mp4': 'mp4',
        'video/webm': 'webm'
    }
    
    # Настройки распознавания речи
    SPEECH_CONFIG = {
        'encoding': 'LINEAR16',
        'sample_rate_hertz': 16000,
        'language_code': 'ru-RU'
    }
