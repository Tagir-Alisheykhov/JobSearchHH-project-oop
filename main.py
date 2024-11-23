"""
Модуль для объединения всего функционала программы

"""
from src.connect_to_hh_api import HeadHunterAPI, Vacancy, CastToListObjects, JSONSaver

# # Создание экземпляра класса для работы с API сайтов с вакансиями
hh_api = HeadHunterAPI()

# # Получение вакансий с hh.ru в формате JSON
hh_vacancies = hh_api.get_vacancies("Python")
# print(hh_api.call_vacancies())

# Преобразование набора данных из JSON в список объектов (ORIGINAL)
vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)
# print(vacancies_list)


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

# # Сохранение информации о вакансиях в файл
json_saver = JSONSaver()

print(json_saver.call_json_file_by_parameters("Python"))

# json_saver.add_vacancy(vacancy)

# json_saver.delete_vacancy(vacancy)
#
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


# if __name__ == "__main__":
    # user_interaction()
