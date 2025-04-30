# Quick fevelopment commands

**Migrations:**
```shell
python manage.py makemigrations
python manage.py migrate
```

**Collect static files:**

**Important:** Set `DEBUG=False` in `settings.py` before running this in production to avoid overwriting the development static files.
```shell
python manage.py collectstatic
```

**Create superuser:**
```shell
python manage.py createsuperuser
```

**Run server:**
```shell
python manage.py runserver
```

**Run Tailwind:**
```shell
python manage.py tailwind start
```
