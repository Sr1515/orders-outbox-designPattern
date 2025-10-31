build:
	docker compose build

run: 
	docker compose up -d

off:
	docker compose down

log-api:
	docker compose logs -f receipts-api

log-db:
	docker compose logs -f receipts-db

log-consumer: 
	docker compose logs -f receipts-consumer

db-init:
	docker compose exec receipts-api /usr/local/bin/flask db init

# example how to add some new migrate
#docker compose exec receipts-api /usr/local/bin/flask db migrate -m ""
