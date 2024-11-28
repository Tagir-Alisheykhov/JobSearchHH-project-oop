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


def from_and_to_parameters(salary_from: int, salary_to: int, vacancy: dict):
    """
    :param vacancy: Словарь с данными одной вакансии
    :param salary_from: Параметр поиска зарплаты "От"
    :param salary_to: Параметр поиска зарплаты "До"
    :return: Отфильтрованные о вакансии
    """
    if salary_from and salary_to and salary_from < salary_to:
        if salary_from <= vacancy['salary'] <= salary_to:
            return vacancy
    elif not salary_from and not salary_to:
        return vacancy
    elif (salary_from and not salary_to and
          vacancy["salary"] >= salary_from):
        return vacancy
    elif (salary_to and not salary_from and
          vacancy["salary"] <= salary_to):
        return vacancy
    elif salary_from > salary_to:
        raise ValueError("'salary_from' не может быть больше 'salary_to'")
