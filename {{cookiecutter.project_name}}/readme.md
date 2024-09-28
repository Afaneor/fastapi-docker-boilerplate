# Start

To start up the app you can run native with:
```shell
python app/main.py
```
or docker way:

```shell
docker-compose up -d
```

# Migrations
First of all you need to initialize migrations:
```shell
aerich init-db
```
This will create migrations folder in db module. And all models in 
__init__.py (db module) will be reflected in the migration.

# TODO
* ~~linters~~
* ~~Tests~~
* wemake services linters
* admin
* celery
