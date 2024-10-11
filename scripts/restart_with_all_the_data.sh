#!/bin/bash


# Specify the folders where backups are stored
DB_BACKUP_FOLDER="./backup_database"
MIGRATION_BACKUP_FOLDER="./backup_migrations"

# Function to backup database and migrations
backup_data() {
    # Backup Database
    echo "Starting database backup..."
    local db_backup_name="backup_$(date +%Y-%m-%d_%H-%M-%S)_auto.sql"
    docker compose -f ./docker-compose.yml run --rm db-backup bash -c "pg_dump -h db -p 5436 -U postgres -d punthorder_db > $DB_BACKUP_FOLDER/$db_backup_name"
    echo "Database backup completed: $db_backup_name"

    # Backup Migrations
    echo "Starting migrations backup..."
    local migration_backup_name="migration_backup_$(date +%Y-%m-%d_%H-%M-%S)_auto"
    local migration_target_dir="$MIGRATION_BACKUP_FOLDER/$migration_backup_name"

    # The directories you want to handle
    local dirs=("authentication" "bet_manager" "notification_manager" "users_management")
    mkdir -p $migration_target_dir

    for dir in ${dirs[@]}; do
        if [ -d "./apps/$dir/migrations" ]; then
            mkdir -p "$migration_target_dir/$dir/migrations"
            cp -r "./apps/$dir/migrations/"* "$migration_target_dir/$dir/migrations/"
        fi
    done

    # Compress the backup directory
    zip -r "$migration_target_dir.zip" "$migration_target_dir"
    rm -r "$migration_target_dir"
    echo "Migrations backup completed: $migration_backup_name.zip"
}

# Function to stop and clean up Docker containers
stop_and_cleanup_docker() {
    echo "Stopping Docker containers..."
    docker compose down
    echo "Cleaning up Docker system..."
    docker system prune -a --volumes
}

# Function to rebuild Docker containers
rebuild_docker() {
    echo "Rebuilding Docker containers..."
    docker compose build
}


# Function to restore database and migrations
restore_data() {
    echo "Restoring database and migrations..."

    # Restore Database
    echo "Starting database restore..."
    local latest_db_backup=$(ls -t $DB_BACKUP_FOLDER/*.sql | head -1)
    if [ -f "$latest_db_backup" ]; then
        local db_backup_name=$(basename $latest_db_backup)
        echo "Restoring from backup file: $db_backup_name"  # Display the backup file name
        docker compose -f ./docker-compose.yml run --rm db-restore bash -c "psql -h db -p 5436 -U postgres -c 'DROP DATABASE IF EXISTS punthorder_db;' && psql -h db -p 5436 -U postgres -c 'CREATE DATABASE punthorder_db;' && psql -h db -p 5436 -U postgres -d punthorder_db < /backup/$db_backup_name"
        echo "Database restore completed."
    else
        echo "No database backup file found."
    fi

    # Restore Migration Files
    echo "Starting migrations restore..."
    local latest_migration_backup=$(ls -t $MIGRATION_BACKUP_FOLDER/*.zip | head -1)
    if [ -f "$latest_migration_backup" ]; then
        unzip -o $latest_migration_backup -d $MIGRATION_BACKUP_FOLDER
        local extracted_dir=${latest_migration_backup%.zip}

        # Your specified directories
        local dirs=("authentication" "bet_manager" "notification_manager" "users_management")
        for dir in ${dirs[@]}; do
            local migration_dir="./apps/$dir/migrations"
            if [ -d "$extracted_dir/$dir/migrations" ]; then
                # Clear the existing migrations directory
                if [ -d "$migration_dir" ]; then
                    rm -r "$migration_dir/"*
                fi
                # Recreate the __init__.py file to keep it as a Python package
                touch "$migration_dir/__init__.py"
                # Copy the restored migration files
                cp -r "$extracted_dir/$dir/migrations/"* "$migration_dir/"
            fi
        done

        rm -r "$extracted_dir"
        echo "Migrations restore completed."
    else
        echo "No migration backup file found."
    fi
}

# Function to run Django setup tasks
run_django_setup() {
    echo "Running Django setup tasks..."
    docker compose run app python manage.py makemigrations
    docker compose run app python manage.py migrate
    docker compose run app python manage.py collectstatic --noinput
}

# Function to start Docker containers
start_docker() {
    echo "Starting Docker containers..."
    docker compose up -d
}

# Main script execution
backup_data
stop_and_cleanup_docker
rebuild_docker
run_django_setup
start_docker
restore_data

echo "Process completed."
