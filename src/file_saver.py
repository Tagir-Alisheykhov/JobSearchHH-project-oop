import json
from abc import ABC, abstractmethod
from itertools import chain
from os import path
from typing import Any

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
        with open(self.path_to_file, "w", encoding="UTF-8") as file:
            empty_value_json = []
            json.dump(empty_value_json, file, indent=4, ensure_ascii=False)
        self.absolut_path_to_file = self.path_to_file

    def file_validate(self, new_data: list | dict) -> None:
        """
        Валидация файла и его обработка перед записью в JSON-файл
        Данный метод обрабатывает массив с вакансиями

        """
        with open(self.absolut_path_to_file, "r+", encoding="UTF-8") as file:
            empty_file = json.load(file)
            empty_file.extend(new_data)
            formatted_file = list({d["url"]: d for d in empty_file}.values())
            with open(self.absolut_path_to_file, "w+", encoding="UTF-8") as file_:
                json.dump(formatted_file, file_, indent=4, ensure_ascii=False)

    def creating_dictionary_vacancy(self, data: list) -> Any:
        """
        Создание словаря из полученных параметров вакансии

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
        return self.file_validate(new_list_dict)

    def save_data_in_file(self, *information_vacancies: list) -> None:
        """
        Сохраняем информацию о вакансиях в формате JSON

        """
        # Удаление лишнего списка верхнего уровня
        flattened_data = list(chain.from_iterable(information_vacancies))
        self.creating_dictionary_vacancy(flattened_data)

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
        with open(self.absolut_path_to_file, "r", encoding="utf-8") as js_file:
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
