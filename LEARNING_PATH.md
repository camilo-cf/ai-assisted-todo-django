# Learning Path: Zero to Hero

## 🎯 Your Journey to Django Mastery

This guide will take you from complete beginner to confident Django developer. Follow the path that matches your current level!

---

## 📚 Table of Contents

1. [Complete Beginner (5-Year-Old Level)](#complete-beginner-5-year-old-level)
2. [Novice Programmer](#novice-programmer)
3. [Intermediate Developer](#intermediate-developer)
4. [Advanced Topics](#advanced-topics)
5. [Learning Resources](#learning-resources)

---

## Complete Beginner (5-Year-Old Level)

### What is a Website?

**Simple Explanation**: A website is like a digital book that lives on the internet. When you type an address (like `google.com`), your computer asks another computer (a server) to send you that book's pages.

**Our Todo App**: It's like a digital notebook where you can write down things you need to do, check them off when done, and see them anytime from any computer!

### How Does It Work?

```
You (Browser) → "Can I see my todos?" → Server (Our App)
Server → "Here they are!" → Sends HTML page → You see pretty todos!
```

### Key Concepts (ELI5)

**1. Frontend (What You See)**
- Like the cover and pages of a book
- HTML = The words and pictures
- CSS = The colors and decorations
- JavaScript = The interactive parts (buttons that do things)

**2. Backend (The Brain)**
- Like the author writing the book
- Python/Django = The language the author speaks
- Database = The filing cabinet where we store todos

**3. Server (The Library)**
- A computer that's always on, waiting to send pages
- Like a library that never closes

### Your First Steps

**Week 1: Understanding the Basics**
1. Open the app in your browser
2. Create a todo - see what happens!
3. Edit it - notice the form?
4. Delete it - see the confirmation?
5. Look at the URL bar - see how it changes?

**Week 2: Peek Behind the Curtain**
1. Open `todos/templates/todos/home.html`
2. Find where it says "My Todos" - that's HTML!
3. Change it to "My Awesome Todos"
4. Refresh the page - you just edited a website!

**Week 3: Understanding Data**
1. Create 3 todos
2. Open `db.sqlite3` with DB Browser for SQLite
3. See your todos stored as rows in a table!
4. This is how websites remember things

---

## Novice Programmer

### Prerequisites
- Basic Python knowledge (variables, functions, loops)
- Understanding of HTML/CSS
- Comfortable with command line

### Week-by-Week Learning Plan

#### Week 1-2: Django Fundamentals

**Concepts to Master**:
- MVT Architecture (Model-View-Template)
- URL routing
- Django ORM basics
- Template language

**Exercises**:
1. **Add a new field to Todo**:
   ```python
   # In todos/models.py
   priority = models.CharField(max_length=10, choices=[
       ('low', 'Low'),
       ('medium', 'Medium'),
       ('high', 'High'),
   ], default='medium')
   ```
   - Run `makemigrations` and `migrate`
   - Update forms and templates

2. **Create a "Completed Todos" page**:
   - New URL: `/completed/`
   - New view: Filter `is_resolved=True`
   - New template: Show only completed todos

3. **Add a search feature**:
   ```python
   # In views.py
   def get_queryset(self):
       queryset = super().get_queryset()
       search = self.request.GET.get('search')
       if search:
           queryset = queryset.filter(title__icontains=search)
       return queryset
   ```

#### Week 3-4: Forms and Validation

**Concepts**:
- Django Forms vs ModelForms
- Form validation
- Custom clean methods
- Form widgets

**Exercises**:
1. **Add custom validation**:
   ```python
   def clean_title(self):
       title = self.cleaned_data['title']
       if len(title) < 3:
           raise ValidationError("Title must be at least 3 characters")
       return title
   ```

2. **Create a bulk-add feature**:
   - Form with textarea
   - Each line becomes a todo
   - Use `formsets` for multiple items

#### Week 5-6: Authentication

**Concepts**:
- User model
- Login/Logout views
- Permission decorators
- User-specific data

**Exercises**:
1. **Add user authentication**:
   ```python
   # Add to models.py
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   
   # In views.py
   from django.contrib.auth.mixins import LoginRequiredMixin
   
   class TodoListView(LoginRequiredMixin, ListView):
       def get_queryset(self):
           return Todo.objects.filter(user=self.request.user)
   ```

2. **Create registration page**:
   - Use `UserCreationForm`
   - Add email field
   - Send welcome email

#### Week 7-8: Testing and Quality

**Concepts**:
- Unit tests
- Integration tests
- Test coverage
- Continuous Integration

**Exercises**:
1. **Improve test coverage**:
   ```python
   def test_todo_ordering(self):
       """Todos should be ordered by created_at descending"""
       old_todo = Todo.objects.create(title="Old")
       new_todo = Todo.objects.create(title="New")
       response = self.client.get(reverse('todo-list'))
       todos = response.context['todos']
       self.assertEqual(todos[0], new_todo)
   ```

2. **Add form tests**:
   - Test validation rules
   - Test error messages
   - Test success cases

---

## Intermediate Developer

### Prerequisites
- Completed novice section
- Comfortable with Django basics
- Understanding of databases and SQL

### Advanced Features to Implement

#### 1. Categories and Tags

```python
class Category(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7)  # Hex color
    
class Todo(models.Model):
    # ... existing fields
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField('Tag', blank=True)
```

**Learning Goals**:
- Foreign Keys
- Many-to-Many relationships
- Related object queries

#### 2. API with Django REST Framework

```bash
uv add djangorestframework
```

```python
# todos/serializers.py
from rest_framework import serializers

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'

# todos/api_views.py
from rest_framework import viewsets

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
```

**Learning Goals**:
- RESTful APIs
- Serializers
- ViewSets
- API authentication

#### 3. Real-time Updates with Channels

```bash
uv add channels channels-redis
```

**Learning Goals**:
- WebSockets
- Async Django
- Redis integration
- Real-time features

#### 4. Advanced Querying

```python
from django.db.models import Q, Count, Avg
from django.db.models.functions import TruncDate

# Complex queries
overdue_todos = Todo.objects.filter(
    Q(due_date__lt=timezone.now()) & Q(is_resolved=False)
)

# Aggregation
stats = Todo.objects.aggregate(
    total=Count('id'),
    completed=Count('id', filter=Q(is_resolved=True)),
    avg_per_day=Count('id') / 30
)

# Group by date
todos_by_date = Todo.objects.annotate(
    date=TruncDate('created_at')
).values('date').annotate(count=Count('id'))
```

---

## Advanced Topics

### 1. Performance Optimization

**Database Optimization**:
```python
# Use select_related for foreign keys
todos = Todo.objects.select_related('user', 'category').all()

# Use prefetch_related for many-to-many
todos = Todo.objects.prefetch_related('tags').all()

# Add database indexes
class Meta:
    indexes = [
        models.Index(fields=['created_at']),
        models.Index(fields=['user', 'is_resolved']),
    ]
```

**Caching**:
```python
from django.core.cache import cache

def get_user_todos(user_id):
    cache_key = f'user_todos_{user_id}'
    todos = cache.get(cache_key)
    if not todos:
        todos = list(Todo.objects.filter(user_id=user_id))
        cache.set(cache_key, todos, 300)  # 5 minutes
    return todos
```

### 2. Celery for Background Tasks

```python
# tasks.py
from celery import shared_task

@shared_task
def send_due_date_reminders():
    tomorrow = timezone.now() + timedelta(days=1)
    todos = Todo.objects.filter(
        due_date__date=tomorrow.date(),
        is_resolved=False
    )
    for todo in todos:
        send_email(todo.user.email, f"Reminder: {todo.title}")
```

### 3. Custom Management Commands

```python
# todos/management/commands/cleanup_old_todos.py
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Delete completed todos older than 30 days'
    
    def handle(self, *args, **options):
        cutoff = timezone.now() - timedelta(days=30)
        deleted = Todo.objects.filter(
            is_resolved=True,
            updated_at__lt=cutoff
        ).delete()
        self.stdout.write(f'Deleted {deleted[0]} todos')
```

### 4. Custom Template Tags

```python
# todos/templatetags/todo_extras.py
from django import template

register = template.Library()

@register.filter
def priority_badge(priority):
    colors = {'low': 'green', 'medium': 'orange', 'high': 'red'}
    return f'<span class="badge-{colors[priority]}">{priority}</span>'
```

---

## Learning Resources

### Official Documentation
- [Django Docs](https://docs.djangoproject.com/) - The best resource
- [Django Tutorial](https://docs.djangoproject.com/en/stable/intro/tutorial01/) - Official tutorial

### Books
1. **"Django for Beginners"** by William S. Vincent
2. **"Two Scoops of Django"** by Daniel and Audrey Roy Greenfeld
3. **"Django for Professionals"** by William S. Vincent

### Online Courses
1. **freeCodeCamp** - Free Django course on YouTube
2. **Django Girls Tutorial** - Beginner-friendly
3. **TestDriven.io** - Advanced Django patterns

### Practice Projects

**Beginner**:
1. Blog with comments
2. Recipe sharing site
3. Bookmark manager

**Intermediate**:
1. Social media clone
2. E-commerce site
3. Project management tool

**Advanced**:
1. Real-time chat application
2. Video streaming platform
3. Multi-tenant SaaS application

---

## Troubleshooting Common Issues

### "No module named 'django'"
**Solution**: Activate virtual environment or run with `uv run`

### "TemplateDoesNotExist"
**Solution**: Check `INSTALLED_APPS` and template directory structure

### "CSRF verification failed"
**Solution**: Ensure `{% csrf_token %}` is in your forms

### "Migrations not applying"
**Solution**: 
```bash
uv run python manage.py migrate --run-syncdb
```

### "Static files not loading"
**Solution**:
```bash
uv run python manage.py collectstatic
```

---

## Next Steps

### After Mastering This App

1. **Add More Features**:
   - Recurring todos
   - Subtasks
   - File attachments
   - Collaboration (share todos)

2. **Learn Related Technologies**:
   - PostgreSQL
   - Redis
   - Docker
   - Kubernetes

3. **Build Your Own Project**:
   - Start with an idea you're passionate about
   - Plan the models and features
   - Build incrementally
   - Deploy and share!

4. **Contribute to Open Source**:
   - Find Django projects on GitHub
   - Fix bugs
   - Add features
   - Learn from code reviews

---

## Milestones and Achievements

Track your progress:

- [ ] **Beginner**: Created first todo
- [ ] **Novice**: Modified a template
- [ ] **Intermediate**: Added a new model field
- [ ] **Advanced**: Implemented authentication
- [ ] **Expert**: Deployed to production
- [ ] **Master**: Built own Django project
- [ ] **Hero**: Contributed to Django or major project

---

## Remember

> "The expert in anything was once a beginner." - Helen Hayes

- **Don't rush** - Take time to understand concepts
- **Build projects** - Learning by doing is most effective
- **Read code** - Study well-written Django projects
- **Ask questions** - Django community is very helpful
- **Have fun** - Enjoy the journey!

Happy coding! 🚀
