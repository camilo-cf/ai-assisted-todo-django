from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["title", "description", "due_date", "is_resolved"]
        widgets = {
            "due_date": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }
