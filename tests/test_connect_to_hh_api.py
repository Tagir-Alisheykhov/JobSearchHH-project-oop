from os import path
from unittest.mock import patch

import pytest

from src.connect_to_hh_api import HeadHunterAPI
from src.file_saver import JSONSaver
from src.vacancy import ValidateVacancy

path_to_data = path.join(path.dirname(path.dirname(__file__)), "data/")


@patch("requests.get")
def test_connection_200(mock_get) -> None:
    """
    Имитация GET-запроса APi сервиса вакансий
    :param mock_get: заменяет функцию которую хотим проверить
    """
    hh_api = HeadHunterAPI()
    mock_get.return_value.status_code.return_value = 200
    assert hh_api.get_vacancies("Python") == "[]"
    mock_get.assert_called_once_with(
        "https://api.hh.ru/vacancies",
        headers={"User-Agent": "HH-User-Agent"},
        params={"text": "Python", "page": 1, "per-page": 100},
    )


def test_validate_vacancy_salary() -> None:
    """
    Проверка корректной работы метода `salary_validate` класса `ValidateVacancy`

    """
    obj_validate_vacancy = ValidateVacancy()
    assert obj_validate_vacancy.salary_validate(0) == 0
    # int & float
    assert obj_validate_vacancy.salary_validate(1) == 1
    assert obj_validate_vacancy.salary_validate(55.99) == 55
    # str
    assert obj_validate_vacancy.salary_validate("от #$$$ 1000- рублей") == 1000

    assert obj_validate_vacancy.salary_validate("от 1000- 5000 рублей") == 5000
    assert obj_validate_vacancy.salary_validate("от 1000 00 - 5000 00 рублей") == 500000
    # dict
    assert obj_validate_vacancy.salary_validate({"from": 10, "to": 20}) == 20
    assert obj_validate_vacancy.salary_validate({"from": 50, "to": 1}) == 50
    assert obj_validate_vacancy.salary_validate({"from": 1, "to": None}) == 1
    assert obj_validate_vacancy.salary_validate({"from": None, "to": 100}) == 100
    assert obj_validate_vacancy.salary_validate({"from": None, "to": None}) == 0
    # else
    with pytest.raises(TypeError):
        assert obj_validate_vacancy.salary_validate(list())
    with pytest.raises(TypeError):
        assert obj_validate_vacancy.salary_validate(tuple())


def test_validate_for_empty_value_salary(list_with_values: dict) -> None:
    """
    Проверка корректной работы метода `validate_for_empty_value_salary` класса `ValidateVacancy`

    """
    obj_validate_vacancy = ValidateVacancy()
    assert obj_validate_vacancy.validate_for_empty_value_salary(None) == 0
    assert (
        obj_validate_vacancy.validate_for_empty_value_salary(list_with_values) == 100000
    )
    assert (
        obj_validate_vacancy.validate_for_empty_value_salary(
            {"from": 50000, "to": None}
        )
        == 50000
    )
    assert (
        obj_validate_vacancy.validate_for_empty_value_salary(
            {"from": None, "to": 80000}
        )
        == 80000
    )
    assert (
        obj_validate_vacancy.validate_for_empty_value_salary({"from": None, "to": None})
        == 0
    )


def test_class_vacancy(one_salary_1, one_salary_2) -> None:
    """
    Тестирование магических методов, предназначенных для сравнения
    объектов вакансий класса `Vacancy`.

    """
    comparison_1 = one_salary_1 > one_salary_2
    assert comparison_1 is False
    comparison_2 = one_salary_1 < one_salary_2
    assert comparison_2 is True
    comparison_3 = one_salary_1 != one_salary_2
    assert comparison_3 is True
    comparison_4 = one_salary_1 == one_salary_2
    assert comparison_4 is False
    comparison_5 = one_salary_1 >= one_salary_2
    assert comparison_5 is False
    comparison_6 = one_salary_1 <= one_salary_2
    assert comparison_6 is True


def test_json_creating_dictionary_vacancy():
    """
    Тестирование метода валидации json-файла `file_validate`
    класса `JSONSaver`.

    """
    json_saver = JSONSaver()
    with pytest.raises(TypeError):
        assert json_saver.creating_dictionary_vacancy(list("<<<virus>>>"))


def test_add_vacancy(one_salary_1):
    """
    Тестирование метода добавления json-файла `add_vacancy`
    класса `JSONSaver`.

    """
    json_saver = JSONSaver()
    with pytest.raises(AssertionError):
        assert json_saver.add_vacancy(one_salary_1)


def test_delete_vacancy(one_salary_1):
    """
    Тестирование метода удаления json-файла `add_vacancy`
    класса `JSONSaver`.

    """
    json_saver = JSONSaver()
    with pytest.raises(AssertionError):
        assert json_saver.delete_vacancy(one_salary_1)
