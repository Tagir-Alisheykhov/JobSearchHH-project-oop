"""
Модуль для объединения всего функционала программы

"""
from src.connect_to_hh_api import HeadHunterAPI, Vacancy, ValidateVacancy, JSONSaver


def api_connect(user_query: str) -> list:
    """
    Связывает функционал программы, отвечающий за
    подключением к APi и полученных данных в виде списка объектов
    :param: user_query - Результат поискового ввода пользователя
    :return: Список с объектами вакансий
    """
    # Создание экземпляра класса для работы с API сайтов с вакансиями
    hh_api = HeadHunterAPI()
    # # Получение вакансий с hh.ru в формате JSON
    hh_vacancies = hh_api.get_vacancies(user_query)
    # Преобразование набора данных из JSON в список объектов (ORIGINAL)
    vacancies_list_objs = Vacancy.cast_to_object_list(hh_vacancies)
    return vacancies_list_objs


def user_interaction() -> str:
    """
    Связывает функционал программы, который реализует преобразование
    входных данных, валидацию и фильтрацию по указанным параметрам или без них
    :return: Вывод отфильтрованных данных из HH.ru в формате JSON
    """
    search_query = input("Введите поисковый запрос: ")
    top_n = input("Введите количество вакансий для вывода в топ N: ")
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input("Введите диапазон зарплат: ")
    # -----------
    # Обработка search_query
    if top_n:
        top_n = int(top_n)
    # Обработка filter_words
    filter_words = " ".join(filter_words).lower()
    # -----------
    # Обработка salary_range
    diapason_salary = ValidateVacancy.salary_validate_input(salary_range)
    from_ = 0
    to_ = 0
    if len(diapason_salary) == 2:
        from_salary, to_salary = int(diapason_salary[0]), int(diapason_salary[1])
        from_ += from_salary
        to_ += to_salary
    elif len(diapason_salary) == 1:
        from_salary = int(diapason_salary[0])
        from_ += from_salary
    # -----------
    # Ввод параметров для фильтрации данных и
    # вывод результата работы программы.
    vacancies_list = api_connect(search_query)
    json_saver = JSONSaver()
    json_saver.save_data_in_file(vacancies_list)
    return json_saver.call_json_file_by_parameters(
        top_number=top_n,
        keyword=filter_words,
        salary_from=from_,
        salary_to=to_
    )


if __name__ == "__main__":
    # res = user_interaction()
    print(ValidateVacancy.salary_validate("от #$$$ 1000- рублей"))






# -------------------------------------------------------------------
# # Создание экземпляра класса для работы с API сайтов с вакансиями
# hh_api = HeadHunterAPI()

# # Получение вакансий с hh.ru в формате JSON
# ЕДИНСТВЕННОЕ, ЗДЕСЬ ПЕРЕДАЕТСЯ ПЕРЕМЕННАЯ (КЛЮЧЕВОЕ СЛОВО ПОЛЬЗОВАТЕЛЯ)
# hh_vacancies = hh_api.get_vacancies("Python")
# print(hh_vacancies)

# Преобразование набора данных из JSON в список объектов (ORIGINAL)
# vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)
# -------------------------------------------------------------------


# # # Пример работы конструктора класса с одной вакансией
# vacancy = Vacancy("Python Developer", "<https://hh.ru/vacancy/123456>",
#                   "100 000-200 000 руб.", "Требования: опыт работы от 3 лет...")

# print(vacancy.name)
# print(vacancy.url)
# print(vacancy.salary)
# print(vacancy.requirement)

# # Для теста
# vacancy_del = Vacancy("Python Developer", "<https://hh.ru/vacancy/123456>", "100 000-150 000 руб.", "Требования: опыт работы от 3 лет...")
# print(vacancy >= vacancy_del)
# print(res)

# print(JSONSaver.save_in_json())
# -----------------------------------------------
# # # Сохранение информации о вакансиях в файл
# json_saver = JSONSaver()
# json_saver.save_data_in_file(vacancies_list)
#
# json_saver.add_vacancy(vacancy)
#
# json_saver.delete_vacancy(vacancy)
# print(json_saver.call_json_file_by_parameters("Python"))
# -----------------------------------------------


# def search_user_query(input_query: str) -> str:
#     """
#     Получение данных по вводимому запросу пользователя.
#     :param input_query: Вводимый пользователем запрос (str)
#     :return: Список вакансий (json)
#     """
#     # # Создание экземпляра класса для работы с API сайтов с вакансиями
#     hh_api_ = HeadHunterAPI()
#
#     # # Получение вакансий с hh.ru в формате JSON
#     hh_vacancies_ = hh_api_.get_vacancies(input_query)
#     return hh_vacancies_

