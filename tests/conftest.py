import pytest

from src.connect_to_hh_api import Vacancy


@pytest.fixture
def list_with_values():
    """
    Список с простыми значениями
    :return: dict()

    """
    dict_values = {'from': 50000, 'to': 100000}
    return dict_values


@pytest.fixture
def one_salary_1():
    """
    Параметры одной вакансии
    :return: obj.__class__.__name__(Vacancy)
    """
    vacancy1 = Vacancy("Python Developer", "<https://hh.ru/vacancy/123456>",
                  "50 000-100 000 руб.", "Требования: опыт работы от 3 лет...")
    return vacancy1


@pytest.fixture
def one_salary_2():
    """
    Параметры одной вакансии
    :return: obj.__class__.__name__(Vacancy)
    """
    vacancy2 = Vacancy("Python Developer", "<https://hh.ru/vacancy/123456>",
                  "100 000-200 000 руб.", "Требования: опыт работы от 3 лет...")
    return vacancy2


@pytest.fixture
def list_dict_vacancy():
    """
    Возвращает словари с недопустимыми значениями
    :return: list[dict(), dict()]
    """
    vacancy1 = ({
        'name': "Python Developer",
        'url': "<https://hh.ru/vacancy/123456>",
        'salary': None,
        'requirement': "Требования: опыт работы от 98 лет...",
        'responsibility': None
    },
                {
        'name': "Python Developer",
        'url': "<https://hh.ru/vacancy/123456>",
        'salary': None,
        'requirement': "Требования: опыт работы от 98 лет...",
        'responsibility': None
    })
    return list(vacancy1)
