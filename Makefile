all: pull build

pull:
	docker pull python:alpine

build:
	docker build --network yann_default -t python-routeros .