"""
Модуль для валидации вакансий

"""
import json
import re
from typing import Any


class ValidateVacancy:
    """
    Класс для валидаций значений класса обработки вакансий

    """

    @classmethod
    def salary_validate_input(cls, value: str) -> Any:
        """
        Валидация вводимых значений зарплаты
        :return: диапазон зарплат
        """
        user_input = re.findall(r"(\d[0-9]+)", value)
        if len(user_input) <= 2:
            return user_input

    @classmethod
    def salary_validate(cls, meaning_salary: Any) -> Any:
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
                salary_value = re.findall(
                    r"\d+[-., ]\d+", meaning_salary
                ) or re.findall(r"\d+", meaning_salary)
                cleaned_salary = list()
                for salary in salary_value:
                    clean_salary = re.sub(r"[^0-9]", "", salary)
                    cleaned_salary.append(int(clean_salary))
                return max(cleaned_salary)
            elif isinstance(meaning_salary, dict):
                # 'dict' с ключами "from" и "to"
                if not meaning_salary["from"]:
                    meaning_salary["from"] = 0
                if not meaning_salary["to"]:
                    meaning_salary["to"] = 0
                salary_value = max(meaning_salary["from"], meaning_salary["to"])
                return int(salary_value)
            else:
                raise TypeError("Неправильный тип атрибута зарплаты")
        elif meaning_salary == 0:
            return meaning_salary

    @classmethod
    def validate_for_empty_value_salary(cls, meaning_salary: dict | None) -> dict | int:
        """
        Валидация json-файла с вакансиями, на пустые значения ключей

        """
        if not meaning_salary:
            meaning_salary = 0
            return meaning_salary
        else:
            if not meaning_salary["from"]:
                meaning_salary["from"] = 0
            if not meaning_salary["to"]:
                meaning_salary["to"] = 0
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
            vacancy["salary"] = ValidateVacancy.validate_for_empty_value_salary(
                vacancy["salary"]
            )
            # Создание списка
            name = vacancy["name"]
            url = vacancy["alternate_url"]
            salary = vacancy["salary"]
            requirement = vacancy["snippet"]["requirement"]
            responsibility = vacancy["snippet"]["responsibility"]
            returned_obj_vacancy = Vacancy(
                name, url, salary, requirement, responsibility
            )
            vacancies_list.append(returned_obj_vacancy)
        return vacancies_list


class Vacancy:
    """
    Класс для работы с вакансиями.

    """

    __slots__ = ("name", "url", "salary", "requirement", "responsibility")

    name: str
    link: str
    salary: int
    requirement: str
    responsibility: str

    def __init__(self, name, url, salary, requirement="null", responsibility="null"):
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
