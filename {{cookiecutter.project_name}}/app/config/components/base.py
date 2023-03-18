from os import environ

ENV = environ.get('ENV', 'development')
APP_HOST = environ.get('APP_HOST', '0.0.0.0')
APP_PORT = environ.get('APP_PORT', 8000)
