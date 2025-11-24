from django.test import TestCase
from django.urls import reverse
from .models import Todo

class TodoModelTest(TestCase):
    def test_todo_creation(self):
        todo = Todo.objects.create(title="Test Todo", description="Test Description")
        self.assertEqual(todo.title, "Test Todo")
        self.assertEqual(todo.description, "Test Description")
        self.assertFalse(todo.is_resolved)
        self.assertTrue(isinstance(todo, Todo))
        self.assertEqual(str(todo), "Test Todo")

class TodoViewTest(TestCase):
    def setUp(self):
        self.todo = Todo.objects.create(title="Test Todo")

    def test_todo_list_view(self):
        response = self.client.get(reverse("todo-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todos/home.html")
        self.assertContains(response, "Test Todo")

    def test_todo_create_view(self):
        response = self.client.post(reverse("todo-create"), {
            "title": "New Todo",
            "description": "New Description"
        })
        self.assertEqual(response.status_code, 302) # Redirects
        self.assertEqual(Todo.objects.count(), 2)
        self.assertEqual(Todo.objects.last().title, "New Todo")

    def test_todo_update_view(self):
        response = self.client.post(reverse("todo-update", args=[self.todo.pk]), {
            "title": "Updated Todo",
            "description": "Updated Description",
            "is_resolved": True
        })
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, "Updated Todo")
        self.assertTrue(self.todo.is_resolved)

    def test_todo_delete_view(self):
        response = self.client.post(reverse("todo-delete", args=[self.todo.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 0)
