# Task Manager API

REST API для управления задачами с аутентификацией. Проект для изучения FastAPI, SQLAlchemy и JWT.

## Возможности

- Регистрация и аутентификация (JWT)
- CRUD операции с задачами
- Фильтрация задач по статусу, приоритету и тегам
- Поддержка тегов (многие ко многим)
- SQLite (можно легко заменить на PostgreSQL)

## Технологии

- FastAPI
- SQLAlchemy 2.0 (async)
- SQLite (aiosqlite)
- Pydantic
- python-jose (JWT)
- passlib (bcrypt)

## Установка и запуск

```bash
# Клонируйте репозиторий
git clone https://github.com/UZer88/task_manager_fastapi.git
cd task_manager_fastapi
```

## Создайте виртуальное окружение
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
```

## Установите зависимости
```bash
pip install -r requirements.txt
```

## Запустите сервер
```bash
uvicorn src.main:app --reload --port 8000
```

## API Документация
После запуска откройте http://localhost:8000/docs

## Автор
UZer88

