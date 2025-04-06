# Инструкция по развертыванию бота на сервере

## 1. Подключение к серверу
```bash
ssh root@45.12.72.25
```

## 2. Установка зависимостей
```bash
apt update && apt upgrade -y
apt install -y python3 python3-venv python3-pip ffmpeg git
```

## 3. Копирование проекта
```bash
git clone https://github.com/wo0dman/vt_tg_bot.git
cd vt_tg_bot
```

## 4. Настройка виртуального окружения
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 5. Настройка конфигурации
```bash
cp .env.example .env
nano .env  # отредактируйте файл конфигурации
```

## 6. Запуск бота
```bash
screen -S bot
python -m bot.core
```
(Для выхода из screen: Ctrl+A, затем D)

## 7. Автозапуск при перезагрузке
Добавьте в cron:
```bash
crontab -e
```
Добавьте строку:
```
@reboot cd /root/vt_tg_bot && ./venv/bin/python -m bot.core
```

## Важные примечания
1. Убедитесь что:
- Файл .env содержит правильные токены
- Сервисный ключ Google Cloud скопирован на сервер
- FFmpeg установлен и работает

2. Для управления процессом:
- Просмотр запущенных screen: `screen -ls`
- Переподключение: `screen -r bot`
- Остановка: `Ctrl+C` в screen сессии
