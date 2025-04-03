
build: c2/* dumper/* victim/*
	mkdir -p challenge
	docker compose build
	docker compose run --rm victim
	docker compose down

.PHONY: build
