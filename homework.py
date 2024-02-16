import logging
import os
import sys
import time
from http import HTTPStatus

import requests
from dotenv import load_dotenv
from telegram import Bot, TelegramError

from exceptions import EmptyListError, NonExistendStatusError, StatusError

load_dotenv()


PRACTICUM_TOKEN = os.getenv("PRACTICUM_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

RETRY_TIME = 600
ENDPOINT = "https://practicum.yandex.ru/api/user_api/homework_statuses/"
HEADERS = {"Authorization": f"OAuth {PRACTICUM_TOKEN}"}


HOMEWORK_STATUSES = {
    "approved": "Работа проверена: ревьюеру всё понравилось. Ура!",
    "reviewing": "Работа взята на проверку ревьюером.",
    "rejected": "Работа проверена: у ревьюера есть замечания.",
}


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def send_message(bot, message):
    """Отправка сообщения в Телеграмм."""
    message_error = "Сообщение в телеграмм не отправлено"
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.info("Сообщение отправлено.")
    except TelegramError:
        logger.error(message_error)


def get_api_answer(current_timestamp):
    """Получение данных с API Яндекс Практикума."""
    try:
        timestamp = current_timestamp or int(time.time())
        params = {"from_date": timestamp}
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
    except requests.exceptions.RequestException as error:
        logger.error(error)
        raise SystemExit(error)
    else:
        try:
            if response.status_code != HTTPStatus.OK:
                message_error = "Ответ API некорректен."
                logger.error(message_error)
                raise StatusError(message_error)
            return response.json()
        except requests.JSONDecodeError as error:
            logger.error(error)
            raise error


def check_response(response):
    """Проверка данных полученных с API."""
    if type(response) is not dict:
        message_error = "Response не является словарем."
        logger.error(message_error)
        raise TypeError(message_error)
    if type(response.get("homeworks")) is not list:
        message_error = "Homeworks не является списком."
        logger.error(message_error)
        raise TypeError(message_error)
    if response.get("homeworks") is None:
        message_error = "Ошибка ключа homeworks."
        logger.error(message_error)
        raise KeyError(message_error)
    if len(response.get("homeworks")) == 0:
        message_error = "Список пуст."
        logger.error(message_error)
        raise EmptyListError(message_error)
    return response.get("homeworks")


def parse_status(homework):
    """Определение статуса Домашней работы."""
    homework_name = homework.get("homework_name")
    homework_status = homework.get("status")
    if homework_status is None:
        message_error = "homework_status имеет пустое значение."
        logger.error(message_error)
        raise KeyError(message_error)
    if homework_name is None:
        message_error = "homework_name имеет пустое значение."
        logger.error(message_error)
        raise KeyError(message_error)
    if homework_status not in HOMEWORK_STATUSES:
        message_error = (
            f"{homework_status} - недокументированный статус домашней работы."
        )
        logger.error(message_error)
        raise NonExistendStatusError(message_error)
    verdict = HOMEWORK_STATUSES.get(homework_status)
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверка на наличие обязательных прерменных окружения."""
    message_error = "Отсутствие обязательных переменных окружения:"
    if PRACTICUM_TOKEN is None:
        logger.critical(f"{message_error} PRACTICUM_TOKEN")
        return False
    if TELEGRAM_TOKEN is None:
        logger.critical(f"{message_error} TELEGRAM_TOKEN")
        return False
    if TELEGRAM_CHAT_ID is None:
        logger.critical(f"{message_error} TELEGRAM_CHAT_ID")
        return False


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        exit()
    bot = Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    error_message = None

    while True:

        try:
            response = get_api_answer(current_timestamp)
            homeworks = check_response(response)
            if homeworks:
                message = parse_status(homeworks[0])
                time.sleep(RETRY_TIME)
                logger.info("Сообщение отправлено.")

        except Exception as error:
            message = f"Сбой в работе программы: {error}"
            if error_message is None or error.args != error_message.args:
                send_message(bot, message)
                error_message = error
            logger.error(message)
            time.sleep(RETRY_TIME)
        else:
            send_message(bot, message)


if __name__ == "__main__":
    main()
