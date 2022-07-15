# UI

- **Framework**: [React](https://reactjs.org/)
- **Language**: [Typescript](https://www.typescriptlang.org/)
- **Testing framework**: [Jest](https://jestjs.io/)
- **Linter**: [Eslint](https://eslint.org/)
- **Style guide**: [gts](https://github.com/google/gts)
- **Formatter**: [Prettier](https://prettier.io/)
- The react app uses [vite](https://vitejs.dev/) instead of webpack for frontend tooling.

## Setup (local)

- Run `cd ui`
- Run `npm install` to install all dependencies.
- Create a new file in the same directory named `.env` and copy all the content from `.env.template`
- Run `npm run dev` to start the server and visit [site](http://localhost:3000).
- Run `npm run test` to run tests.
- Run `npm run lint` to check if the code is properly formatted.
- Run `npm run lint:fix` to lint code.
- Run `npm run format` to format code.

## Setup (docker)

Make sure you have docker installed. Checkout [installation guide](https://docs.docker.com/get-docker/) to install docker.

- Change your working directory to `ui`
- Create a new file in the same directory named `.env` and copy all the content from `.env.template`
- Run `docker image rm gymkhana-ui` to remove any previous images of `ui`.
- Run `docker build . -t gymkhana-ui -f Dockerfile.dev` to build image.
- Run `docker run --name gymkhana-ui -p 8000:8000 gymkhana-ui` to start the container.
- Run `docker rm -f gymkhana-ui` to stop and remove container.
