# Дипломный проект Foodgram
## Backend-разработка, сборка docker-контейнеров и развёртывание на удалённом сервере с применением GitHub Actions и DockerHub
[![foodgram workflow](https://github.com/Koloyojik/foodgram-project-react/actions/workflows/workflow.yaml/badge.svg)](https://github.com/Koloyojik/foodgram-project-react/actions/workflows/workflow.yaml)

**Примеры работы на сервере:**
- [**Главная страница**](http://158.160.17.231/)
- [**Раздел Django Admin на сервере**](http://158.160.17.231/admin/)
- [**Документация к API на сервере**](http://158.160.17.231/api/docs/)

Для входа в раздел администратора:
```bash
login: admin@admin.ru
password: admin 
```

**Описание**

Проект Foodgram является сервисом по размещению кулинарных рецептов с их фотографиями.
Этот репозиторий посвящён развёртыванию этого проекта на сервере при помощи GitHub Actions и DockerHub.
Во время разработки проекта, после изучения предоставленной документации было решено разбить проект на 3 приложения *api*, *recipes* и *users*, при этом основную логику работы проекта было решено вынести в отдельную поддиректорию, чтобы в будущем при расширении функционала API не ломать обратную совместимость и разрабатывать новые модули внутри другого подкаталога.
Все рецепты сортируются согласно указанным при их создании тегам. Авторизованные пользователи могут подписываться на понравившихся авторов, добавлять рецепты в избранное, в список покупок, а затем скачивать список покупок в формате .pdf. Неавторизованным пользователям доступна страница регистрации, авторизации, а так же просмотр рецептов других пользователей. Раздел админа настроен, в него выведены все существующие модели и созданы необходимые параметры для сортировки и группировки.

**Версии:**
- [Python 3.7.16](https://www.python.org/doc/) 
- [Django 3.2.18](https://docs.djangoproject.com/en/4.1/releases/3.2.18/)
- [Django REST framework 3.14](https://www.django-rest-framework.org/)
- [Djoser 2.1](https://djoser.readthedocs.io/en/latest/introduction.html)
- [Django Filter 22.1](https://django-filter.readthedocs.io/en/main/)
- [Docker 23.0](https://docs.docker.com/)
- [Docker Compose 1.29.2](https://docs.docker.com/compose/gettingstarted/)
- [PostgreSQL 14](https://www.postgresql.org/)
- [Gunicorn 20.1](https://gunicorn.org/)
- [nginx 1.22](https://nginx.org/en/)

**Как запустить проект:**

Перед развёртыванием проекта на сервере необходимо остановить работу *nginx*
```bash
sudo systemctl disable nginx 
```

После этого необходимо обновить *docker-compose* до последней версии:
```bash
sudo curl -L "https://github.com/docker/compose/releases/download/v2.4.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
```bash
sudo chmod +x /usr/local/bin/docker-compose
```
Для проверки иправной работы *docker-compose* просто вызываем утилиту из консоли
```bash
docker-compose
```

При помощи утилиты **scp** копируем необходимую статику, резервные копии БД, конфигурационные файлы *nginx/default.conf* и *docker-compose.yaml* на сервер.

Перед финальной отправкой проекта в репозиторий необходимо перейти в раздел *Settings* репозитория на GitHub и открыть раздел *Secrets and variables > Actions* и добавить необходимые для работы *Workflow* переменные:
- **DOCKER_USERNAME** - имя пользователя DockerHub чей репозиторий будет использован для развёртывания
- **DOCKER_PASSWORD** - пароль от репозитория на DockerHub
- **USER** - имя пользователя на удалённом сервере
- **HOST** - IP-адресс удалённого сервера
- **PASSPHRASE** - ключевое слово для SSH
- **SSH_KEY** - приватный SSH-ключ
- **TELEGRAM_TO** - ID пользователя Телеграм, которому должно приходить оповещение безопасности
- **TELEGRAM_TOKEN** - Токен бота, который должен рассылать уведомления
- **DB_ENGINE** - БД, которую должен использовать Django.
- **DB_NAME** - Название БД
- **POSTGRES_USER** - Имя пользователя указанной БД
- **POSTGRES_PASSWORD** - Пароль доступа к БД
- **DB_HOST** - IP-адрес на котором запущена БД
- **DB_PORT** - порт через который работает БД
- **DEBUG** - Режим отладки Django, может быть *True* или *False*

После обновления репозитория, GitHub Actions должен создать *user-db-1* и *user-nginx-1*, а так же загрузить контейнеры backend и frontend из репозитория DockerHub user/foodgram_backend:latest и user/foodgram_frontend:latest на сервер:

Перед началом развёртывания необходимо перенести файлы nginx/default.conf и docker-compose.yml на сервер при помощи утилиты **scp**:
```bash
scp -r /path/to/infra/ user_name@host_ip:/path/to/work_directory
```

Необходимо подключиться к удалённому серверу по SSH:
```bash
ssh user_name@host_ip
```
И выполнить *docker container ls* для проверки работы контейнеров:
```bash
sudo docker container ls
```

Выполняем миграции для базы данных и собираем статику в контейнер:
```bash
sudo docker-compose exec backend python manage.py makemigrations
sudo docker-compose exec backend python manage.py migrate
sudo docker-compose exec backend python manage.py collectstatic --no-input
```
В проекте предусмотрены готовые скрипты для импорта в базу данных ингридиентов из файла csv и генерация тегов для правильной работы сервиса:
```bash
sudo docker-compose exec backend python manage.py import_ingredients_from_csv
sudo docker-compose exec backend python manage.py import_tags
```
Загружаем данные в базу из резервной копии, если она есть, *fixtures.json*:
```bash
sudo docker cp ./fixtures.json <container_id>:/app/fixtures.json
sudo docker-compose exec backend python manage.py loaddata fixtures.json
```
Создаем суперпользователя, если необходимо:
```bash
sudo docker-compose exec backend python manage.py createsuperuser
```

Перед остановкой контейнера необходимо создать резервную копию баз данных командой:
```bash
sudo docker-compose exec backend python manage.py dumpdata > fixtures.json
```
Остановка контейнеров производится командами:
```bash
sudo docker-compose down -v (если необходимо очистить данные Value)
sudo docker-compose stop (обычная остановка)
```

Автор: [**Даур Павликов**](https://github.com/Koloyojik)
