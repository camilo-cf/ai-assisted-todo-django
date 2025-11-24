from django.db import models

# Create your models here.
class Todo(models.Model):
    """
    Model representing a Todo item.
    
    Attributes:
        title: Short description of the todo (required)
        description: Detailed description (optional)
        due_date: When the todo should be completed (optional)
        is_resolved: Whether the todo has been completed
        created_at: When the todo was created
        updated_at: When the todo was last modified
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return the title of the todo."""
        return self.title


