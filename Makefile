.PHONY: help test test-sqlite test-postgres test-mysql test-mariadb test-oracle test-db test-matrix db-up db-down build publish clean

PYTHON ?= python
TEST ?= ./manage.py test tests

POSTGRES_URL ?= postgres://jsonstore:jsonstore@127.0.0.1:5432/jsonstore
MYSQL_URL    ?= mysql://jsonstore:jsonstore@127.0.0.1:3306/jsonstore
MARIADB_URL  ?= mysql://jsonstore:jsonstore@127.0.0.1:3307/jsonstore
ORACLE_URL   ?= oracle://system:jsonstore@127.0.0.1:1521/FREEPDB1

help:  ## show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'

test: test-sqlite  ## run the suite on sqlite (default)

test-sqlite:  ## run the suite on sqlite -- JSON query tests are skipped
	$(PYTHON) $(TEST)

test-postgres:  ## run the suite against the postgres container
	DATABASE_URL=$(POSTGRES_URL) $(PYTHON) $(TEST)

test-mysql:  ## run the suite against the mysql container
	DATABASE_URL=$(MYSQL_URL) $(PYTHON) $(TEST)

test-mariadb:  ## run the suite against the mariadb container
	DATABASE_URL=$(MARIADB_URL) $(PYTHON) $(TEST)

test-oracle:  ## run the suite against the oracle container
	DATABASE_URL=$(ORACLE_URL) $(PYTHON) $(TEST)

test-db: db-up test-postgres test-mysql test-mariadb  ## every containerized db except oracle

test-matrix:  ## every supported django version on sqlite
	tox

db-up:  ## start the database containers and wait until they are healthy
	docker compose up -d --wait postgres mysql mariadb

db-down:  ## stop and remove the database containers
	docker compose --profile oracle down -v

build: clean  ## build the sdist and wheel
	$(PYTHON) -m build
	twine check dist/*

publish: build  ## upload to PyPI
	twine upload dist/*

clean:  ## remove build artifacts
	rm -rf build dist django_jsonstore.egg-info
