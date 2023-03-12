# Продуктовый помощник - foodgram

[![Foodgram Workflow](https://github.com/Tsarev-n1/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/Tsarev-n1/foodgram-project-react/actions/workflows/foodgram_workflow.yml)

---

## Описание проекта
Сервис позволяет пользователям делиться рецептами, а так же формировать свой список покупок для выбранных блюд.

## Запуск проекта в контейнере
Клонируйте репозиторий и перейдите в него в командной строке.
Создайте и активируйте виртуальное окружение:
```
git clone git@github.com:Tsarev-n1/foodgram-project-react.git
cd foodgram-project-react
```
Cоздать и открыть файл .env с переменными окружения:
```
cd infra
touch .env
echo DB_ENGINE=django.db.backends.postgresql >> .env
echo DB_NAME=postgres >> .env
echo POSTGRES_PASSWORD=postgres >> .env
echo POSTGRES_USER=postgres  >> .env
echo DB_HOST=db  >> .env
echo DB_PORT=5432  >> .env
echo SECRET_KEY=123456 >> .env
```
Запуск приложения в контейнере
```
docker-compose up -d
```
Запустить миграции, создать суперпользователя, собрать статику и заполнить а БД таблицы с ингредиентами и тегами:
```
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py collectstatic --no-input
docker-compose exec backend python manage.py load_ingredients
docker-compose exec backend python manage.py load_tags
```
## Проверить работу можно уже на готовом сервере
[Продуктовый помощник](http://tsarev.ddns.net)

### Тестовый аккаунт для админ-панели Django
```
email: admin@yandex.ru
password: admin
```

#### [Автор](https://github.com/Tsarev-n1)
