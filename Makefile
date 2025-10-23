build:
	docker compose build

run: 
	docker compose up -d

off:
	docker compose down

log-orders:
	docker compose logs -f orders-api

log-redis:
	docker compose logs -f redis

log-postgres:
	docker compose logs -f postgres

mk: 
	docker compose exec orders-api python manage.py makemigrations

mg: 
	docker compose exec orders-api python manage.py migrate

create-admin:
	docker compose exec orders-api python manage.py createsuperuser