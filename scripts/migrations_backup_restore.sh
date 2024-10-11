#!/bin/bash

# Your source directory
SOURCE_DIR=./apps

# Your target directory
DATE_TIME=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_FOLDER="backup_migrations"
TARGET_DIR="$BACKUP_FOLDER/migration_backup_$DATE_TIME"

# The directories you want to handle
DIRS=("ecommerce" "notification_management" "users_management" )

echo "Please choose operation:"
echo "1. Backup"
echo "2. Restore"
echo "3. Remove Migrations files"
read -p "Enter your choice (1, 2, or 3): " choice

case $choice in
    1)  # Backup operation
        # Create target directory if it doesn't exist
        mkdir -p $TARGET_DIR

        # Loop through each specified directory
        for dir in ${DIRS[@]}; do
            # Check if migrations subdirectory exists
            if [ -d "$SOURCE_DIR/$dir/migrations" ]; then
                # Create the directory structure in the target directory
                mkdir -p "$TARGET_DIR/$dir/migrations"

                # Copy the migrations directory
                cp -r "$SOURCE_DIR/$dir/migrations/"* "$TARGET_DIR/$dir/migrations/"
            fi
        done

        echo "Backup operation completed successfully."

        # Compress the backup directory
        zip -r "$TARGET_DIR.zip" "$TARGET_DIR"

        # Remove the original directory after compression
        rm -r "$TARGET_DIR"

        echo "Backup operation completed successfully. The backup has been saved as $TARGET_DIR.zip"
        ;;
    2)  # Restore operation
        echo "Please choose a backup to restore:"
        select ZIP_FILE in $BACKUP_FOLDER/*.zip; do
            if [ -z "$ZIP_FILE" ]; then
                echo "Invalid choice. Please select a valid backup file."
                continue
            fi

            # Remove existing migrations
            for dir in ${DIRS[@]}; do
                if [ -d "$SOURCE_DIR/$dir/migrations" ]; then
                    rm -r "$SOURCE_DIR/$dir/migrations/"*
                else
                    mkdir -p "$SOURCE_DIR/$dir/migrations"
                fi
                touch "$SOURCE_DIR/$dir/migrations/__init__.py"
            done
            echo "Migrations files removed and __init__.py files recreated successfully."

            # Extract the zip file
            unzip $ZIP_FILE

            # Get the name of the extracted directory
            EXTRACTED_DIR=${ZIP_FILE%.zip}

            # Loop through each specified directory
            for dir in ${DIRS[@]}; do
                # Check if migrations subdirectory exists in the extracted directory
                if [ -d "$EXTRACTED_DIR/$dir/migrations" ]; then
                    # Copy the migrations directory back to the source directory
                    cp -r "$EXTRACTED_DIR/$dir/migrations/"* "$SOURCE_DIR/$dir/migrations/"
                fi
            done

            # Remove the extracted directory after copying files
            rm -r "$EXTRACTED_DIR"

            echo "Restoration operation completed successfully."
            break
        done
        ;;
    3)  # Remove operation
        echo "Removing Files:"
        if [ -d "./media/" ] && [ "$(ls -A ./media/)" ]; then
          rm -r ./media/*
          echo "Deleted Media Files!"
        else
          echo "./media/ is empty or does not exist, skipping delete."
        fi

        for dir in ${DIRS[@]}; do
            if [ -d "$SOURCE_DIR/$dir/migrations" ]; then
                rm -r "$SOURCE_DIR/$dir/migrations/"*
                touch "$SOURCE_DIR/$dir/migrations/__init__.py"
            fi
        done
        echo "Migrations files removed and __init__.py files recreated successfully."
        ;;
    *)  # Invalid choice
        echo "Invalid choice. Please enter 1 for Backup or 2 for Restore."
        ;;
esac
