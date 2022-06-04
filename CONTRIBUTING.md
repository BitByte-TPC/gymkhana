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

To be updated soon.

### Frontend setup

- Run `cd ui`
- Run `npm install` to install all dependencies.
- Run `npm run dev` to start the server and visit [site](http://localhost:3000).

### Before making PR

- Run `git fetch upstream` & `git rebase upstream/master` to fetch updated codebase into your local repository before creating any new branch.
- Run `git checkout -b <your-branch-name>`
