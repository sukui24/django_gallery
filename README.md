# General
Public web gallery based on Django web framework. Allows users to private/public image upload and look other users images. Provided download functional, user profiles, CRUD operations with users and images and more.

**Currently hosted on [this](https://automode.asion.tk/) domain**

## Technologies
Project made by using this technologies:
* [Python 3.11.0](https://www.python.org/)
* [Django 4.2.3](https://www.djangoproject.com/)
* [Django REST Framework 3.14.0](https://www.django-rest-framework.org/)
* [PostgreSQL 12](https://www.postgresql.org/)
* [Nginx](https://nginx.org/)
* [Docker](https://www.docker.com/)
* [Docker compose V2](https://docs.docker.com/compose/)
* [Gunicorn 21.2.0](https://gunicorn.org/)
* [Swagger UI (drf-yasg)](https://drf-yasg.readthedocs.io/en/stable/)

**And also a few more supporting libraries that I did not use much, you can find them in `requirements.txt`**

## Local setup
* To set-up project on your computer first of all you shoud **clone repository**:
```bash
$ git clone https://github.com/Diazord/django_gallery "folder_name"
```

* Then go in your folder (if added):
```bash
$ cd "folder_name"
```

* Rename `dev_settings.py` to `settings.py`

* Now you should run migrations:
```bash
$ python manage.py makemigrations && python manage.py migrate
```

* After all preparing you can run server:
```bash
$ python manage.py runserver 127.0.0.1:8000
```

**If you using different folder for data make sure you support it**
* data directory used in `base(and users_app)/signals.py`, `settings.py`, `docker-compose.yml` and `nginx.conf`

**Now you're done with local deployment!**

## Docker setup

Docker deployment is little harder since you need to manage `.env` and `.env.db` files with your data:

* First fill the `.env.example` and `.env.db.example` with your data, then rename them to: `.env` and `.env.db`

* Secondary in settings.py change `CSRF_TRUSTED_ORIGINS` to your domain/ip

**Now you're ready to run container:**
* Make sure you're in the top project folder which contains `docker-compose.yml`:
```bash
$ pwd

Path
----
C:\your\project\folder
```

* Then run docker compose build:
```bash
$ docker compose up -d --build
```

**if you didn't change port - default is `80`**

**Now you're done with docker deployment!**
