#!/bin/bash

# Function to run development commands
restart() {
    service=$1
    docker compose -f docker-compose.yml stop $service
    docker compose -f docker-compose.yml up -d $service
}

# Ask the user which service to restart
echo -e "Please enter:\n1 to restart the django service,\n2 to restart the race-delta-forwarder service,\n3 to restart the promo-bet-stream-forwarder service,\n4 to restart the mug-bet-stream-forwarder service:"
read service_choice

# Check the user input and call the restart function
if [ "$service_choice" == "1" ]; then
    restart django
elif [ "$service_choice" == "2" ]; then
    restart race-delta-forwarder
elif [ "$service_choice" == "3" ]; then
    restart promo-bet-stream-forwarder
elif [ "$service_choice" == "4" ]; then
    restart mug-bet-stream-forwarder
else
    echo "Invalid argument, please enter a valid number (1-4)"
fi