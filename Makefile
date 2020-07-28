build:
	docker build -t qrapi-flask:latest .

run-dev:
	docker run -p 5001:5001 \
		-e "API_AUTHORIZATION_TOKEN=secret" \
		-e "FLASK_ENV=development" \
		-e "FLASK_RUN_HOST=0.0.0.0" \
		qrapi-flask

run:
	docker run -d -p 5001:5001 qrapi-flask

stop:
	docker stop `docker ps -qf ancestor="qrapi-flask"`

bash:
	docker exec -it `docker ps -qf ancestor="qrapi-flask"` /bin/bash