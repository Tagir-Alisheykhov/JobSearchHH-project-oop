"""
Модуль для объединения всего функционала программы

"""
import json

from src.connect_to_hh_api import HeadHunterAPI, Vacancy, CastToListObjects, JSONSaver


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


def api_connect(user_query):
    """
    Функция, связывающая функционал программы, связанный с
    подключением к APi и преобразования полученных данных в
    список объектов.
    """
    # Создание экземпляра класса для работы с API сайтов с вакансиями
    hh_api = HeadHunterAPI()
    # # Получение вакансий с hh.ru в формате JSON
    hh_vacancies = hh_api.get_vacancies(user_query)
    # Преобразование набора данных из JSON в список объектов (ORIGINAL)
    vacancies_list_objs = Vacancy.cast_to_object_list(hh_vacancies)
    return vacancies_list_objs


def user_interaction():
    platforms = ["HeadHunter"]
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    # filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    # salary_range = input("Введите диапазон зарплат: ")  # Пример: 100000 - 150000

    # -----------
    # Выдает список объектов
    vacancies_list = api_connect(search_query)

    # КЛЮЧЕВЫЕ СЛОВА ДОБАВЛЯЮТСЯ В КАЖДЫЙ НОВЫЙ ЗАПРОС (Если удалять файл. То проблема исчезает)

    json_saver = JSONSaver()
    json_saver.save_data_in_file(vacancies_list)
    print(json_saver.call_json_file_by_parameters(top_number=top_n))
    # -----------

#     filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
#
#     ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
#
#     sorted_vacancies = sort_vacancies(ranged_vacancies)
#     top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
#     print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_interaction()


# # Функция для взаимодействия с пользователем
# def user_interaction():
#     platforms = ["HeadHunter"]
#     search_query = input("Введите поисковый запрос: ")
#     top_n = int(input("Введите количество вакансий для вывода в топ N: "))
#     filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
#     salary_range = input("Введите диапазон зарплат: ") # Пример: 100000 - 150000
#
#     filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
#
#     ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
#
#     sorted_vacancies = sort_vacancies(ranged_vacancies)
#     top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
#     print_vacancies(top_vacancies)
#
























# 4. Создать функцию для взаимодействия с пользователем.
# Функция должна взаимодействовать с пользователем через консоль.
# Возможности этой функции должны быть следующими:
# - ввести поисковый запрос для запроса вакансий из hh.ru;
# - получить топ N вакансий по зарплате (N запрашивать у пользователя);
# - получить вакансии с ключевым словом в описании.
# Помимо этого функционала, можно придумать дополнительные возможности, которые покажутся удобными.
# 5. Объединить все классы и функции в единую программу.
# 6. Покрыть описанный функционал тестами.

# from src.connect_to_hh_api import HeadHunterAPI, Vacancy, CastToListObjects, JSONSaver

# # Создание экземпляра класса для работы с API сайтов с вакансиями
# hh_api = HeadHunterAPI()
#
# # # Получение вакансий с hh.ru в формате JSON
# hh_vacancies = hh_api.get_vacancies("Python")
# # print(hh_vacancies)
#
# # Преобразование набора данных из JSON в список объектов (ORIGINAL)
# vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)
#
# # # # Пример работы конструктора класса с одной вакансией
# vacancy = Vacancy("Python Developer", "<https://hh.ru/vacancy/123456>",
#                   "100 000-200 000 руб.", "Требования: опыт работы от 3 лет...")

# print(vacancy.name)
# print(vacancy.url)
# print(vacancy.salary)
# print(vacancy.requirement)

# # Для теста
# vacancy_del = Vacancy("Python Developer", "<https://hh.ru/vacancy/123456>", "100 000-150 000 руб.", "Требования: опыт работы от 3 лет...")
# print(vacancy >= vacancy_del)
#
# # print(JSONSaver.save_in_json())
#
# # # Сохранение информации о вакансиях в файл
# --------------------------------------
# json_saver = JSONSaver()
# json_saver.save_data_in_file(vacancies_list)
#
# json_saver.add_vacancy(vacancy)
#
# # json_saver.delete_vacancy(vacancy)
#
# # Вызов по ключевому слову
# print(json_saver.call_json_file_by_parameters("Python"))
# -------------------------------------------


# # Функция для взаимодействия с пользователем
# def user_interaction():
#     platforms = ["HeadHunter"]
#     search_query = input("Введите поисковый запрос: ")
#     top_n = int(input("Введите количество вакансий для вывода в топ N: "))
#     filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
#     salary_range = input("Введите диапазон зарплат: ") # Пример: 100000 - 150000
#
#     filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
#
#     ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
#
#     sorted_vacancies = sort_vacancies(ranged_vacancies)
#     top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
#     print_vacancies(top_vacancies)
#
