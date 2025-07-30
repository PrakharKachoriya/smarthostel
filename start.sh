#!/bin/bash

# Usage: ENV=dev ./start.sh OR ENV=prod ./start.sh
set -e

ENV=${ENV:-dev}  # Default to 'dev' if ENV not set

echo "Starting in '$ENV' environment..."

if [ "$ENV" = "dev" ]; then
  COMPOSE_FILES="-f docker-compose.yaml -f docker-compose.dev.yaml"
elif [ "$ENV" = "prod" ]; then
  COMPOSE_FILES="-f docker-compose.yaml -f docker-compose.prod.yaml"
else
  echo "Unknown ENV: $ENV"
  echo "Use ENV=dev or ENV=prod"
  exit 1
fi

docker compose $COMPOSE_FILES up server --build