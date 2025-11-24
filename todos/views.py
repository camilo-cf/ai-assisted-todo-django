from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Todo

# Create your views here.
class TodoListView(ListView):
    model = Todo
    template_name = "todos/home.html"
    context_object_name = "todos"

    ordering = ["-created_at"]

class TodoCreateView(CreateView):
    model = Todo
    fields = ["title", "description", "due_date", "is_resolved"]
    success_url = reverse_lazy("todo-list")

class TodoUpdateView(UpdateView):
    model = Todo
    fields = ["title", "description", "due_date", "is_resolved"]
    success_url = reverse_lazy("todo-list")

class TodoDeleteView(DeleteView):
    model = Todo
    success_url = reverse_lazy("todo-list")

