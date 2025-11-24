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

## 📚 Documentation

This project includes comprehensive documentation for all skill levels:

- **[DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md)** - Complete development walkthrough
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System diagrams and architecture explanations
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deploy to Raspberry Pi, cloud services, or self-hosted servers
- **[LEARNING_PATH.md](LEARNING_PATH.md)** - Zero to hero learning guide
- **[SECURITY.md](SECURITY.md)** - Security best practices and production checklist

## 🎯 Features

- ✅ Create, edit, and delete todos
- ✅ Assign due dates with date picker
- ✅ Mark todos as resolved
- ✅ Status badges (Resolved/Pending)
- ✅ Modern, responsive UI
- ✅ Success messages for user actions
- ✅ Full test coverage

## 🚀 Quick Start for Beginners

New to Django? Start here:
1. Read [LEARNING_PATH.md](LEARNING_PATH.md) - Start with "Complete Beginner"
2. Follow [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md) - Understand how it was built
3. Check [ARCHITECTURE.md](ARCHITECTURE.md) - See visual diagrams

## 🌐 Deployment

Ready to deploy? We've got you covered:
- **Self-hosted**: [Raspberry Pi guide](DEPLOYMENT.md#self-hosted-deployment-raspberry-pi)
- **Cloud**: [Railway, Render, DigitalOcean, Heroku](DEPLOYMENT.md#cloud-deployment-options)

## 🤝 Contributing

This is a learning project! Feel free to:
- Add new features
- Improve documentation
- Fix bugs
- Share your learnings

## 📝 License

MIT License - feel free to use this project for learning!

