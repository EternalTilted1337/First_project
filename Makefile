POETRY = poetry

.PHONY: run install migrate makemigrations

install:
	$(POETRY) install

run:
	$(POETRY) run python manage.py runserver

#Миграции
migrate:
	$(POETRY) run python manage.py migrate

makemigrations:
	$(POETRY) run python manage.py makemigrations

#Ruff линтинг
lint:
	$(POETRY) run ruff check
lint-fix:
	$(POETRY) run ruff check . --fix

#Форматирование через Ruff
format:
	$(POETRY) run ruff format .



