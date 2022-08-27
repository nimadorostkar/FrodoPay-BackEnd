# FrodoPay API Services

Frodo Pay a mobile app you always keep near on your phone at hand!
Safe, Simple and helpful way to manage your crypto payments!

check demo or use api: https://frodopay.pythonanywhere.com/

<br>

[![](https://img.shields.io/badge/python-3.7%20%7C%203.8-brightgreen)](https://www.python.org/)
[![](https://warehouse-camo.ingress.cmh1.psfhosted.org/e6b4c32598d3849599e30d23aae1dabcdd59a248/68747470733a2f2f696d672e736869656c64732e696f2f707970692f646a76657273696f6e732f646a616e676f2d6a616c616c692e737667)](https://www.djangoproject.com/)
[![](https://warehouse-camo.ingress.cmh1.psfhosted.org/cd7ef4975d71b4a87a35b3c01b5b1ec8481c4549/68747470733a2f2f696d672e736869656c64732e696f2f707970692f762f7069702e737667)](https://pypi.org/project/django-extra-settings/)
[![](https://img.shields.io/pypi/l/django-extra-settings.svg?color=blue)](https://github.com/fabiocaccamo/django-extra-settings/blob/master/LICENSE.txt)
[![](https://warehouse-camo.ingress.cmh1.psfhosted.org/e6204225b517cffe323f2898cd51b8885664675e/68747470733a2f2f6769746875622e636f6d2f736c6173686d696c692f646a616e676f2d6a616c616c692f776f726b666c6f77732f54657374732f62616467652e7376673f6272616e63683d6d61696e)](https://github.com)



Build code with docker compose
```
docker-compose build
```

Run the built container
```
docker-compose up -d
```



Build the image and spin up the containers:
```
docker-compose up -d --build
```



Migrate databases
```
docker-compose exec app python manage.py makemigrations
docker-compose exec app python manage.py migrate
```




Collect static files
```
docker-compose exec app python manage.py collectstatic
```



Create super user
```
docker-compose exec app python manage.py createsuperuser
```
