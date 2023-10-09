# django_gallery
Public web gallery based on Django web framework. Allows users to private/public image upload and look other users images. Provided download functional, user profiles, CRUD operations with users and images and more.

## Local deployment
To set-up project on your computer first of all you shoud **clone repository**:
```
git clone https://github.com/Diazord/django_gallery "folder_name"
```
Then go in your folder (if added):
```
cd "folder_name"
```
In settings.py change all prod settings to dev, example:
> SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY") => SECRET_KEY = 'Your key here'
After all preparing you can run server:
```
python manage.py runserver 127.0.0.1:8000
```
**Now you're done with local deployment!**

## Docker deployment

Docker deployment is little harder since you need to manage `.env` and `.env.db` files with your data

First fill the `.env.example` and `.env.db.example` with your data
Then rename this files to: `.env` and `.env.db`

Secondary in settings.py change `CSRF_TRUSTED_ORIGINS` to your domain/ip

Now you're ready to run container:
Make sure you're in the top project folder:
```
pwd

Path
----
C:\your\project\folder
```
Then run docker compose build:
```
docker compose up -d --build
```
if you didn't change port - default is `80`

**Now you're done with docker deployment!**
