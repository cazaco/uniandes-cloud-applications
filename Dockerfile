FROM python:3

COPY . app/
WORKDIR app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR project/

RUN python manage.py makemigrations events_app
RUN python manage.py sqlmigrate events_app 0001
RUN python manage.py migrate

CMD python manage.py runserver 0:8080