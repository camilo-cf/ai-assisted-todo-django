from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Todo

# Create your views here.
class TodoListView(ListView):
    model = Todo
    template_name = "todos/home.html"
    context_object_name = "todos"

    ordering = ["-created_at"]

class TodoCreateView(SuccessMessageMixin, CreateView):
    model = Todo
    fields = ["title", "description", "due_date", "is_resolved"]
    success_url = reverse_lazy("todo-list")
    success_message = "Todo '%(title)s' was created successfully."

class TodoUpdateView(SuccessMessageMixin, UpdateView):
    model = Todo
    fields = ["title", "description", "due_date", "is_resolved"]
    success_url = reverse_lazy("todo-list")
    success_message = "Todo '%(title)s' was updated successfully."

class TodoDeleteView(DeleteView):
    model = Todo
    success_url = reverse_lazy("todo-list")
    success_message = "Todo was deleted successfully."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
