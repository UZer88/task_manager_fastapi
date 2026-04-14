# Task Manager API

[![CI](https://github.com/UZer88/task_manager_fastapi/actions/workflows/ci.yml/badge.svg)](https://github.com/UZer88/task_manager_fastapi/actions/workflows/ci.yml)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://www.docker.com/)
[![Deployed on Render](https://img.shields.io/badge/deployed%20on-render-blue)](https://task-manager-fastapi-m87d.onrender.com/docs)

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

## Быстрый старт с Docker

```bash
docker-compose up --build
```
После запуска API доступен по адресу: http://localhost:8000/docs

## Локальная установка

```bash
# Клонируйте репозиторий
git clone https://github.com/UZer88/task_manager_fastapi.git
cd task_manager_fastapi

# Создайте виртуальное окружение
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Установите зависимости
pip install -r requirements.txt

# Запустите сервер
uvicorn src.main:app --reload --port 8000
```

## Тестирование
```bash
pytest tests/ -v
```

## Автор
UZer88

