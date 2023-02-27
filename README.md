# API_YAMDB

[![Python](https://img.shields.io/badge/-Python-464641?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-464646?style=flat-square&logo=django)](https://www.djangoproject.com/)
[![Pytest](https://img.shields.io/badge/Pytest-464646?style=flat-square&logo=pytest)](https://docs.pytest.org/en/6.2.x/)
[![Postman](https://img.shields.io/badge/Postman-464646?style=flat-square&logo=postman)](https://www.postman.com/)

# Описание

Проект YaMDb собирает отзывы пользователей на произведения. 
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». 
Произведению может быть присвоен жанр из списка предустановленных.
Пользователи оставляют к произведениям текстовые отзывы и ставят 
произведению оценку в диапазоне от одного до десяти.
Пользователи могут оставлять комментарии к отзывам.

# Категории пользователей

Пользователи делятся на 5 категорий:

- Суперюзер - SuperUser
- Админ - Admin
- Модератор - Moderator
- Авторизованный пользователь - User (присваивается всем новым пользователям)
- Неавторизованный пользователь - UnauthUser

# Права пользователей

**UnauthUser:**
* Просмотр описания произведений, чтение отзывов и комментариев.
    
**User:** 
* Просмотр описания произведений, чтение отзывов и комментариев.
* Публикация отзывов, комментариев.
* Редактирование/удаление своих отзывов/комментариев.
    
**Moderator:**
* Просмотр описания произведений, чтение отзывов и комментариев.
* Публикация отзывов, комментариев.
* Редактирование/удаление ВСЕХ отзывов/комментариев.

**SuperUser/Admin:**
* Полные права на все действия.

# Функционал

# Установка:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Vladislav-Rybachuk/api_yamdb.git
```

```
cd api_yamdb
```
Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости:

   ```
   python3 -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

