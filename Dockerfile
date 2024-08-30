FROM python:3.12.5
WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/
COPY .env.docker /code/.env

RUN python manage.py collectstatic --noinput
RUN python manage.py migrate


ENV APP_NAME=STRIPEAPI
ENV DEBUG=True

CMD ["/bin/bash", "-c", "python create_db.py && python manage.py runserver 0.0.0.0:8000"]