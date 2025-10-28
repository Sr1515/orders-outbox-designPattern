build:
	docker compose build

run: 
	docker compose up -d

off:
	docker compose down

log-orders:
	docker compose logs -f orders-api

log-rabbitmq:
	docker compose logs -f rabbitmq

log-relay:
	docker compose logs -f relay-service

log-postgres:
	docker compose logs -f postgres

mk: 
	docker compose exec orders-api python manage.py makemigrations

mg: 
	docker compose exec orders-api python manage.py migrate

create-admin:
	docker compose exec orders-api python manage.py createsuperuser