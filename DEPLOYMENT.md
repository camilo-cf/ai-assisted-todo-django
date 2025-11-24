# Django Todo App - Deployment Guide

## Table of Contents
1. [Self-Hosted Deployment (Raspberry Pi)](#self-hosted-deployment-raspberry-pi)
2. [Cloud Deployment Options](#cloud-deployment-options)
3. [Production Checklist](#production-checklist)
4. [Troubleshooting](#troubleshooting)

---

## Self-Hosted Deployment (Raspberry Pi)

### Prerequisites
- Raspberry Pi (3, 4, or 5 recommended)
- Raspberry Pi OS (64-bit recommended)
- Internet connection
- Domain name (optional, for HTTPS)

### Step 1: Prepare Your Raspberry Pi

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11+ and dependencies
sudo apt install python3 python3-pip python3-venv nginx supervisor -y

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env
```

### Step 2: Clone and Setup the Project

```bash
# Create app directory
sudo mkdir -p /var/www/todo-app
sudo chown $USER:$USER /var/www/todo-app
cd /var/www/todo-app

# Clone your repository
git clone https://github.com/YOUR_USERNAME/ai-assisted-todo-django.git .

# Install dependencies
uv sync

# Install production server
uv add gunicorn
```

### Step 3: Configure Environment Variables

```bash
# Create .env file
cat > .env << 'EOF'
DJANGO_SECRET_KEY=your-super-secret-key-here-change-this
DEBUG=False
ALLOWED_HOSTS=your-pi-ip-address,your-domain.com
DATABASE_URL=sqlite:///db.sqlite3
EOF

# Update settings.py to use environment variables
```

### Step 4: Prepare for Production

```bash
# Collect static files
uv run python manage.py collectstatic --noinput

# Run migrations
uv run python manage.py migrate

# Create superuser
uv run python manage.py createsuperuser
```

### Step 5: Configure Gunicorn

Create `/var/www/todo-app/gunicorn_config.py`:

```python
bind = "127.0.0.1:8000"
workers = 2  # For Raspberry Pi, keep this low
worker_class = "sync"
timeout = 120
accesslog = "/var/www/todo-app/logs/gunicorn-access.log"
errorlog = "/var/www/todo-app/logs/gunicorn-error.log"
loglevel = "info"
```

Create log directory:
```bash
mkdir -p /var/www/todo-app/logs
```

### Step 6: Configure Supervisor

Create `/etc/supervisor/conf.d/todo-app.conf`:

```ini
[program:todo-app]
directory=/var/www/todo-app
command=/var/www/todo-app/.venv/bin/gunicorn config.wsgi:application -c gunicorn_config.py
user=YOUR_USERNAME
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/www/todo-app/logs/supervisor.log
```

Start the service:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start todo-app
```

### Step 7: Configure Nginx

Create `/etc/nginx/sites-available/todo-app`:

```nginx
server {
    listen 80;
    server_name your-pi-ip-address your-domain.com;

    client_max_body_size 10M;

    location /static/ {
        alias /var/www/todo-app/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/todo-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 8: Enable HTTPS (Optional but Recommended)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is configured automatically
```

### Raspberry Pi Optimization Tips

1. **Use SQLite for small deployments** (up to ~100 concurrent users)
2. **Limit Gunicorn workers** to 2-3 on Raspberry Pi
3. **Enable swap** if you have limited RAM:
   ```bash
   sudo dphys-swapfile swapoff
   sudo nano /etc/dphys-swapfile  # Set CONF_SWAPSIZE=1024
   sudo dphys-swapfile setup
   sudo dphys-swapfile swapon
   ```
4. **Use a USB SSD** instead of SD card for better performance

---

## Cloud Deployment Options

### Option 1: Railway (Easiest)

**Cost**: Free tier available, then ~$5/month

**Steps**:
1. Push your code to GitHub
2. Go to [railway.app](https://railway.app)
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-detects Django and deploys!

**Configuration**:
- Add environment variables in Railway dashboard:
  - `DJANGO_SECRET_KEY`
  - `ALLOWED_HOSTS`
- Railway provides PostgreSQL for free

### Option 2: Render

**Cost**: Free tier available (with limitations)

**Steps**:
1. Create `render.yaml` in your project root:

```yaml
services:
  - type: web
    name: todo-app
    env: python
    buildCommand: "uv sync && uv run python manage.py collectstatic --noinput && uv run python manage.py migrate"
    startCommand: "uv run gunicorn config.wsgi:application"
    envVars:
      - key: DJANGO_SECRET_KEY
        generateValue: true
      - key: PYTHON_VERSION
        value: 3.11
      - key: DATABASE_URL
        fromDatabase:
          name: todo-db
          property: connectionString

databases:
  - name: todo-db
    databaseName: todo_app
    user: todo_user
```

2. Push to GitHub
3. Connect repository on [render.com](https://render.com)

### Option 3: DigitalOcean App Platform

**Cost**: $5/month minimum

**Steps**:
1. Create `app.yaml`:

```yaml
name: todo-app
services:
- name: web
  github:
    repo: YOUR_USERNAME/ai-assisted-todo-django
    branch: main
  build_command: uv sync && uv run python manage.py collectstatic --noinput
  run_command: uv run gunicorn config.wsgi:application
  envs:
  - key: DJANGO_SECRET_KEY
    scope: RUN_TIME
    type: SECRET
  - key: DATABASE_URL
    scope: RUN_TIME
    type: SECRET

databases:
- name: db
  engine: PG
  version: "15"
```

2. Deploy via DigitalOcean dashboard

### Option 4: Heroku

**Cost**: $5-7/month (no free tier anymore)

**Steps**:
1. Install Heroku CLI
2. Create `Procfile`:
   ```
   web: gunicorn config.wsgi --log-file -
   ```
3. Create `runtime.txt`:
   ```
   python-3.11.0
   ```
4. Deploy:
   ```bash
   heroku create your-app-name
   heroku addons:create heroku-postgresql:mini
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

### Option 5: AWS EC2 (Advanced)

**Cost**: ~$3-10/month (t2.micro/t3.micro)

Similar to Raspberry Pi setup, but:
- Use Ubuntu 22.04 LTS
- Configure security groups (ports 80, 443, 22)
- Use RDS for PostgreSQL (optional)
- Consider using AWS Elastic Beanstalk for easier management

---

## Production Checklist

### Security
- [ ] `DEBUG = False` in production
- [ ] Strong `SECRET_KEY` (use environment variable)
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Enable HTTPS/SSL
- [ ] Set `SECURE_SSL_REDIRECT = True`
- [ ] Set `SESSION_COOKIE_SECURE = True`
- [ ] Set `CSRF_COOKIE_SECURE = True`
- [ ] Set `SECURE_HSTS_SECONDS = 31536000`
- [ ] Use PostgreSQL instead of SQLite (for production)

### Performance
- [ ] Run `collectstatic` for static files
- [ ] Configure static file serving (Nginx/Whitenoise)
- [ ] Enable database connection pooling
- [ ] Set up caching (Redis/Memcached)
- [ ] Configure logging

### Monitoring
- [ ] Set up error tracking (Sentry)
- [ ] Configure uptime monitoring
- [ ] Set up log aggregation
- [ ] Monitor resource usage

### Backup
- [ ] Automated database backups
- [ ] Backup media files
- [ ] Test restore procedures

---

## Troubleshooting

### Common Issues

**Issue**: "Bad Request (400)"
- **Solution**: Add your domain/IP to `ALLOWED_HOSTS`

**Issue**: Static files not loading
- **Solution**: Run `python manage.py collectstatic` and configure Nginx/Whitenoise

**Issue**: Database connection errors
- **Solution**: Check `DATABASE_URL` environment variable

**Issue**: Gunicorn won't start
- **Solution**: Check logs in `/var/www/todo-app/logs/` and verify Python path

**Issue**: Nginx 502 Bad Gateway
- **Solution**: Ensure Gunicorn is running (`sudo supervisorctl status`)

### Useful Commands

```bash
# Check Gunicorn status
sudo supervisorctl status todo-app

# Restart application
sudo supervisorctl restart todo-app

# View logs
tail -f /var/www/todo-app/logs/gunicorn-error.log

# Test Nginx configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx

# Check if port 8000 is listening
sudo netstat -tlnp | grep 8000
```

---

## Comparison: Self-Hosted vs Cloud

| Feature | Raspberry Pi | Railway | Render | DigitalOcean |
|---------|-------------|---------|--------|--------------|
| **Cost** | $0/month (after hardware) | $5/month | Free tier available | $5/month |
| **Setup Difficulty** | Medium | Very Easy | Easy | Medium |
| **Scalability** | Limited | Excellent | Good | Excellent |
| **Control** | Full | Limited | Limited | Full |
| **Maintenance** | You | Them | Them | You |
| **Best For** | Learning, home use | Quick deploys | Side projects | Production apps |

---

## Next Steps After Deployment

1. **Set up monitoring**: Use tools like UptimeRobot or Pingdom
2. **Configure backups**: Automate database backups
3. **Add custom domain**: Point your domain to your server
4. **Set up CI/CD**: Automate deployments with GitHub Actions
5. **Scale as needed**: Add more workers, upgrade server, or add caching

Happy deploying! 🚀
