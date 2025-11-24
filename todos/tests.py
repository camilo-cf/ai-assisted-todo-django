from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Todo
from .forms import TodoForm

class TodoModelTest(TestCase):
    def test_todo_creation(self):
        """Test basic todo creation"""
        todo = Todo.objects.create(title="Test Todo", description="Test Description")
        self.assertEqual(todo.title, "Test Todo")
        self.assertEqual(todo.description, "Test Description")
        self.assertFalse(todo.is_resolved)
        self.assertTrue(isinstance(todo, Todo))
        self.assertEqual(str(todo), "Test Todo")
    
    def test_is_overdue(self):
        """Test is_overdue method"""
        # Past due date, not resolved
        past_todo = Todo.objects.create(
            title="Overdue Todo",
            due_date=timezone.now() - timedelta(days=1)
        )
        self.assertTrue(past_todo.is_overdue())
        
        # Future due date
        future_todo = Todo.objects.create(
            title="Future Todo",
            due_date=timezone.now() + timedelta(days=1)
        )
        self.assertFalse(future_todo.is_overdue())
        
        # Past but resolved
        resolved_todo = Todo.objects.create(
            title="Resolved Todo",
            due_date=timezone.now() - timedelta(days=1),
            is_resolved=True
        )
        self.assertFalse(resolved_todo.is_overdue())
        
        # No due date
        no_date_todo = Todo.objects.create(title="No Date")
        self.assertFalse(no_date_todo.is_overdue())
    
    def test_mark_resolved(self):
        """Test mark_resolved method"""
        todo = Todo.objects.create(title="Test")
        self.assertFalse(todo.is_resolved)
        todo.mark_resolved()
        self.assertTrue(todo.is_resolved)
    
    def test_mark_unresolved(self):
        """Test mark_unresolved method"""
        todo = Todo.objects.create(title="Test", is_resolved=True)
        self.assertTrue(todo.is_resolved)
        todo.mark_unresolved()
        self.assertFalse(todo.is_resolved)
    
    def test_ordering(self):
        """Test that todos are ordered by created_at descending"""
        old_todo = Todo.objects.create(title="Old")
        new_todo = Todo.objects.create(title="New")
        todos = list(Todo.objects.all())
        self.assertEqual(todos[0], new_todo)
        self.assertEqual(todos[1], old_todo)

class TodoFormTest(TestCase):
    def test_valid_form(self):
        """Test form with valid data"""
        form_data = {
            'title': 'Test Todo',
            'description': 'Test Description',
            'due_date': (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M'),
        }
        form = TodoForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_past_due_date_validation(self):
        """Test that past due dates are rejected for new todos"""
        form_data = {
            'title': 'Test Todo',
            'due_date': (timezone.now() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M'),
        }
        form = TodoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('due_date', form.errors)
    
    def test_empty_title_validation(self):
        """Test that title is required"""
        form_data = {'description': 'Test'}
        form = TodoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

class TodoViewTest(TestCase):
    def setUp(self):
        self.todo = Todo.objects.create(title="Test Todo")

    def test_todo_list_view(self):
        """Test list view displays todos"""
        response = self.client.get(reverse("todo-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todos/home.html")
        self.assertContains(response, "Test Todo")
    
    def test_todo_list_view_statistics(self):
        """Test that statistics are displayed"""
        Todo.objects.create(title="Completed", is_resolved=True)
        response = self.client.get(reverse("todo-list"))
        self.assertIn('total_todos', response.context)
        self.assertIn('completed_todos', response.context)
        self.assertIn('pending_todos', response.context)
        self.assertEqual(response.context['total_todos'], 2)
        self.assertEqual(response.context['completed_todos'], 1)
        self.assertEqual(response.context['pending_todos'], 1)
    
    def test_todo_list_pagination(self):
        """Test pagination works"""
        # Create 15 todos (more than paginate_by=10)
        for i in range(15):
            Todo.objects.create(title=f"Todo {i}")
        response = self.client.get(reverse("todo-list"))
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['todos']), 10)

    def test_todo_create_view(self):
        """Test creating a new todo"""
        response = self.client.post(reverse("todo-create"), {
            "title": "New Todo",
            "description": "New Description"
        })
        self.assertEqual(response.status_code, 302) # Redirects
        self.assertEqual(Todo.objects.count(), 2)
        # With ordering by -created_at, newest todo is first
        self.assertEqual(Todo.objects.first().title, "New Todo")


    def test_todo_update_view(self):
        """Test updating an existing todo"""
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
        """Test deleting a todo"""
        response = self.client.post(reverse("todo-delete", args=[self.todo.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 0)
    
    def test_404_for_nonexistent_todo(self):
        """Test that accessing non-existent todo returns 404"""
        response = self.client.get(reverse("todo-update", args=[9999]))
        self.assertEqual(response.status_code, 404)
