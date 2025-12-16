

.PHONY: run install migrate makemigrations lint lint-fix format


install:
	poetry install

run:
	python manage.py makemigrations --no-input --merge
	python manage.py migrate --no-input
	python manage.py runserver 0.0.0.0:8000

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

lint:
	ruff check

lint-fix:
	ruff check . --fix

format:
	ruff format .