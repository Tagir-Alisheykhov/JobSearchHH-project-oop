"""
Модуль содержит классы для реализации функционала -
вывода актуальных данных о вакансиях из сервиса HH.ru, и последующей их
фильтрацией посредством указания дополнительных параметров пользователем.

"""

import json
from abc import ABC, abstractmethod
from typing import Any

import requests


class AbstractHHAPI(ABC):
    """
    Абстрактный класс для работы API сервиса вакансий

    """

    @abstractmethod
    def get_vacancies(self, *args: Any, **kwargs: Any) -> Any:
        """Получение вакансий из сервиса"""
        pass


class HeadHunterAPI(AbstractHHAPI):
    """
    Класс для подключения к API и получения вакансий

    """

    def __init__(self):
        """
        Инициализация параметров запроса вывод вакансий в json-формате

        """
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 1, "per-page": 100}
        self.__vacancies = []

    def __connection_to_api(self, keyword: str) -> Any:
        """
        Метод подключения к API

        """
        self.__params["text"] = keyword
        response = requests.get(
            self.__url, headers=self.__headers, params=self.__params
        )
        if response.status_code == 200:
            while self.__params.get("page") != 20:
                vacancies_ = response.json()["items"]
                self.__vacancies.extend(vacancies_)
                self.__params["page"] += 1
                return response.status_code
        else:
            return response.status_code

    def get_vacancies(self, keyword: str) -> str:
        """
        Получение данных (вакансий)

        """
        self.__connection_to_api(keyword)
        return json.dumps(self.__vacancies, indent=4, ensure_ascii=False)
