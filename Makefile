psql-up:
	- docker run --name=postgres -d -e POSTGRES_USER=pguser -e POSTGRES_PASSWORD=pgpass -e POSTGRES_DB=pgdb -e ALLOW_IP_RANGE=0.0.0.0/. -p 5555:5432 -v pg_data:/var/lib/postgresql postgres

psql-restart:
	- docker stop postgres
	- docker rm postgres
	- docker run --name=postgres -d -e POSTGRES_USER=pguser -e POSTGRES_PASSWORD=pgpass -e POSTGRES_DB=pgdb -e ALLOW_IP_RANGE=0.0.0.0/. -p 5555:5432 -v pg_data:/var/lib/postgresql postgres

psql:
	- psql postgresql://pguser:pgpass@localhost:5555/pgdb

psql-dump-data:
	- pg_dump postgresql://pguser:pgpass@localhost:5555/pgdb -t predmeti -t smjer -t korisnici -t prijave -t upisi > dump_data.sql

psql-dump-all:
	- pg_dump postgresql://pguser:pgpass@localhost:5555/pgdb > dump_all.sql

psql-load-data:
	- psql postgresql://pguser:pgpass@localhost:5555/pgdb -f dump_data.sql

psql-load-all:
	- psql postgresql://pguser:pgpass@localhost:5555/pgdb -f dump_all.sql

start:
	- python manage.py runserver