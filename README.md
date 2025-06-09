#  Mini-Blog на Django

Простой мини-блог с авторизацией, постами и комментариями. Есть API-документация через Swagger.

##  Установка

```bash

git clone "project"
cd "project"

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

# load save db
python manage.py migrate
python manage.py createsuperuser

# start
python manage.py runserver

```

### OR:

```bash

docker compose up --build
```

Создать админа нужно будет вручную в консоли проекта докер:

```bash

python manage.py createsuperuser
```
