"""


"""
import os.path
import re
import json
import requests
from os import path
from typing import Any
from itertools import chain
from abc import ABC, abstractmethod

from src.utils import top_n_func

path_to_data = path.join(path.dirname(path.dirname(__file__)), 'data/')


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
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = {'text': '', 'page': 1, 'per-page': 100}
        self.__vacancies = []

    def __connection_to_api(self, keyword: str) -> int:
        """
        Метод подключения к API

        """
        self.__params['text'] = keyword
        response = requests.get(self.__url,
                                headers=self.__headers,
                                params=self.__params)
        if response.status_code == 200:
            while self.__params.get('page') != 20:
                vacancies_ = response.json()['items']
                self.__vacancies.extend(vacancies_)
                self.__params['page'] += 1
                return response.status_code
        else:
            return response.status_code

    def get_vacancies(self, keyword: str) -> str:
        """
        Получение данных (вакансий)

        """
        self.__connection_to_api(keyword)
        return json.dumps(self.__vacancies,
                          indent=4,
                          ensure_ascii=False)


class ValidateVacancy:
    """
    Класс для валидаций значений класса обработки вакансий

    """
    @classmethod
    def salary_validate(cls, meaning_salary: list | tuple | str | int | float | dict) \
            -> str | int | float | dict:
        """
        Валидация значений ключа с зарплатой ('salary') с разными типами данных

        """
        if meaning_salary != 0:
            if isinstance(meaning_salary, int):
                # 'int'
                return meaning_salary
            if isinstance(meaning_salary, float):
                # 'float'
                return int(meaning_salary)
            elif isinstance(meaning_salary, str):
                # 'str'
                salary_value = (re.findall(r'\d+[-., ]\d+', meaning_salary) or
                                re.findall(r'\d+', meaning_salary))
                cleaned_salary = list()
                for salary in salary_value:
                    clean_salary = re.sub(r'[^0-9]', "", salary)
                    cleaned_salary.append(int(clean_salary))
                return max(cleaned_salary)
            elif isinstance(meaning_salary, dict):
                # 'dict' с ключами "from" и "to"
                if not meaning_salary['from']:
                    meaning_salary['from'] = 0
                if not meaning_salary['to']:
                    meaning_salary['to'] = 0
                salary_value = max(meaning_salary['from'],
                                   meaning_salary['to'])
                return int(salary_value)
            else:
                raise TypeError('Неправильный тип атрибута зарплаты')
        elif meaning_salary == 0:
            return meaning_salary

    @classmethod
    def validate_for_empty_value_salary(cls, meaning_salary: dict | None) \
            -> dict | int:
        """
        Валидация json-файла с вакансиями, на пустые значения ключей

        """
        if not meaning_salary:
            meaning_salary = 0
            return meaning_salary
        else:
            if not meaning_salary['from']:
                meaning_salary['from'] = 0
            if not meaning_salary['to']:
                meaning_salary['to'] = 0
            # Дополнительная валидация на корректность значений
            meaning_salary = cls.salary_validate(meaning_salary)
            return meaning_salary


class CastToListObjects:
    """
    Класс для создания списка объектов вакансий

    """

    @classmethod
    def to_list(cls, vacancies: Any) -> list:
        """
        Создание списка объектов класса Vacancy

        """
        vacancies_list = list()
        for vacancy in json.loads(vacancies):
            vacancy['salary'] = ValidateVacancy.validate_for_empty_value_salary(vacancy['salary'])
            # Создание списка
            name = vacancy['name']
            url = vacancy['alternate_url']
            salary = vacancy['salary']
            requirement = vacancy['snippet']['requirement']
            responsibility = vacancy['snippet']['responsibility']
            returned_obj_vacancy = (
                Vacancy(name, url, salary, requirement, responsibility)
            )
            vacancies_list.append(returned_obj_vacancy)
        return vacancies_list


class Vacancy:
    """
    Класс для работы с вакансиями.

    """
    __slots__ = ('name', 'url', 'salary', 'requirement', 'responsibility')

    name: str
    link: str
    salary: int
    requirement: str
    responsibility: str

    def __init__(self, name, url, salary, requirement='null', responsibility='null'):
        """
        Инициализация атрибутов вакансии

        """
        self.name = name
        self.url = url
        self.salary = ValidateVacancy.salary_validate(salary)
        self.requirement = requirement
        self.responsibility = responsibility

    def __lt__(self, other: Any) -> bool:
        """Сравнение объектов (меньше)"""
        return self.salary < other.salary

    def __gt__(self, other: Any) -> bool:
        """Сравнение объектов (больше)"""
        return self.salary > other.salary

    def __le__(self, other: Any) -> bool:
        """Сравнение объектов (меньше или равно)"""
        return self.salary <= other.salary

    def __ge__(self, other: Any) -> bool:
        """Сравнение объектов (больше или равно)"""
        return self.salary >= other.salary

    def __eq__(self, other: Any) -> bool:
        """Сравнение объектов (равные значения)"""
        return self.salary == other.salary

    def __ne__(self, other: Any) -> bool:
        """Сравнение объектов (неравные значения)"""
        return self.salary != other.salary

    @classmethod
    def cast_to_object_list(cls, vacancies: str) -> list:
        """
        Создание списка из объектов вакансий

        """
        list_of_objs = CastToListObjects.to_list(vacancies)
        return list_of_objs


class FileSaver(ABC):
    """
    Абстрактный класс для добавления файла вакансий

    """

    @abstractmethod
    def save_data_in_file(self):
        pass

    @abstractmethod
    def add_vacancy(self):
        pass

    @abstractmethod
    def delete_vacancy(self):
        pass


class JSONSaver(FileSaver):
    """
    Класс для добавления информации о вакансиях в JSON-файл.

    """
    filtered_data = list()

    def __init__(self, filename='DefaultFilename'):
        """
        Инициализация атрибутов.

        """
        self.filename = filename
        self.path_to_file = path_to_data + self.filename + '.json'
        with open(self.path_to_file, 'w', encoding='UTF-8') as file:
            empty_value_json = []
            json.dump(empty_value_json, file, indent=4, ensure_ascii=False)
        self.absolut_path_to_file = self.path_to_file

    def file_validate(self, new_data: list | dict) -> None:
        """
        Валидация файла и его обработка перед записью в JSON-файл
        Данный метод обрабатывает как массив с вакансиями, так и словарь с одной вакансией

        """
        with open(self.absolut_path_to_file, 'r+', encoding="UTF-8") as file:
            empty_file = json.load(file)
            empty_file.extend(new_data)
            formatted_file = list({d["url"]: d for d in empty_file}.values())
            with open(self.absolut_path_to_file, 'w+', encoding="UTF-8") as file_:
                json.dump(formatted_file, file_, indent=4, ensure_ascii=False)

    def creating_dictionary_vacancy(self, data: list) -> None:
        """
        Создание словаря из полученных параметров вакансии

        """
        new_list_dict = list()
        for vacancy in data:
            if not isinstance(vacancy, Vacancy):
                raise TypeError('Неверный тип атрибута/ов вакансии')
            elif isinstance(vacancy, Vacancy):
                formation_dict = dict()
                formation_dict['name'] = vacancy.name
                formation_dict['url'] = vacancy.url
                formation_dict['salary'] = vacancy.salary
                formation_dict['requirement'] = vacancy.requirement
                formation_dict['responsibility'] = vacancy.responsibility
                new_list_dict.append(formation_dict)
        return self.file_validate(new_list_dict)

    def save_data_in_file(self, *information_vacancies: list) -> None:
        """
        Сохраняем информацию о вакансиях в формате JSON

        """
        # Удаление лишнего списка верхнего уровня
        flattened_data = list(chain.from_iterable(information_vacancies))
        self.creating_dictionary_vacancy(flattened_data)

    def call_json_file_by_parameters(self,
                                     top_number: int = None,
                                     keyword: str = " ",
                                     salary_from: int = False,
                                     salary_to: int = False
                                     ) -> str:
        """
        Получение данных из JSON-файла по указанным критериям.
        Имеет необязательные критерии, такие как:
        - `keyword` (опционально) - ключевое слово, по которому будет
        производиться поиск вакансии
        - `salary_from` и `salary_to` (опционально) - дополнительные параметры
        выбора диапазона зарплат необходимых вакансий.
        Можно указать только один параметр или сразу оба.

        """
        # Функция с параметром "Поисковой запрос"
        # Функция с параметром "Топ-х вакансий"
        # Функция фильтрация вакансий по ключевому слову
        # Функция фильтрации по диапазону зарплат

        with open(self.absolut_path_to_file, 'r', encoding="utf-8") as js_file:
            data = json.load(js_file)  # Выводит транзакции по запросу (уже обработанные)
            # Фильтрация данных с выводом зарплат в порядке убывания
            data = top_n_func(top_number, data)

            for vacancy in data:
                key_true_vacancies = None
                # print(vacancy)
                # Фильтрация вакансий по ключевому слову
                for value in vacancy.values():
                    # print(value)
                    if isinstance(value, str) and keyword in value:
                        key_true_vacancies = vacancy

                # Фильтрация вакансий по указанным параметрам зарплаты (от и до)
                if key_true_vacancies:
                    # print(json.dumps(key_true_vacancies, indent=4, ensure_ascii=False))
                    if salary_from and salary_to and salary_from < salary_to:
                        if salary_from <= key_true_vacancies['salary'] <= salary_to:
                            self.filtered_data.append(vacancy)
                    elif not salary_from and not salary_to:
                        self.filtered_data.append(vacancy)
                    elif (salary_from and not salary_to and
                          key_true_vacancies["salary"] >= salary_from):
                        self.filtered_data.append(vacancy)
                    elif (salary_to and not salary_from and
                          key_true_vacancies["salary"] <= salary_to):
                        self.filtered_data.append(vacancy)
                    elif salary_from > salary_to:
                        raise ValueError("'salary_from' не может быть больше 'salary_to'")

            return json.dumps(self.filtered_data, indent=4, ensure_ascii=False)

    def add_vacancy(self, *vacancy: Vacancy) -> None:
        """
        Метод добавляющий вакансию в файл.
        Принимает объект класса Vacancy

        """
        self.creating_dictionary_vacancy(list(vacancy))

    def delete_vacancy(self, *del_vacancy: Vacancy) -> None:
        """
        Метод удаления выбранной вакансии.
        Принимает объект класса Vacancy.

        """
        formatted_file_json = list()
        del_vacancy_name = ''
        del_vacancy_url = ''
        del_vacancy_salary = 0
        try:
            with open(self.path_to_file, 'r+', encoding="UTF-8") as file:
                data = json.load(file)
        except json.JSONDecodeError:
            raise ValueError('Файл пуст')
        else:
            for param in list(del_vacancy):
                del_vacancy_name = param.name
                del_vacancy_url = param.url
                del_vacancy_salary = param.salary
            for vacancy in data:
                if (vacancy.get('name') == del_vacancy_name and
                        vacancy.get('url') == del_vacancy_url and
                        vacancy.get('salary') == del_vacancy_salary):
                    del vacancy
                else:
                    formatted_file_json.append(vacancy)
            with open(self.path_to_file, 'w', encoding="UTF-8") as file:
                json.dump(formatted_file_json, file,
                          indent=4,
                          ensure_ascii=False)

# ПРОВЕРЬ РАБОТУ call_json_file_by_parameters С ПАРАМЕТРАМИ И БЕЗ НИХ
# А ТАКЖЕ ПОПРОБУЙ ПОМЕСТИТЬ ПЕРЕМЕННУЮ КЛАССА filtered_data = list() ВНУТРЬ ДАННОЙ ФУНКЦИИ






# ----------------------
#     def __init__(self, filename=None):
#         """
#         Инициализация атрибутов.
#
#         """
#
#         self.filename = filename if filename else "DefaultName"
#
#         # if not self.filename:
#         #     self.filename = "DefaultName"
#         #     print(f"1. Отработало условие: {self.filename}")
#
#         print(f'2. Отработал основной поток: {self.filename}')
#
#         self.path_to_file = path_to_data + self.filename + '.json'
#
#         if not path.exists(self.path_to_file):
#             with open(self.path_to_file, 'w', encoding='UTF-8') as file:
#                 empty_value_json = []
#                 json.dump(empty_value_json, file, indent=4, ensure_ascii=False)
#         self.path_to_file = self.path_to_file
# -----------------------
# class JSONSaver(FileSaver):
#
#     def __init__(self, filename=None):
#         self.filename = filename if filename else "DefaultName"
#         print(self.filename)
#         self.path_to_file = path_to_data + self.filename + '.json'
#
#     def file_validate(self, new_data: list | dict) -> None:
#         """
#         Валидация файла и его обработка перед записью в JSON-файл
#         Данный метод обрабатывает как массив с вакансиями, так и словарь с одной вакансией
#
#         """
#         print(f'3.1 Отработал метод file_validate')
#         print(f'3.1. (Имя файла {self.filename})')
#         print('----------------------')
#
#         with open(self.path_to_file, 'r+', encoding="UTF-8") as file:
#             empty_file = json.load(file)
#
#             print(f'3.2. Отработал метод file_validate')
#             print(f'3.2. (Имя файла {self.filename})')
#             print('----------------------')
#             # Исключение дублей вакансий
#             formatted_file = list({d["url"]: d for d in empty_file}.values())
#
#             formatted_file.extend(new_data)
#
#             print(f'3.3. Отработал метод file_validate')
#             print(f'3.3. (Имя файла {self.filename})')
#             print('----------------------')
#
#             with open(self.path_to_file, 'w+', encoding="UTF-8") as file_:
#                 json.dump(formatted_file, file_, indent=4, ensure_ascii=False)
#             print(f'3.4. Отработал метод file_validate')
#             print(f'3.4. (Имя файла {self.filename})')
#             print('----------------------')
#
#     def creating_dictionary_vacancy(self, data: list) -> None:
#         """
#         Создание словаря из полученных параметров вакансии
#
#         """
#         print(f'4.1 creating_dictionary_vacancy')
#         print(f'4.1. (Имя файла {self.filename})')
#         print('----------------------')
#
#         new_list_dict = list()
#         for vacancy in data:
#             if isinstance(vacancy, Vacancy):
#                 formation_dict = dict()
#                 formation_dict['name'] = vacancy.name
#                 formation_dict['url'] = vacancy.url
#                 formation_dict['salary'] = vacancy.salary
#                 formation_dict['requirement'] = vacancy.requirement
#                 formation_dict['responsibility'] = vacancy.responsibility
#                 new_list_dict.append(formation_dict)
#             else:
#                 raise TypeError('Неверный тип атрибута/ов вакансии')
#         self.file_validate(new_list_dict)
#
#     def save_data_in_file(self, *information_vacancies: list) -> None:
#         """
#         Сохраняем информацию о вакансиях в формате JSON
#
#         """
#         print(f'5.1 save_data_in_file')
#         print(f'5.1. (Имя файла {self.filename})')
#         print('----------------------')
#
#         # Удаление лишнего списка верхнего уровня
#         flattened_data = list(chain.from_iterable(information_vacancies))
#         # print(self.creating_dictionary_vacancy(flattened_data))
#         self.creating_dictionary_vacancy(flattened_data)
#
#     def add_vacancy(self):
#         pass
#
#     def delete_vacancy(self):
#         pass








    # def file_validate(self, new_data: list | dict) -> None:
    #     """
    #     Валидация файла и его обработка перед записью в JSON-файл
    #     Данный метод обрабатывает как массив с вакансиями, так и словарь с одной вакансией
    #
    #     """
    #     if isinstance(new_data, dict):
    #         new_data = list(new_data)
    #     if self.path_to_file:
    #         try:
    #             with open(self.path_to_file, "r", encoding="UTF-8") as old_file_path:
    #                 old_file_data = json.load(old_file_path)
    #                 # Объединение старых и новых вакансий
    #                 if isinstance(new_data, list):
    #                     new_data.extend(old_file_data)
    #                 else:
    #                     raise TypeError
    #                 # Исключение дублей вакансий
    #                 formatted_file = list({d["url"]: d for d in new_data}.values())
    #         except json.JSONDecodeError as err:
    #             print(f"Файл пуст(1) {err}")
    #         except TypeError as err:
    #             raise TypeError(f"Ошибка типа входных данных {err}")
    #         else:
    #             # Создание нового файла с добавленными новыми вакансиями
    #             with open(self.path_to_file, "w", encoding="UTF-8") as old_file_path:
    #                 json.dump(formatted_file, old_file_path, indent=4, ensure_ascii=False)
    #     else:
    #         with open(self.path_to_file, "w", encoding="UTF-8") as new_file_path:
    #             json.dump(new_data, new_file_path, indent=4, ensure_ascii=False)