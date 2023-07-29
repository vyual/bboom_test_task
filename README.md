Установка зависимостей:

poetry install
ИЛИ
pip3 install -r requirements.txt

Миграции:

poetry run python manage.py migrate
ИЛИ
python3.11 manage.py migrate

Запуск:

poetry run python manage.py runserver
ИЛИ
python3.11 manage.py runserver

Тесты:

poetry run python manage.py test
ИЛИ
python3.11 manage.py test