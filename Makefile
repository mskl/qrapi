build:
	docker build -t qrapi-flask:latest .

run:
	docker run -d -p 5001:5001 qrapi-flask

stop:
	docker stop `docker ps -qf ancestor="qrapi-flask"`

bash:
	docker exec -it `docker ps -qf ancestor="qrapi-flask"` /bin/bash