"""
Модуль для создания файла с актуальными вакансиями.
Также в данном модуле возможно добавить вакансии, удалить

"""

import json
from abc import ABC, abstractmethod
from itertools import chain
from os import path

from src.vacancy import Vacancy
from src.utils import from_and_to_parameters, top_n_func

path_to_data = path.join(path.dirname(path.dirname(__file__)), "data/")


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

    def __init__(self, filename="DefaultFilename"):
        """
        Инициализация атрибутов.

        """
        self.filename = filename
        self.path_to_file = path_to_data + self.filename + ".json"

    @classmethod
    def __validate_objects_vacancy(cls, data: list | dict):
        """

        """
        new_list_dict = list()
        for vacancy in data:
            if not isinstance(vacancy, Vacancy):
                raise TypeError("Неверный тип атрибута/ов вакансии")
            elif isinstance(vacancy, Vacancy):
                formation_dict = dict()
                formation_dict["name"] = vacancy.name
                formation_dict["url"] = vacancy.url
                formation_dict["salary"] = vacancy.salary
                formation_dict["requirement"] = vacancy.requirement
                formation_dict["responsibility"] = vacancy.responsibility
                new_list_dict.append(formation_dict)
        new_list_dict_unique = list({d["url"]: d for d in new_list_dict}.values())
        return new_list_dict_unique

    def creating_dictionary_vacancy(self, data: list):
        """
        Создание словаря из полученных параметров вакансии

        """
        validate = self.__validate_objects_vacancy(data)
        with open(self.path_to_file, 'w+', encoding="UTF-8") as file:
            json.dump(validate, file, indent=4, ensure_ascii=False)

    def save_data_in_file(self, *information_vacancies: list):
        """
        Сохраняем информацию о вакансиях в формате JSON

        """
        # Удаление лишнего списка верхнего уровня
        flattened_data = list(chain.from_iterable(information_vacancies))
        return self.creating_dictionary_vacancy(flattened_data)

    def call_json_file_by_parameters(
            self,
            top_number: int = None,
            keyword: str = None,
            salary_from: int = None,
            salary_to: int = None,
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
        filtered_data = list()
        if (self.path_to_file
                and path.exists(self.path_to_file)
                and isinstance(self.path_to_file, type("JSON"))):
            with open(self.path_to_file, "r+", encoding="utf-8") as js_file:
                data = json.load(js_file)
                # Фильтрация данных с выводом зарплат в порядке убывания
                if top_number:
                    data = top_n_func(top_number, data)
                for vacancy in data:
                    key_true_vacancies = None
                    # Фильтрация вакансий по ключевому слову
                    for value in vacancy.values():
                        if isinstance(value, str):
                            if keyword:
                                if keyword in str(value).lower():
                                    key_true_vacancies = vacancy
                            else:
                                key_true_vacancies = vacancy
                    # Фильтрация вакансий по указанным параметрам зарплаты (от и до)
                    if key_true_vacancies is not None and isinstance(
                            key_true_vacancies, dict
                    ):
                        res = from_and_to_parameters(
                            salary_from, salary_to, key_true_vacancies
                        )
                        filtered_data.append(res)
                return json.dumps(filtered_data, indent=2, ensure_ascii=False)
        else:
            raise ValueError("Файл отсутствует, либо поврежден.")

    def add_vacancy(self, *vacancy: Vacancy) -> None:
        """
        Метод добавляющий вакансию в файл.
        Принимает объект класса Vacancy

        """
        vacancy = self.__validate_objects_vacancy(list(vacancy))
        if (self.path_to_file
                and path.exists(self.path_to_file)
                and isinstance(self.path_to_file, type("JSON"))):
            with open(self.path_to_file, 'r+', encoding="UTF-8") as file:
                vacancies = json.load(file)
                for value in vacancy:
                    vacancies.append(value)
                    vacancies_unique = list({d["url"]: d for d in vacancies}.values())
                with open(self.path_to_file, 'w+', encoding="UTF-8") as refresh_file:
                    json.dump(vacancies_unique, refresh_file, indent=4, ensure_ascii=False)
        else:
            with open(self.path_to_file, 'w+', encoding="UTF-8") as refresh_file:
                json.dump(vacancy, refresh_file, indent=4, ensure_ascii=False)

    def delete_vacancy(self, *del_vacancy: Vacancy) -> None:
        """
        Метод удаления выбранной вакансии.
        Принимает объект класса Vacancy.

        """
        formatted_file_json = list()
        del_vacancy_name = ""
        del_vacancy_url = ""
        del_vacancy_salary = 0
        try:
            with open(self.path_to_file, "r+", encoding="UTF-8") as file:
                data = json.load(file)
        except json.JSONDecodeError:
            raise ValueError("Файл пуст")
        else:
            for param in list(del_vacancy):
                del_vacancy_name = param.name
                del_vacancy_url = param.url
                del_vacancy_salary = param.salary
            for vacancy in data:
                if (
                        vacancy.get("name") == del_vacancy_name
                        and vacancy.get("url") == del_vacancy_url
                        and vacancy.get("salary") == del_vacancy_salary
                ):
                    del vacancy
                else:
                    formatted_file_json.append(vacancy)
            with open(self.path_to_file, "w", encoding="UTF-8") as file:
                json.dump(formatted_file_json, file, indent=4, ensure_ascii=False)
