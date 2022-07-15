# API

- **Framework**: [Django](https://www.djangoproject.com/)
- **Language**: [Python 3.8](https://www.python.org/)

## Prerequisites
- Create an OAuth2 Client
  1. Go to the [Google Cloud Platform Console](https://console.cloud.google.com/)
  2. From the projects list, select a project or create a new one
  3. If the APIs & services page isn't already open, open the console left side menu and select APIs & services
  4. On the left, click Credentials
  5. Click New Credentials, then select OAuth client ID
  6. Select `Web application` in the Application type
  7. Give a name to the application
  8. In Authorized Javascript origins add `http://localhost:3000`
  9. In Authorized redirect URIs add `http://localhost:3000/login/redirect`
  10. Click on Create button
  11. Note Client ID and Client Secret

## Setup (local)

Make sure you are using `python 3.8` as we are officially working on it. If something fails when using another python version, it's on you to solve that issue. Do not expect support from devs.

- Change your working directory to `api`
- Create a new file in the same directory named: `.env` and copy all the content from `.env.template`
- Add the OAuth2 Client ID and Secret to the `.env` file
- Create a virtual environment: `$ python -m virtualenv .venv`
- Activate the virtual environment: `$ source .venv/bin/activate` (On windows: `> ./.venv/Scripts/activate`)
- Install the dependencies: `$ pip install -r requirements.txt`
- Make Migrations: `$ chmod +x scripts/makemigrations.sh && sh ./scripts/makemigrations.sh` (This commands generates migrations which would be used to update database schemas)
- Migrate the DB: `$ python manage.py migrate`
- Run server: `$ python manage.py runserver`
- Run tests: `$ pytest`
- Run tests with coverage information: `$ pytest --cov=api`

## Setup (docker)

Make sure you have docker installed. Checkout [installation guide](https://docs.docker.com/get-docker/) to install docker.

- Change your working directory to `api`
- Create a new file in the same directory named `.env` and copy all the content from `.env.template`
- Run `docker image rm gymkhana-api` to remove any previous images of `api`.
- Run `docker build . -t gymkhana-api` to build image.
- Run `docker run --name gymkhana-api -p 8000:8000 gymkhana-api` to start the container.
- Run `docker rm -f gymkhana-api` to stop and remove container.
