# homework_bot
![Homework_bot_workflow](https://github.com/bissaliev/homework_bot/actions/workflows/main.yml/badge.svg)

## Технологии
- python
- telegram bot

## Описание
__Проект создан в учебных целях.__

Телеграмм-бот, созданный для контроля статуса проверки домашнего задания студента Яндекс.Практикума. Бот написан на языке Python, используется библиотека python-telegram-bot, настроенно логирование. В автоматическом режиме запрашивает состояние, обращаясь к API Яндекс.Практикум через определенное время. Если состояние за этот промежуток времени изменилось - программа выдает ответ, содержащий один из статусов:

- approved - 'Работа проверена: ревьюеру всё понравилось. Ура!'
- reviewing - 'Работа взята на проверку ревьюером.'
- rejected - 'Работа проверена: у ревьюера есть замечания.'

## Как запустить проект:
В первую очередь необходимо зарегистрировать Телеграмм-бота и получить от него токен, узнать свой id в Телеграмме и получить токен API Яндекс.Практикума.

Затем клонировать репозиторий и перейти в него в командной строке:
```bash
git clone git@github.com:bissaliev/homework_bot.git
```
```bash
cd homework_bot
```

Cоздать и активировать виртуальное окружение:
```bash
python3 -m venv venv
```
```bash
source venv/bin/activate
```
Установить зависимости из файла requirements.txt:
```bash
pip install -r requirements.txt
```
Записать три переменных в общее пространство переменных окружения:
```bash
export PRACTICUM_TOKEN=<Ваш токен Яндекс.Практикума>
```
```bash
export TELEGRAM_TOKEN=<Токен телеграмм-бота>
```
```bash
export TELEGRAM_CHAT_ID=<ваш id в Телеграмме>
```

Или создайте файл `.env` в корне проекта:
```bash
PRACTICUM_TOKEN=<Ваш токен Яндекс.Практикума>
TELEGRAM_TOKEN=<Токен телеграмм-бота>
TELEGRAM_CHAT_ID=<ваш id в Телеграмме>
```


Запустить файл homework.py:
```bash
python3 homework.py
```

## Автор
[Биссалиев Олег](https://github.com/bissaliev?tab=repositories)
