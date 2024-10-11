#!/bin/bash

docker compose -f docker-compose.yml run --rm django python manage.py makemigrations
docker compose -f docker-compose.yml run --rm django python manage.py migrate