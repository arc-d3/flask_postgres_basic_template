#!/bin/sh
set -e

echo "Waiting for postgres..."
while ! nc -z db 5432; do
    sleep 1
done

echo "Postgres is ready."

if [ ! -f migrations/env.py ]; then
    echo "Initializing migrations..."
    rm -f migrations/dummy.txt
    flask db init
fi

flask db migrate -m "auto"
flask db upgrade

exec python main.py