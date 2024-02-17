# ambient-app

## Description
This repository contains a full-stack web application with a Python FastAPI backend and a Vite app with React frontend. The backend is located in the `packages/backend` directory, while the frontend is located in the `packages/frontend` directory.

## Frontend
The frontend is a Vite app with React. It follows a typical React project structure. The backend
depends on the build `dist` directory to host the app, the frontend must be built first.

### Initialization
1. Navigate to the `packages/frontend` directory.
2. Ensure you have [Yarn](https://yarnpkg.com/) installed.
3. Run `yarn install` to install the dependencies.
4. Run `yarn build` to build the project.

### Available Scripts
- `yarn dev`: Starts the development server.
- `yarn build`: Builds the production-ready bundle.
- `yarn lint`: Lints the code using ESLint.
- `yarn preview`: Previews the production build locally.
- `yarn format`: Formats the code using Prettier.

## Backend
The backend is a Python FastAPI application. It includes an `app` directory for the main application code and a `migrations` directory for database migrations. The application uses SQLAlchemy as its ORM (Object-Relational Mapping) library and PostgreSQL as its database backend. If no PostgreSQL database URL is provided, the application will default to using a development SQLite database. Examine the .env.example file for ENV variables that can be added.

### Initialization
1. Navigate to the `packages/backend` directory.
2. Ensure you have [Poetry](https://python-poetry.org/) installed, along with a matching Python version (recommended to use pyenv for managing Python versions).
3. Run the following command to install the dependencies:
    ```bash
    poetry install
    ```
4. Start the FastAPI application:
    ```bash
    poetry run python main.py
    ```
    Note: This can be run without the poetry command if the poetry env is active.

### Database Migrations
The application uses Alembic for managing database migrations. Follow these steps to run migrations:

1. Navigate to the `packages/backend` directory.
2. Ensure your database URL is properly configured in the Alembic configuration file (`alembic.ini`).
3. Run the following command to generate a new migration script:
    ```bash
    alembic revision --autogenerate -m "Your migration message"
    ```
4. Run the migration to apply the changes to the database:
    ```bash
    alembic upgrade head
    ```

Make sure to replace `"Your migration message"` with a meaningful description of your migration changes.

## Docker
The entire application can also be built and run using Docker. A Docker Compose file is included for running the application in a Docker environment.

### Building and Running with Docker
1. Ensure you have Docker installed on your system.
2. Navigate to the root directory of the project.
3. Run the following command to build and start the containers:
    ```bash
    docker-compose up --build
    ```

## License
TBA

## Author
[Connor McLean](https://github.com/mclean-connor)
