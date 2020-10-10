# Commit Service
Сервис, который хранит коммиты по публичному репозиторию.


## Установка

```
1. Склонируйте репозитории
    git clone https://github.com/koreicnurs/commit_service.git

2. Войдите в папку с проектом
    cd commit_service/

3. Установите виртуальное окружение
    virtualenv --python `which python3` env

4. Активируйте виртуальное окружение
    . env/bin/activate

5. Установите REDIS глобально
    sudo apt-get install redis-server (Linux Ubuntu)
    brew install redis (macOS)

6. Установите все компоненты проекта
    pip install -r requirements.txt

7. Сделайте миграцию
    ./manage.py migrate

8. Создайте супер юзара для админки
    ./manage.py createsuperuser

9. Запустите сам проект
    ./manage.py runserver

10. Запустите Celery в 2 разных теминалах
    celery -A commit_service worker -l info
    celery -A commit_service beat -l info
```


## Как работает проект
Для начала нужно указать в админке репозитории, это может быть GitLab или GitHub

В Админ панели указать путь к репозиторию для GitLab обзятаельно заполнить строку Project_id,
а для GitHub обязательно заполнить строки Author_name и Repository_name

Каждый день в 10 00 утра, запускается таск

Таск в свою очередь вытаскивает все коммиты по указанным репозиториям






