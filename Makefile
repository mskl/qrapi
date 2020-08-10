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

# Heroku CLI shortcuts
heroku-deploy:
	docker build -t registry.heroku.com/swapper-backend-qrapi/web .
	docker push registry.heroku.com/swapper-backend-qrapi/web:latest
	heroku container:release web -a swapper-backend-qrapi

heroku-open:
	heroku open -a swapper-backend-qrapi

heroku-logs:
	heroku logs -a swapper-backend-qrapi --tail
