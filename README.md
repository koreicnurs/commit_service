Сервис, который хранит коммиты по публичному репозиторию.



## Установка

```
git clone https://github.com/koreicnurs/commit_service.git
cd commit_service/
virtualenv --python `which python3` env
. env/bin/activate
pip install -r requirements.txt
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```
