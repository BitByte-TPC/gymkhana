# API 

- **Framework**: [Django](https://www.djangoproject.com/)
- **Language**: [Python 3.8](https://www.python.org/)


## Setup
Make sure you are using `python 3.8` as we are officially working on it. If something fails when using another python version, it's on you to solve that issue. Do not expect support from devs.

- Change your working directory to `api`
- Create a virtual environment: `$ python -m virtualenv .venv`
- Activate the virtual environment: `$ source .venv/bin/activate` (On windows: `> ./.venv/Scripts/activate`)
- Install the dependencies: `$ pip install -r requirements.txt`
- Make Migrations: `$ python manage.py makemigrations` (This commands generates migrations which would be used to update database schemas)
- Migrate the DB: `$ python manage.py migrate`
- Run server: `$ python manage.py runserver`
- Run tests: `$ pytest`
- Run tests with coverage information: `$ pytest --cov=api`

