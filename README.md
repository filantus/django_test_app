## django_test_app
Test Application based on Django and Django REST Framework


## Запуск в Docker
```
docker run --name django_app_test --rm -v $PWD:/app -p 8000:8000 -it python:3.7-slim-stretch bash
cd /app
pip install rcssmin --install-option="--without-c-extensions" && \
    pip install rjsmin --install-option="--without-c-extensions" && \
    pip install -r requirments.txt
```

### Тесты
`python manage.py test`

### Запуск сервера
`python manage.py runserver 0.0.0.0:8000`


## Запуск на Ubuntu 16.04 с Python 3.7

#### Обновляем системные пакеты
`sudo apt-get update && sudo apt-get upgrade`

#### Ставим библиотеки для сборки питона
```
sudo apt-get install -y build-essential python-dev python-setuptools python-pip libpcre3 libpcre3-dev \
    zlib1g-dev libssl-dev libcurl4-openssl-dev libreadline-dev libyaml-dev libxml2-dev libxslt-dev \
    libgdbm-dev libc6-dev libffi-dev libsqlite3-dev
```

### Установка Python3.7 !!! Важно - перезапишет ваш python3 и все python3 пакеты если таковые имеются !!!
```
cd /tmp && wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz && \
    sudo tar -xvf Python-3.7.0.tgz && cd /tmp/Python-3.7.0/ && \
    sudo ./configure && sudo make && sudo make install && sudo rm -rf /tmp/*
```

### !!! На следующем этапе нужно вернуться в папку с проектом (django_test_app) !!!
#### Установка виртуального окружения python и зависимостей проекта
```
sudo pip3 install virtualenv
sudo python3 -m virtualenv ./.venv
sudo ./.venv/bin/python ./.venv/bin/pip install -r requirments.txt
```

### Тесты
`./.venv/bin/python manage.py test`

### Запуск сервера
`./.venv/bin/python manage.py runserver`
