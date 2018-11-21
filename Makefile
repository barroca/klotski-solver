.PHONY: all build test destroy

IMAGE_NAME=klotski-game
FILE=sample-board.txt
run-script:
	@docker-compose exec api python ./klotski-solver.py ${FILE}

test:
	@docker-compose exec api pytest tests/

destroy:
	docker images -a | grep ${IMAGE_NAME} | awk '{print $$3}' | xargs docker rmi -f

build:
	@docker-compose build

up:
	@docker-compose up

shell:
	@docker-compose exec api bash

venv:
	virtualenv --python=python3 venv

venv-destroy:
	rm -rf venv
