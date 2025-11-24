from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Todo

class TodoForm(forms.ModelForm):
    """
    Form for creating and updating Todo items.
    
    Includes custom validation to ensure due dates are not in the past.
    """
    class Meta:
        model = Todo
        fields = ["title", "description", "due_date", "is_resolved"]
        widgets = {
            "due_date": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }
        labels = {
            "title": "Title",
            "description": "Description",
            "due_date": "Due Date & Time",
            "is_resolved": "Mark as resolved",
        }
        help_texts = {
            "title": "Give your todo a short, descriptive name.",
            "description": "Add any additional details or notes.",
            "due_date": "Optionally set a deadline for this todo.",
        }
    
    def clean_due_date(self):
        """Validate that due_date is not in the past (for new todos)."""
        due_date = self.cleaned_data.get('due_date')
       
        if due_date and not self.instance.pk:  # Only check for new todos
            if due_date < timezone.now():
                raise ValidationError("Due date cannot be in the past.")
        
        return due_date

