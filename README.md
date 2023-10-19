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

## Clonning repository
* To set-up project on your computer first of all you shoud **clone repository**:
```bash
$ git clone https://github.com/sukui24/django_gallery
```
You can change folder for clonning into by setting folder name after git link, but make sure to use it properly later

* Then go in project folder:
```bash
$ cd djnago_gallery
```

## Fixtures using
**Fixtures is preset data that i made for project testing purpose**

**If you want to get preset data and don't fill website by yourself follow this steps:**
 1. Setup the project (local or docker)
 2. Make sure you're in `core` folder: execute ```$ pwd```
 3. Execute this command:
    ```bash
    $ python manage.py loaddata fixtures.json
    ```
 4. In .env you have field `DATA`, set it to `'fixtures_data/'`
 5. Restart django server

## Fixtures loaddata decoding issue
If you have decode issue (for example UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte) then follow this steps:
* Check the file encoding:
    - Open file in VSCode or another text editor
    - You will see encoding on the bottom of work window
    - (In VSCode) type on encoding and select `Save with encoding` then choose `utf-8`

* **If you can't change encoding manually then execute this command**:
  ```bash
  $ python -c "import codecs; codecs.open('OUTPUT.json', 'w', 'utf-8').write(codecs.open('INPUT.json', 'r', 'ENCODING')
  ```
  `OUTPUT`: name of the file for re-coding output (fixtures.json)
  
  `INPUT`: name of wrong decoded file (rename it from fixtures.json to wrong_fixtures.json for example and put in `INPUT`)
  
  `ENCODING`: the wrong fixtures.json encoding (in my case it was `utf-16`)
  
* Now check again encoding or just try to load data again

**If something goes wrong anyways you can contact me or find solution by yourself** 

## Local setup

**Make sure to clone the project first**

* First rename the settings files:

1. `setting.py` to something else, for example `prod_settings.py`

2. `dev_settings.py` to `settings.py`

* Rename .env.example to .env and set `DATA` field to `'data/'`, or `'fixtures_data/'` if you're using fixtures. 

* Now you should run migrations:
```bash
$ python manage.py makemigrations && python manage.py migrate
```

* Use this command to run server:
```bash
$ python manage.py runserver 127.0.0.1:8000
```

**!!! If you using different folder for data (media) make sure you support it !!!**
* data directory used in: `base(and users_app)/signals.py`, `settings.py`, `docker-compose.yml` and `nginx.conf`

**Now you're done with local deployment!**

## Docker setup

**Make sure to clone the project first**

Docker deployment is little harder since you need to manage `.env` and `.env.db` files with your data:

* First fill the `.env.example` and `.env.db.example` with your data, then rename them to: `.env` and `.env.db`

* Secondary in settings.py change `CSRF_TRUSTED_ORIGINS` to your domain/ip

**!!! If you using different folder for data (media) make sure you support it !!!**
* data directory used in: `base(and users_app)/signals.py`, `settings.py`, `docker-compose.yml` and `nginx.conf`

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
## P.S.
I can forgot to handle some operations in this `README`, but i hope you can handle it by your own or you can contact me :)
I'm trying to improve and would be glad if someone will help me to write documentation or to optimize my code.
