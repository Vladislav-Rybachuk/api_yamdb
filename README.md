# API_YAMDB

[![Python](https://img.shields.io/badge/-Python-464641?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-464646?style=flat-square&logo=django)](https://www.djangoproject.com/)
[![Pytest](https://img.shields.io/badge/Pytest-464646?style=flat-square&logo=pytest)](https://docs.pytest.org/en/6.2.x/)
[![Postman](https://img.shields.io/badge/Postman-464646?style=flat-square&logo=postman)](https://www.postman.com/)

# Description

The YaMDb project collects user feedback on titles.
The titles are divided into categories such as "Books", "Films", "Music".
A title can be assigned a genre from the preset list.
Users leave text reviews for titles and rate the title in the range from one to ten.
Users can leave comments on reviews.

# User categories

Users are divided into 5 categories:

- SuperUser
- Admin
- Moderator
- User (the category is assigned to all new users)
- UnauthUser

# User rights

**UnauthUser:**
* View descriptions of titles, read reviews and comments.
    
**User:** 
* View descriptions of titles, read reviews and comments.
* Publication of reviews, comments.
* Editing / deleting your reviews / comments.
    
**Moderator:**
* View descriptions of titles, read reviews and comments.
* Publication of reviews, comments.
* Edit/delete ALL reviews/comments.

**SuperUser/Admin:**
* Full rights to all actions.

# Installation:

Clone the repository and change into it on the command line:

```
git clone https://github.com/Vladislav-Rybachuk/api_yamdb.git
```

```
cd api_yamdb
```
Create and activate virtual environment:

```
python -m venv env
```

* If you have Linux/macOS

    ```
    source env/bin/activate
    ```

* If you have windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Install dependencies:

   ```
   python3 -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

Run migrations:

```
python3 manage.py migrate
```

Run project:

```
python3 manage.py runserver
```

