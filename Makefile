build:
	docker build -t qrapi-flask:latest .

.SILENT:
setup:
	echo "Run the following command:"
	echo "source export_env_variables.sh"

run-dev:
	docker run -d -p "$(PORT):$(PORT)" \
		-v "${CURDIR}/qrapi:/app" \
		-e "FLASK_ENV=development" \
		-e "API_AUTHORIZATION_TOKEN=secret" \
		qrapi-flask

stop:
	docker stop `docker ps -qf ancestor="qrapi-flask"`

bash:
	docker exec -it `docker ps -qf ancestor="qrapi-flask"` /bin/bash

# Heroku CLI shortcuts
heroku-deploy:
	docker build -t registry.heroku.com/swapper-backend-qrapi/web .
	docker push registry.heroku.com/swapper-backend-qrapi/web:latest
	heroku container:release web -a swapper-backend-qrapi

heroku-open:
	heroku open -a swapper-backend-qrapi

heroku-logs:
	heroku logs -a swapper-backend-qrapi --tail
