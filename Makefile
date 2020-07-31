build:
	docker build -t qrapi-flask:latest .

run-dev:
	docker run -d -p 5001:5001 \
		-v "${CURDIR}/qrapi:/app" \
		-e "FLASK_ENV=development" \
		-e "API_AUTHORIZATION_TOKEN=secret" \
		qrapi-flask

run:
	docker run -d -p 5001:5001 qrapi-flask

stop:
	docker stop `docker ps -qf ancestor="qrapi-flask"`

bash:
	docker exec -it `docker ps -qf ancestor="qrapi-flask"` /bin/bash
