## Project detail

### Installation
- Install `Docker Desktop`, mssql and SQL Server Management Studio (SSMS)
- Run command
```javascript
docker compose build
docker compose up -d
```
- Connect DB and create database `django_app`

- Run command in docker container
```javascript
docker ps
docker exec -it <CONTAINER ID> bash
```
### Check format code
```
python -m venv venv
venv\Scripts\activate
poetry install
pre-commit install
```

### Commands

- Run: `poetry install` to install all packages
- Run: `poetry add package` to add package
- Run: `poetry remove package` to remove package
- Run: `poetry lock` to update **poetry.lock**
- Run: `pre-commit install` to ensure code quality before committing changes. (ignore format code —no-verify)
- Run: `python manage.py makemigrations core --name xxxx_xxxx` to create a migration
- Run: `python manage.py migrate` to migrate database
- Run: `python manage.py runserver` to start dev environmenthont
- Run: `python manage.py show_urls` to show all urls
- Run: `python manage.py shell_plus` to start shell cli
- Run: `print(QuerySet.query)` to showing sql query

### build production
- Run command
```
docker compose -f docker-compose.production.yml -p pms_prod down
docker compose -f docker-compose.production.yml -p pms_prod build --no-cache
docker compose -f docker-compose.production.yml -p pms_prod up -d
```

## Deploy
- CI/CD
```

```

## gRPC
- generate protoc
```
python3 -m grpc_tools.protoc --proto_path=/usr/src/service/ --python_out=/usr/src/service/ --grpc_python_out=/usr/src/service/ /usr/src/service/core/grpc/notification.proto
```
