import os

CONFIG = {
    "databases": [
        {
            "type": "mariadb",
            "host": "mariadb",
            "username": "root",
            "password": os.getenv("MARIADB_ROOT_PASSWORD"),
            "database": os.getenv("MYSQL_DATABASE")
        },
        {
            "type": "postgresql",
            "host": "postgresql",
            "username": os.getenv("POSTGRES_USER"),
            "password": os.getenv("POSTGRES_PASSWORD"),
            "database": os.getenv("POSTGRES_DB"),
        },
    ]
}