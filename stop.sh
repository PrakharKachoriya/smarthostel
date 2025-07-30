#!/bin/bash

# Usage: ENV=dev ./stop.sh OR ENV=prod ./stop.sh
set -e

ENV=${ENV:-dev}

echo "Stopping '$ENV' environment..."

if [ "$ENV" = "dev" ]; then
  COMPOSE_FILES="-f docker-compose.yaml -f docker-compose.dev.yaml"
elif [ "$ENV" = "prod" ]; then
  COMPOSE_FILES="-f docker-compose.yaml -f docker-compose.prod.yaml"
else
  echo "Unknown ENV: $ENV"
  exit 1
fi

docker compose $COMPOSE_FILES down
