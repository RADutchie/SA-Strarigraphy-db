# SA Strat db

## Quick Start

A simple flask based CRUD web application to add, view and edit SA Stratigraphy digital notes into a Postres db

```

Created with https://github.com/testdrivenio/cookiecutter-flask-skeleton.git

```

Designed to run with Docker.
-------------

> Built with Docker v19.03.5.

## Getting Started for local dev

Update the environment variables in *docker-compose.yml*, and then build the images and spin up the containers:

```sh
$ docker-compose up -d --build
```

By default the app is set to use the production configuration. If you would like to use the development configuration, you can alter the `APP_SETTINGS` environment variable:

```
APP_SETTINGS=project.server.config.DevelopmentConfig
```


Create the database:

```sh
$ docker-compose run web python manage.py create-db
$ docker-compose run web python manage.py db init
$ docker-compose run web python manage.py db migrate
$ docker-compose run web python manage.py create-admin
$ docker-compose run web python manage.py create-data
```

Access the application at the address [http://localhost:5002/](http://localhost:5002/)

### Testing

Test without coverage:

```sh
$ docker-compose run web python manage.py test
```

Test with coverage:

```sh
$ docker-compose run web python manage.py cov
```

Lint:

```sh
$ docker-compose run web flake8 project
```

## For Deployment

Set environment variables to production, including database and email variables, including .env file.
Use Dockerfile-for-deploy to build a single container for the web app.
entrypoint_prod.sh will run gunicorn wsgi server in front of flask on port 8000

```sh
$ docker build -t web/app .
$ docker run -d -p 8000:8000 --env-file ./.env web
```
Then ensure connection to database and run 

```sh
$ docker run web python manage.py create-db
$ docker run web python manage.py create-admin
```
Or if on remote server, ssh in and run the below to get a shell in the container 
```sh
$ docker ps
$ docker exec -it <container name> sh
```

Then create the database and admin as above