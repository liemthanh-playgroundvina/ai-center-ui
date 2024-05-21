config:
	cp env.example .env
	# And add params ...

build:
	docker build -t ai-center:ui-streamlit -f Dockerfile .

start:
	docker compose -f docker-compose.yml down
	docker compose -f docker-compose.yml up -d

stop:
	docker compose -f docker-compose.yml down
