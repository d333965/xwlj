#!/bin/bash

# Navigate to the directory
cd /home/xwlj

# Fetch the latest changes from the origin repository
git fetch origin

# Merge the changes from the origin's main branch
git merge origin/main

# Stop the running Docker containers
docker-compose down

# Build the Docker containers
docker-compose build

# Start the Docker containers in detached mode
docker-compose up -d

# Apply database migrations
docker-compose exec backend aerich upgrade
