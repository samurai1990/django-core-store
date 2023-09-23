.PHONY: clean clean-test clean-pyc clean-build docs help down build_ngix runserver stage 
.DEFAULT_GOAL := help

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

build_ngix:
	-docker container prune -f
	-docker image rm target_nginx:1.0.0
	@docker build -t target_nginx:1.0.0 ./nginx

builddev: build_ngix ## build docker
	-docker container prune -f	
	-docker image rm store_io:1.0.0
	@docker build -f Dockerfile.develop -t store_io:1.0.0 .

debug: ## Debug a test
	@MODE="debug" docker compose -f service.yml up

stage: 
	@MODE="stage" docker compose -f service.yml up

runserver: ## Debug a test
	@python manage.py runserver $(h):$(p)

down:
	@docker compose -f service.yml down

attach: ## Attach for debugging
	@docker exec -it $$(docker ps -a --filter name=store_io_web | awk '{ print $$1}'| tail -n+2) bash
