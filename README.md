# Hotel Booking API Project

Бэкенд-сервис для управления номерами и бронированиями отеля, разработанный на Django REST Framework (DRF) и PostgreSQL.
Готовый образ доступен на Docker Hub.

---

# Стек технологий

**Бэкенд: Python, Django, Django REST Framework.**

**База данных: PostgreSQL.**

**Контейнеризация: Docker и Docker Compose.**

**Docker Hub Image: pr1me1337/first_project**

---

# Начало:

1)Скопировать репозирий
``git clone https://github.com/EternalTilted1337/First_project.git``

2)Проверка docker-compose.yml: Убедитесь, что ваш docker-compose.yml использует ваш опубликованный образ. Если он сейчас
настроен на сборку (build: .), замените это на image:

## Фрагмент docker-compose.yml

```services:
  hotel-django:
    image: pr1me1337/first_project:latest 
    container_name: hotel-django
    ports:
      - "8000:8000"
    depends_on:
      - db
    # ... остальные настройки ...
```

3)Запустить контейнеры по образу
``docker-compose up -d``

4)Миграции
Применить миграцию базы данных

``docker-compose exec hotel-django python manage.py migrate``

Создать суперпользователя

```docker-compose exec hotel-django python manage.py createsuperuser```

--- 

# Карта эндпоинтов

z`

## Управление номерами

**Просмотр номера**
GET

/api/rooms/

---

**Создать новый номер**
POST

/api/rooms/ - обязательно требуется верный JSON

Пример JSON
``{
    "description" : "СЮДАИМЯ",
    "price" : СЮДАЛАВЕХУ
}
``
---
**Удалить номер по ID (DELETE)**

/api/rooms/{id}/

---

## Управление бронью

Получить список бронирований для конкретного номера.

GET

/api/bookings/?room_id={id}

---
Создать новое бронирование

POST

/api/bookings/

---

Удалить бронь по ID.

DELETE

/api/bookings/{id}/

Перед эндпоинтом "http://127.0.0.1:8000" 