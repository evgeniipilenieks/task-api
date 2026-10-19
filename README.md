\# Task API (FastAPI + MySQL)



REST API для управления задачами. Проект демонстрирует навыки создания бэкенда на Python с использованием современных инструментов.



\## 🛠 Технологии

\- \*\*Python 3.10+\*\*

\- \*\*FastAPI\*\* — веб-фреймворк для создания API.

\- \*\*SQLAlchemy\*\* — ORM для работы с базой данных.

\- \*\*MySQL\*\* — реляционная база данных.

\- \*\*Pydantic\*\* — валидация данных.

\- \*\*Uvicorn\*\* — ASGI-сервер.



\## 🚀 Функционал

Реализован полный цикл \*\*CRUD\*\* (Create, Read, Update, Delete):

\- Создание новой задачи (`POST /tasks`).

\- Получение списка всех задач с возможностью фильтрации по статусу (`GET /tasks?status=new`).

\- Обновление существующей задачи (`PUT /tasks/{id}`).

\- Удаление задачи (`DELETE /tasks/{id}`).



\## ⚙️ Как запустить локально



1\. Клонируйте репозиторий:

&#x20;  ```bash

&#x20;  git clone https://github.com/evgeniipilenieks/task-api.git

&#x20;  cd task-api



2\. Установите зависимости:

pip install fastapi uvicorn sqlalchemy pymysql



3\. Создайте базу данных в MySQL:

CREATE DATABASE fastapi\_db CHARACTER SET utf8mb4 COLLATE utf8mb4\_unicode\_ci;



4\. В файле main.py укажите свой пароль от MySQL в строке DATABASE\_URL.



5\. Запустите сервер:

bash

uvicorn main:app --reload



6\. Откройте интерактивную документацию (Swagger) в браузере:

http://127.0.0.1:8000/docs



📁 Структура проекта

main.py — основной код приложения (модели, эндпоинты, подключение к БД).



.gitignore — файлы, исключенные из Git.

