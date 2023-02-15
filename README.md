#### Доступные переменные окружения:

- `DEBUG` — Дебаг-режим Django.
- `SECRET_KEY` — Ключ Django.
- `SERVER_NAMES` - Разрешённые хосты.
- `STRIPE_PUBLIC_KEY` — :)
- `STRIPE_SECRET_KEY` — :)
- `STRIPE_WEBHOOK_SECRET` — :)

### Структура проекта

```
├───app
│   ├───base
│   │   ├───migrations
│   │   ├───models
│   │   ├───services  # main logic
│   │   ├───static
│   │   │   └───stripe
│   │   │       ├───css
│   │   │       └───js
│   │   ├───templates
│   │   │   └───stripe
│   │   └───views
│   └───config  # settings
└───docker  # dockerfile's
    └───nginx
```

### Url's

`bu/<id>/` - Stripe Session \
`cart/checkout/` - Stripe Session \
`buy/intent/<id>` - <ins>StipeIntent</ins>

`cart/` - Корзина товаров \
`webhooks/stripe/` - Stripe WebHook
---

#### Docker-compose:

1. ```bash 
    docker build -t django-stripe
    ```

2.  ```bash
    docker compose up
    ```

---

### Дополнительные задачи

- [X] Запуск используя Docker
- [X] Использование environment variables
- [X] Просмотр Django Моделей в Django Admin панели
- [X] Запуск приложения на удаленном сервере, доступном для тестирования
- [X] Модель Order, в которой можно объединить несколько Item и сделать платёж в Stripe на содержимое Order c общей
  стоимостью всех Items
- [ ] Модели Discount, Tax, которые можно прикрепить к модели Order и связать с соответствующими атрибутами при создании
  платежа в Stripe - в таком случае они корректно отображаются в Stripe Checkout форме.
- [ ] Добавить поле Item.currency, создать 2 Stripe Keypair на две разные валюты и в зависимости от валюты выбранного
  товара предлагать оплату в соответствующей валюте
- [X] Реализовать не Stripe Session, а Stripe Payment Intent.
