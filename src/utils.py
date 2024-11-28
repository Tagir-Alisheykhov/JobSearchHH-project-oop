import json


def top_n_func(top_number: int = None, query_result: list = None):
    """
    Фильтрует список вакансий. Пользователь вводит необходимое количество
    Топ-вакансий (по зарплате) в порядке убывания.
    :param query_result: Список с вакансиями, полученные по запросу пользователя
    :param top_number: Количество Топ-вакансий
    :return: Топовые вакансии в порядке возрастания

    """
    # Преобразование набора данных из JSON в список объектов
    if isinstance(top_number, int):
        sorted_list = sorted(query_result, key=lambda x: x.get('salary'), reverse=True)[:top_number]
        return sorted_list
