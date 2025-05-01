# Django Deployment on AWS EC2: Step-by-Step Guide

This guide will walk you step-by-step through deploying a Django application on an AWS EC2 instance using Nginx and Gunicorn.

---

## Prerequisites
- AWS EC2 instance running Ubuntu (or similar)
- SSH access to your EC2 instance or EC2 Instance Connection
- Your Django project in a Git repository
- (Optional) Domain name pointed to your EC2 public IP

---

## 1. Update Server & Install Dependencies
Update your package list and install required packages:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv git nginx npm -y
```

## 2. Set Permissions (if needed)
Add your user to the `www-data` group so Nginx can access your files:
```bash
sudo gpasswd -a www-data ubuntu
```

## 3. Clone Your Django Project
```bash
git clone https://github.com/stevillis/stevillis-blog.git
cd stevillis-blog/
```

## 4. Set Up Python Virtual Environment
```bash
python3 -m venv venv_stevillis_blog
source venv_stevillis_blog/bin/activate
```

## 5. Install Python Requirements
```bash
pip install -r requirements.txt
```

## 6. Configure Django ALLOWED_HOSTS and TinyMCE
Edit `app/settings.py` on your local machine or server, and add your EC2 public IP (and domain if any):
```python
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "<YOUR_EC2_PUBLIC_IP>", "<YOUR_DOMAIN>"]

# TinyMCE
TINYMCE_JS_URL = 'https://cdn.tiny.cloud/1/API_KEY/tinymce/6/tinymce.min.js'
TINYMCE_COMPRESSOR = False
```
Replace `API_KEY` with your TinyMCE API key. Don't forget to add your public IP and domain to Approved Domains in Tiny Cloud.

Commit and push changes if editing locally:
```bash
git add app/settings.py
git commit -m "Add EC2 IP/domain to ALLOWED_HOSTS"
git push
```
Then pull on your server:
```bash
git pull
```

## 7. Build Frontend (if using Django-Tailwind)
If your project uses Tailwind CSS:
```bash
cd theme/static_src/
npm install
npm run build
cd ../../
```

## 8. Collect Static Files
```bash
python manage.py collectstatic
```

## 9. Configure Nginx as a Reverse Proxy
Create a new Nginx site config:
```bash
sudo nano /etc/nginx/sites-available/django_app
```
Paste the following (replace `YOUR_DOMAIN_OR_IP` and paths as needed):
```nginx
server {
    listen 80;
    server_name YOUR_DOMAIN_OR_IP;

    access_log /var/log/nginx/django_access.log;
    error_log /var/log/nginx/django_error.log;

    location /static/ {
        alias /home/ubuntu/stevillis-blog/staticfiles/;
    }
    location /media/ {
        alias /home/ubuntu/stevillis-blog/media/;
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
Enable the config and test:
```bash
sudo ln -s /etc/nginx/sites-available/django_app /etc/nginx/sites-enabled/
sudo nginx -t
```
Restart Nginx:
```bash
sudo systemctl restart nginx
sudo systemctl enable nginx
sudo systemctl status nginx
```

## 10. Configure Gunicorn with systemd
Create a Gunicorn service file:
```bash
sudo nano /etc/systemd/system/django_app.service
```
Paste the following (edit paths and environment variables as needed):
```ini
[Unit]
Description=Gunicorn instance for django app
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/stevillis-blog
ExecStart=/home/ubuntu/stevillis-blog/venv_stevillis_blog/bin/gunicorn -w 3 --bind localhost:8000 app.wsgi:application
Restart=always

Environment="DB_NAME=DB_NAME"
Environment="DB_USER=DB_USER"
Environment="DB_PASSWORD=DB_PASSWORD"
Environment="DB_HOST=DB_HOST"
Environment="DB_PORT=DB_PORT"

[Install]
WantedBy=multi-user.target
```
Reload systemd and start Gunicorn:
```bash
sudo systemctl daemon-reload
sudo systemctl start django_app
sudo systemctl enable django_app
sudo systemctl status django_app
```

## 11. Apply Database Migrations
Now that your environment variables are loaded by the Gunicorn service, run:
```bash
python manage.py migrate
```

## 12. Reload & Restart Services After Changes
Whenever you update code or configuration:
```bash
sudo systemctl daemon-reload
sudo systemctl restart django_app
sudo systemctl restart nginx
```

## 13. Secure Your Site with SSL (Let's Encrypt)
Install Certbot and obtain a certificate:
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx
```
Follow prompts to secure your domain.

---

## Verification & Troubleshooting
- Visit `http://YOUR_DOMAIN_OR_IP` to verify your app is running.
- Check Gunicorn: `sudo systemctl status django_app`
- Check Nginx: `sudo systemctl status nginx`
- Check logs: `/var/log/nginx/django_access.log` and `/var/log/nginx/django_error.log`

If you encounter issues, restart services and review error logs.

---

Congratulations! Your Django app should now be live on AWS EC2 with Nginx and Gunicorn.
