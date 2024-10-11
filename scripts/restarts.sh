#!/bin/bash

# Function to run development commands
restart() {
    service=$1
    docker compose -f docker-compose.yml stop $service
    docker compose -f docker-compose.yml up -d $service
}

# Ask the user which service to restart
echo -e "Please enter:\n1 to restart the django service,\n2 to restart the dev_celery_worker service,\n3 to restart the dev_celery_beat service:"
read service_choice

# Check the user input and call the restart function
if [ "$service_choice" == "1" ]; then
    restart django
elif [ "$service_choice" == "2" ]; then
    restart dev_celery_worker
elif [ "$service_choice" == "3" ]; then
    restart dev_celery_beat
else
    echo "Invalid argument, please enter a valid number (1-3)"
fi