# Development Guide

A quick reference for common Django project development tasks.

---

## 1. Database Migrations
Apply changes to your models and update the database schema.
```shell
python manage.py makemigrations   # Create migration files from model changes
python manage.py migrate          # Apply migrations to the database
```
- Run these after changing or adding models.
- If you see errors, check your models for typos or missing fields.

## 2. Collect Static Files
Collect all static files (CSS, JS, images) into one directory for production.
```shell
python manage.py collectstatic
```
**Important:**
- Set `DEBUG=False` in `settings.py` before running this in production to avoid overwriting development static files.
- For more info: [Django static files docs](https://docs.djangoproject.com/en/stable/howto/static-files/)

## 3. Create a Superuser
Create an admin user to access the Django admin interface.
```shell
python manage.py createsuperuser
```
- Follow the prompts to set username, email, and password.

## 4. Run the Development Server
Start the local Django development server.
```shell
python manage.py runserver
```
- Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.
- Use `python manage.py runserver 0.0.0.0:8000` to allow connections from other devices on your network.

## 5. Run Tailwind CSS (if used)
If your project uses Django-Tailwind for CSS:
```shell
python manage.py tailwind start
```
- This watches and rebuilds your Tailwind CSS files as you edit them.

---

## Troubleshooting
- If you get errors about missing modules, run `pip install -r requirements.txt`.
- For static files not appearing, check `STATIC_URL`, `STATIC_ROOT`, and run `collectstatic` again.
- For database errors, check your `DATABASES` setting in `settings.py`.

For more, see the [Django documentation](https://docs.djangoproject.com/en/stable/).
