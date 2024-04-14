#!/bin/bash

echo "Deploying wordweaver"

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

DATA_DIR=""

echo -n "Creating persistent data directory..."

mkdir -p $DATA_DIR

chown -R 1001:root $DATA_DIR

MEDIA_DIR=""

echo -n "Creating persistent media directory..."

mkdir -p $MEDIA_DIR

chown -R root:root $MEDIA_DIR

echo "COMPLETE"

sh "$SCRIPT_DIR/deployment/clear-docker-project"
sh "$SCRIPT_DIR/deployment/clear-junk"

echo -n "Bringing up docker container..."

docker-compose -f "$SCRIPT_DIR/docker-compose-staging.yml" up --build -d --force-recreate --remove-orphans

echo -n "Cleaning up junk..."

sh "$SCRIPT_DIR/deployment/clear-junk"

echo "COMPLETE"

echo "Deployment completed successfully."
echo "========================================="
