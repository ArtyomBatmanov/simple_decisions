## Запуск проекта 

 - Склонируйте репозиторий в папку проекта https://github.com/ArtyomBatmanov/simple_decisions
 - Перейдите на https://dashboard.stripe.com/apikeys чтобы получить Publishable key и Secret key
 - После получения ключей перейдите в файл settings.py в директории myproject и присвойте STRIPE_PUBLIC_KEY и STRIPE_SECRET_KEY соответствующие значения.
 - Выполните команду: sudo docker compose build app
 - Затем команду: sudo docker compose up app
 - Запуститься сервер: http://0.0.0.0:8080/ перейдите на http://0.0.0.0:8000/
 - Для того чтобы проверить возможность оплаты можете воспользоваться тестовыми банковскими картами https://stripe.com/docs/testing#cards
    Админ: 
        логин: admin
        пароль: admin
