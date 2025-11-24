# Security & Production Deployment Guide

## Security Checklist

### Before Deploying to Production

1. **Environment Variables**
   ```python
   # In settings.py, use environment variables:
   import os
   SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
   DEBUG = os.environ.get('DEBUG', 'False') == 'True'
   ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
   ```

2. **Django Security Settings**
   - Set `DEBUG = False` in production
   - Configure `ALLOWED_HOSTS` with your domain
   - Use HTTPS and set `SECURE_SSL_REDIRECT = True`
   - Enable `SESSION_COOKIE_SECURE = True`
   - Enable `CSRF_COOKIE_SECURE = True`
   - Set `SECURE_HSTS_SECONDS = 31536000` (1 year)

3. **Database**
   - Use PostgreSQL or MySQL in production (not SQLite)
   - Keep database credentials in environment variables
   - Enable connection pooling

4. **Static Files**
   ```python
   STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
   ```
   Run `python manage.py collectstatic` before deployment

5. **Dependencies**
   - Keep dependencies up to date: `uv sync --upgrade`
   - Review security advisories regularly

## Production Deployment Options

### Option 1: Platform-as-a-Service (Easiest)
- **Heroku**: Simple `git push` deployment
- **Railway**: Free tier, automatic deployments
- **Render**: PostgreSQL included

### Option 2: VPS (More Control)
- Use **Gunicorn** as WSGI server
- **Nginx** as reverse proxy
- **Supervisor** for process management
- **PostgreSQL** database

### Quick Production Setup Example

1. Install production dependencies:
   ```bash
   uv add gunicorn psycopg2-binary
   ```

2. Create `Procfile` (for Heroku/Railway):
   ```
   web: gunicorn config.wsgi --log-file -
   ```

3. Update `settings.py` for production:
   ```python
   import dj_database_url
   
   DATABASES = {
       'default': dj_database_url.config(
           default='sqlite:///db.sqlite3',
           conn_max_age=600
       )
   }
   ```

## Security Notes

- **Never commit** `SECRET_KEY` or sensitive credentials
- Use `.env` files for local development (add to `.gitignore`)
- Regularly run `python manage.py check --deploy`
- Enable Django security middleware (already configured)
- Keep Django and dependencies updated

## Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Security Middleware](https://docs.djangoproject.com/en/stable/ref/middleware/#module-django.middleware.security)
