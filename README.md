#  From HeadHunter

## Описание:
Программа для поиска и преобразования данных из HeadHunter.

## Установка:

### Способ - 1
```
1. Скопируйте URL-адрес репозитория:
----------------------------------------------------------------
https://github.com/Tagir-Alisheykhov/Alisheykhov_TM_Homework.git
----------------------------------------------------------------
2. Откройте PyCharm или другой используемый вами интерпретатор
и кликните на "Get From VCS".

3. Вставьте скопированный адрес в строку "URL"
4. Далее в строке "Directory" выберите расположение репозитория на вашем ПК. Либо оставьте без изменений
5. Затем кликните на "Clone" для запуска проекта
```
### Способ - 2
```
1. Откройте "PowerShell" или "Terminal"
2. Введите команду "git clone" и добавьте ссылку на скопированный репозиторий:
--------------------------------------------------------------------------
git clone https://github.com/Tagir-Alisheykhov/Alisheykhov_TM_Homework.git
--------------------------------------------------------------------------
3. Запустите свой интерпретатор
4. Кликните на "Open"  
5. Найдите проект который вы добавили с помощью "git clone URL" (он должен сохраниться в вашей корневой директории)
6. Запустите найденный проект
```

## Описание функциональности

Основной модуль 'main'
- [ `main.py` ] - Главный модуль программы. Объединяет модули из папки `src`. 
- [ `connect_to_hh_api.py.py` ] - Содержит в себе классы для реализации функционала по получению данных об актуальных вакансиях из сервиса HeadHunter
- [ `file_saver.py` ] - Модуль для создания файла с актуальными вакансиями. а также возможно удаление вакансий, либо добавление новых
- [ `vacancy.py` ] - Модуль содержащий классы для работы со списком вакансий, а также валидации данных 
- [ `utils.py` ] - Вспомогательный модуль для обработки вводимых пользователем параметров поиска и фильтрация данных 
с учётом заданных параметров.
- Все модули в папке "/tests" названы относительно тестируемых модулей из папки "/src", с добавлением префикса "test_"


## Список зависимостей:
- `certifi`           2024.8.30 Python package for providing Mozilla's CA Bundle.
- `charset-normalizer`3.4.0 The Real First Universal Charset Detector. Open, modern and actively maintaine...
- `idna`              3.10  Internationalized Domain Names in Applications (IDNA)
- `requests`          2.32.3 Python HTTP for Humans.
- `types-requests`    2.32.0.20241016 Typing stubs for requests
- `urllib3`           2.2.3 HTTP library with thread-safe connection pooling, file post, and more.
- `black`             24.10.0 The uncompromising code formatter.
- `click`             8.1.7  Composable command line interface toolkit
- `colorama`          0.4.6  Cross-platform colored terminal text.
- `coverage`          7.6.4  Code coverage measurement for Python
- `flake8`            7.1.1  the modular source code checker: pep8 pyflakes and co
- `iniconfig`         2.0.0  brain-dead simple config-ini parsing
- `isort`             5.13.2 A Python utility / library to sort Python imports.
- `mccabe`            0.7.0  McCabe checker, plugin for flake8
- `mypy`              1.13.0 Optional static typing for Python
- `mypy-extensions`   1.0.0  Type system extensions for programs checked with the mypy type checker.
- `packaging`         24.1   Core utilities for Python packages
- `pathspec`          0.12.1 Utility library for gitignore style pattern matching of file paths.
- `platformdirs`      4.3.6  A small Python package for determining appropriate platform-specific dirs, e.g. a `user data dir`.
- `pluggy`            1.5.0  plugin and hook calling mechanisms for python
- `pycodestyle`       2.12.1 Python style guide checker
- `pyflakes`          3.2.0  passive checker of Python programs
- `pytest`            8.3.3  pytest: simple powerful testing with Python
- `pytest-cov`        6.0.0  Pytest plugin for measuring coverage.
- `typing-extensions` 4.12.2 Backported and Experimental Type Hints for Python 3.8+


## Лицензия:
Этот проект не лицензирован