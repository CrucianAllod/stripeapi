# Stripe API Django Приложение

Это Django приложение интегрирует Stripe для обработки платежей. Оно позволяет пользователям просматривать товары, добавлять их в заказ и переходить к оформлению заказа с использованием платежного шлюза Stripe.

## Особенности

- **Управление товарами**: Просмотр и добавление товаров в заказ.
- **Управление заказами**: Просмотр сводки заказа, применение скидок и налогов.
- **Интеграция с Stripe**: Безопасная обработка платежей с использованием Stripe.

## Предварительные требования

- Docker
- Ключи API Stripe

## Установка

1. **Клонируйте репозиторий:**

    ```sh
    git clone https://github.com/yourusername/stripeapi.git
    cd stripeapi
    ```

2. **Настройте переменные окружения:**

    Скопируйте файл `.env.example` в `.env` и `.env.docker`, обновите необходимые переменные, такие как `SECRET_KEY`, `DEBUG`, `STRIPE_PUBLIC_KEY` и `STRIPE_SECRET_KEY`.

    ```sh
    cp .env.example .env
    cp .env.example .env.docker
    ```

3. **Соберите и запустите Docker контейнер:**

    ```sh
    docker build -t stripeapi .
    docker run -p 8000:8000 stripeapi
    ```

4. **Заполните базу данных тестовыми данными:**

    База данных автоматически заполниться скриптом create_db.py при запуске Docker контейнера.
    
    Вы можете добавить данные с помощью админ панели Django.

    Для этого создайте суперюзера:
    ```python manage.py createsuperuser
    ```
    Откройте браузер и перейдите по адресу `http://localhost:8000/admin/`.

5. **Доступ к приложению:**

    Откройте браузер и перейдите по адресу `http://localhost:8000`.

## Использование

### Просмотр товаров и добавление товаров в заказ

1. **Просмотр товаров:**

    Перейдите на домашнюю страницу, чтобы просмотреть доступные товары.

2. **Детализация товаров:**

    Нажмите кнопку "View Details", чтобы просмотреть детализация товара.

3. **Добавление в заказ:**

    Нажмите кнопку "Add to Order", чтобы добавить товар в ваш заказ.

4. **Просмотр сводки заказа:**

    Нажмите кнопку "Go to Order", чтобы просмотреть сводку заказа.

### Обработка платежей

1. **Детализация товара:**

    На странице детализации товара вы можете обновить ввести данные карты для оплаты.

2. **Оплата товара:**

    Нажмите кнопку "Buy", чтобы оплатить товар и при успешной оплате перейти на страницу с благодарностью.

3. **Сводка заказа:**

    На странице сводки заказа вы можете обновить детали налога и скидки.

4. **Переход к оформлению заказа:**

    Нажмите кнопку "Buy", чтобы перейти на страницу оформления заказа Stripe.

5. **Завершение оплаты заказа:**

    Следуйте инструкциям на странице оформления заказа Stripe, чтобы завершить платеж.

## Конфигурация Docker

Конфигурация Docker включает следующие компоненты:

- **Dockerfile:**

    ```dockerfile
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
    ```

## Структура проекта

```
stripeapi/
├── Dockerfile
├── create_db.py
├── manage.py
├── requirements.txt
├── stripeapi/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── itemstripe/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── stripe_utils.py
│   ├── urls.py
│   ├── views.py
│   ├── templates/
│   │   ├── index.html
│   │   ├── item_detail.html
│   │   ├── order_summary.html
│   │   ├── success.html
│   │   ├── cancel.html
├── .env.docker
├── .gitignore
├── README.md
```
