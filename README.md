# Дипломный проект Foodgram
## Backend-разработка, сборка docker-контейнеров и развёртывание на удалённом сервере с применением GitHub Actions и DockerHub
![Workflow Status](https://github.com/Koloyojik/ foodgram-project-react/actions/workflows/yamdb_workflow.yml/badge.svg?branch=master&event=push)

**Примеы работы на сервере:**
- [**ReDoc на сервере**](http://158.160.17.231/redoc/)
- [**Пример endpoints для API на сервере**](http://158.160.17.231/api/v1/)
- [**Пример работы БД на сервере в разделе Жанры**](http://158.160.17.231/api/v1/genres/)


**Описание**

Проект Foodgram является сервисом по размещению кулинарных рецептов и сбору отзывов пользователей на них.
Этот репозиторий посвящён развёртыванию этого проекта на сервере при помощи GitHub Actions и DockerHub.

**Версии:**
- [Python 3.7.16](https://www.python.org/doc/) 
- [Django 3.2.18](https://docs.djangoproject.com/en/4.1/releases/3.2.18/)
- [Django REST framework 3.14](https://www.django-rest-framework.org/)
- [DRF Simple JWT 4.8](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
- [Django Filter 22.1](https://django-filter.readthedocs.io/en/main/)
- [Docker 23.0](https://docs.docker.com/)
- [Docker Compose 1.29.2](https://docs.docker.com/compose/gettingstarted/)
- [PostgreSQL 14](https://www.postgresql.org/)
- [Gunicorn 20.1](https://gunicorn.org/)
- [nginx 1.22](https://nginx.org/en/)

**Как запустить проект:**

Перед развёртыванием проекта на сервере необходимо остановить работу *nginx*
```bash
sudo systemctl stop nginx 
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

После обновления репозитория, GitHub Actions должен создать *user-db-1* и *user-nginx-1*, а так же загрузить контейнер web из репозитория DockerHub koloyojik/api_yamdb:latest на сервер:

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
sudo docker-compose exec web python manage.py makemigrations
sudo docker-compose exec web python manage.py migrate
sudo docker-compose exec web python manage.py collectstatic --no-input
```
Загружаем данные в базу из резервной копии, если она есть, *fixtures.json*:
```bash
sudo docker cp ./fixtures.json <container_id>:/app/fixtures.json
sudo docker-compose exec web python manage.py loaddata fixtures.json
```
Или создаем суперпользователя для заполнения новой базы данных:
```bash
sudo docker-compose exec web python manage.py createsuperuser
```

Перед остановкой контейнера необходимо создать резервную копию баз данных командой:
```bash
sudo docker-compose exec web python manage.py dumpdata > fixtures.json
```

Автор: [**Даур Павликов**](https://github.com/Koloyojik)