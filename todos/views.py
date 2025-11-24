from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Todo
from .forms import TodoForm

# Create your views here.
class TodoListView(ListView):
    """Display a list of all todos, ordered by creation date (newest first)."""
    model = Todo
    template_name = "todos/home.html"
    context_object_name = "todos"
    paginate_by = 10  # Show 10 todos per page
    ordering = ["-created_at"]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add statistics
        context['total_todos'] = Todo.objects.count()
        context['completed_todos'] = Todo.objects.filter(is_resolved=True).count()
        context['pending_todos'] = Todo.objects.filter(is_resolved=False).count()
        return context


class TodoCreateView(SuccessMessageMixin, CreateView):
    """Handle creation of new todo items with success message."""
    model = Todo
    form_class = TodoForm
    success_url = reverse_lazy("todo-list")
    success_message = "Todo '%(title)s' was created successfully."

class TodoUpdateView(SuccessMessageMixin, UpdateView):
    """Handle updating existing todo items with success message."""
    model = Todo
    form_class = TodoForm
    success_url = reverse_lazy("todo-list")
    success_message = "Todo '%(title)s' was updated successfully."

class TodoDeleteView(DeleteView):
    """Handle deletion of todo items with confirmation and success message."""
    model = Todo
    success_url = reverse_lazy("todo-list")
    success_message = "Todo was deleted successfully."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
