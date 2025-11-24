# Django Todo App

A simple, modern Todo application built with Django 5 and Python.

## Features
- Create, Read, Update, and Delete (CRUD) Todos.
- Assign due dates with a date picker.
- Mark todos as resolved.
- Clean, responsive UI.

## Prerequisites
- Python 3.12+
- `uv` (Universal Package Manager)

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd ai-assisted-todo-django
    ```

2.  **Install dependencies:**
    ```bash
    uv sync
    ```

3.  **Run migrations:**
    ```bash
    uv run python manage.py migrate
    ```

4.  **Run the server:**
    ```bash
    uv run python manage.py runserver
    ```

5.  **Access the app:**
    Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

## Running Tests
To run the automated test suite:
```bash
uv run python manage.py test
```
