# Django Project with Pytest Tests

## Описание проекта
Проект представляет собой Django REST API для управления курсами и студентами. 
В проекте реализованы тесты с использованием pytest.

## Технологии
- Python 3.11
- Django 5.2
- Django REST Framework
- Pytest
- Model Bakery
- Django Filter

## Установка и запуск

### 1. Клонировать репозиторий
```bash
git clone https://github.com/Dmitrovskiy134/django-pytest-project.git
cd django-pytest-project

2. Установить зависимости
bash
pip install -r requirements.txt

3. Применить миграции
bash
python manage.py migrate

4. Запустить сервер
bash
python manage.py runserver

Запуск тестов
bash
python -m pytest -v
Результат:

text
collected 7 items
tests/students/test_courses_api.py ....... [100%]
====== 7 passed in 0.22s ======
API Endpoints
Метод	URL	Описание
GET	/api/courses/	Получить список курсов
GET	/api/courses/{id}/	Получить курс по ID
POST	/api/courses/	Создать курс
PUT/PATCH	/api/courses/{id}/	Обновить курс
DELETE	/api/courses/{id}/	Удалить курс


