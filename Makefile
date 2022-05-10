# Docker compose shortcuts
build:
	docker-compose build

run: build
	docker-compose up -d --remove-orphans

stop:
	docker-compose down

bash:
	docker-compose exec qrapi-flask bash

logs:
	docker-compose logs -f

rbash:
	docker-compose run qrapi-flask bash

deploy:
	gcloud run deploy --source .

# Upload the core image to dockerhub
dockerhub:
	docker build -t skalimat/qrapi -f misc/dockercore/Dockerfile .
	docker push skalimat/qrapi