#!/bin/sh

# Check if config.py exists
if [ ! -f /app/config/config.py ]; then
    echo "config.py not found, creating an example config.py..."
    cat <<EOL > /app/config/config.py
import os

CONFIG = {
    "databases": [
        {
            "type": "mariadb",
            "host": "mariadb",
            "username": "root",
            "password": os.getenv("MARIADB_ROOT_PASSWORD", "example_password"),
            "database": os.getenv("MYSQL_DATABASE", "example_database")
        },
        {
            "type": "postgresql",
            "host": "postgresql",
            "username": os.getenv("POSTGRES_USER", "example_user"),
            "password": os.getenv("POSTGRES_PASSWORD", "example_password"),
            "database": os.getenv("POSTGRES_DB", "example_database"),
        },
    ]
}
EOL
fi

# Execute the original CMD
exec "$@"