import logging
from logging.handlers import RotatingFileHandler
import requests


__all__ = ['LoggedSession']


class LoggedSession(requests.Session):
    def request(self, method, url, **kwargs):
        logging.info(f"Запрос: {method} {url}")
        if "data" in kwargs:
            logging.info(f"Данные запроса: {kwargs['data']}")
        if "json" in kwargs:
            logging.info(f"JSON запрос: {kwargs['json']}")
        if "files" in kwargs:
            logging.info(f"Файлы запроса: {kwargs['files']}")

        response = super().request(method, url, **kwargs)

        logging.info(f"Ответ от {url}: {response.status_code}")
        logging.debug(f"Ответ тела: {response.text[:200]}")

        return response
