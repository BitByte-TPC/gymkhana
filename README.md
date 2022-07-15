# Gymkhana

A web application for managing various gymkhana activities like club
registration, event management, inventory management, booking club
merchandise, etc. for all the gymkhana clubs in our institute.

## Tech stack

- **FrontEnd:** Single Page Application using [React](https://reactjs.org/)([TypeScript](https://www.typescriptlang.org/))
- **API:** [Django Rest Framework](https://www.django-rest-framework.org/) for the API ([Python](https://www.python.org/))
- **PullRequest validation:** [Github Actions](https://github.com/features/actions) to do automated PR validation by running tests and linter
- **Version Control and Hosting:** [Git](https://git-scm.com/) for Source Code Management and [Github](https://github.com) for hosting

## Prerequisites for Setup

Create an OAuth2 Client

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

## Local Setup

- Fork and clone the repository.
- Add remote upstream `git remote add upstream https://github.com/BitByte-TPC/gymkhana.git`
- [ui setup](https://github.com/BitByte-TPC/gymkhana/tree/master/ui#readme)
- [api setup](https://github.com/BitByte-TPC/gymkhana/tree/master/api#readme)

## Setup using docker

- Fork and clone the repository.
- Add remote upstream `git remote add upstream https://github.com/BitByte-TPC/gymkhana.git`
- Create a new file in both `api` & `ui` directories named: `.env` and
  copy all the content from the respective `.env.template` files.
- Run `docker compose up` to start

## Design Docs

- [1000 feet view](https://github.com/BitByte-TPC/gymkhana/wiki/1000-feet-View)
- [Authentication](https://github.com/BitByte-TPC/gymkhana/wiki/Authentication-Design-Doc)
- [Clubs & Events](https://github.com/BitByte-TPC/gymkhana/wiki/Clubs-and-events-Design-Doc) (In Review)

## Want to contribute?

Check out [CONTRIBUTING.md](CONTRIBUTING.md).
