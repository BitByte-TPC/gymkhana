# Contributing to Gymkhana

We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting an issue
- Submitting a fix
- Proposing new features

## Standard Commit Messages

This project is using the [conventional commits](https://www.conventionalcommits.org/en/v1.0.0-beta.2/) standard. Please follow these steps to ensure your
commit messages are standardized:

- Commit messages should have this format:
  `<type>[optional scope]: <description>`
- Type must be one of the following:
  -  **build**: Changes that affect the build system or external dependencies 
  -  **ci**: Changes to our CI configuration files and scripts 
  -  **docs**: Documentation only changes
  -  **feat**: A new feature
  -  **fix**: A bug fix
  -  **perf**: A code change that improves performance
  -  **refactor**: A code change that neither fixes a bug nor adds a feature
  -  **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
  -  **test**: Adding missing tests or correcting existing tests
- Scope should be `ui` or `api` or `global`.
- Description should be concise.
- Example: `feat(ui): add dark-mode`


## Local Setup

- Fork and clone the repository.
- Add remote upstream `git add upstream https://github.com/BitByte-TPC/gymkhana.git`

### Backend setup

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

### Frontend setup

- Run `cd ui`
- Run `npm install` to install all dependencies.
- Run `npm run dev` to start the server and visit [site](http://localhost:3000).

### Before making PR

- Run `git fetch upstream` & `git rebase upstream/master` to fetch updated codebase into your local repository before creating any new branch.
- Run `git checkout -b <your-branch-name>`
