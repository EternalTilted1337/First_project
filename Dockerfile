FROM python:3.12.5-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.2

WORKDIR /app

# Системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    make \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем poetry
RUN pip install "poetry==$POETRY_VERSION"

ENV PATH="/root/.local/bin:$PATH"

# Копируем только poetry-файлы для кеша
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Копируем проект
COPY . .

EXPOSE 8000

CMD ["make", "run"]
