from os import environ

ENV = environ.get('ENV', 'development')
APP_HOST = environ.get('APP_HOST', '0.0.0.0')
APP_PORT = environ.get('APP_PORT', 8000)

DB_CONFIG = {
    'connections': {
        # Dict format for connection
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'host': environ.get('DB_HOST', 'localhost'),
                'port': environ.get('DB_PORT', 5432),
                'user': environ.get('DB_HOST', 'postgres'),
                'password': environ.get('DB_HOST', 'postgres'),
                'database': environ.get('DB_HOST', 'postgres'),
            }
        },
    },
    'apps': {
        'server': {
            'models': [
                'aerich.models',
            ],
        }
    },
}
