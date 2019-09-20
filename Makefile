init:
	docker pull mongo:4.0.3
	docker pull python:3.7-slim-buster

compose-docker: # make compose-docker
	docker-compose up -d
	echo "Enter 'docker-compose stop' to stop running the service"
