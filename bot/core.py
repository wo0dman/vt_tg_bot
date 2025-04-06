import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from pydub import AudioSegment
import ffmpeg
from google.cloud import speech

# Настройка логгирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class VoiceToTextBot:
    def __init__(self, token):
        self.token = token
        self.supported_formats = {
            'audio/mp3': 'mp3',
            'audio/wav': 'wav',
            'audio/ogg': 'ogg',
            'audio/webm': 'webm',
            'video/mp4': 'mp4',
            'video/webm': 'webm'
        }
        self.max_file_size = 20 * 1024 * 1024  # 20MB
        
        # Инициализация клиента Google Speech-to-Text
        try:
            self.speech_client = speech.SpeechClient()
        except Exception as e:
            logger.error(f"Ошибка инициализации Google Speech API: {e}")
            raise RuntimeError(
                "Не удалось инициализировать Google Speech API. Проверьте:\n"
                "1. Файл сервисного аккаунта Google Cloud (указан в GOOGLE_APPLICATION_CREDENTIALS)\n"
                "2. Доступность API Speech-to-Text в вашем проекте Google Cloud\n"
                "3. Интернет-соединение сервера"
            )
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Привет! Отправь мне голосовое сообщение или видео, и я преобразую его в текст."
        )
    
    async def handle_media(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            # Проверка типа и размера файла
            file = await self._validate_file(update)
            if not file:
                return
            
            # Создаем прогресс-бар
            progress_msg = await update.message.reply_text("Обработка: [░░░░░░░░░░] 0%")
            
            # Конвертируем в WAV
            await self._update_progress(progress_msg, 20)
            audio_path = await self._convert_to_wav(file)
            
            # Распознаем речь
            await self._update_progress(progress_msg, 50)
            text = await self._recognize_speech(audio_path)
            
            # Отправляем результат
            await self._update_progress(progress_msg, 90)
            await update.message.reply_text(f"Результат распознавания:\n\n{text}")
            
            # Завершаем прогресс-бар
            await self._update_progress(progress_msg, 100, done=True)
            
        except Exception as e:
            logger.error(f"Error processing media: {e}")
            await update.message.reply_text("Произошла ошибка при обработке файла. Попробуйте еще раз.")
    
    async def _validate_file(self, update: Update):
        """Проверяет файл на соответствие требованиям."""
        file = None
        
        if update.message.voice:
            file = await update.message.voice.get_file()
        elif update.message.video:
            file = await update.message.video.get_file()
        elif update.message.audio:
            file = await update.message.audio.get_file()
        elif update.message.document:
            file = await update.message.document.get_file()
        
        if not file:
            await update.message.reply_text("Пожалуйста, отправьте голосовое сообщение или видео.")
            return None
        
        if file.file_size > self.max_file_size:
            await update.message.reply_text(f"Файл слишком большой. Максимальный размер: {self.max_file_size//1024//1024}MB")
            return None
        
        return file
    
    async def _convert_to_wav(self, file):
        """Конвертирует медиафайл в WAV формат."""
        # Скачиваем файл
        file_path = f"temp_{file.file_id}.{self.supported_formats.get(file.mime_type, 'mp3')}"
        await file.download_to_drive(file_path)
        
        # Конвертируем в WAV
        wav_path = f"converted_{file.file_id}.wav"
        
        if file.mime_type.startswith('video/'):
            # Извлекаем аудио из видео
            (
                ffmpeg
                .input(file_path)
                .output(wav_path, acodec='pcm_s16le', ac=1, ar='16k')
                .run(quiet=True)
            )
        else:
            # Конвертируем аудио
            audio = AudioSegment.from_file(file_path)
            audio.export(wav_path, format="wav")
        
        return wav_path
    
    async def _recognize_speech(self, audio_path):
        """Распознает речь из аудиофайла."""
        with open(audio_path, "rb") as audio_file:
            content = audio_file.read()
        
        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="ru-RU",
        )
        
        response = self.speech_client.recognize(config=config, audio=audio)
        return "\n".join([result.alternatives[0].transcript for result in response.results])
    
    async def _update_progress(self, progress_msg, percent, done=False):
        """Обновляет прогресс-бар."""
        progress = int(percent / 10)
        bar = "🟩" * progress + "⬜" * (10 - progress)
        text = f"Обработка: {bar} {percent}%"
        
        if done:
            text = "✅ Обработка завершена!"
        
        await progress_msg.edit_text(text)

def main():
    # Получаем токен бота из переменных окружения или конфига
    from config.settings import Config
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN") or Config.TELEGRAM_BOT_TOKEN
    if not bot_token:
        print("Ошибка: Не задан TELEGRAM_BOT_TOKEN")
        print("Добавьте токен в .env файл или в config/settings.py")
        print("Пример .env файла смотрите в .env.example")
        raise ValueError("Не задан TELEGRAM_BOT_TOKEN")
    
    bot = VoiceToTextBot(bot_token)
    
    # Создаем и настраиваем приложение
    application = ApplicationBuilder().token(bot_token).build()
    
    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(MessageHandler(
        filters.VOICE | filters.VIDEO | filters.AUDIO | filters.Document.ALL,
        bot.handle_media
    ))
    
    # Запускаем бота
    application.run_polling()

if __name__ == "__main__":
    main()
