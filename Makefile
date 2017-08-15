ifeq (, $(ENV))
	extra := development
else ifeq (test, $(ENV))
	extra := testing
else
	extra := $(ENV)
endif

section := aarau

# installation

setup:
	pip install -e '.[${extra}]' -c constraints.txt
.PHONY: setup

# database

db-init:
	aarau_manage 'config/${extra}.ini#${section}' db init
.PHONY: db-init

db-migrate:
	aarau_manage 'config/${extra}.ini#${section}' db migrate
.PHONY: db-migrate

db-rollback:
	aarau_manage 'config/${extra}.ini#${section}' db rollback
.PHONY: db-rollback

db-seed:
	aarau_manage 'config/${extra}.ini#${section}' db seed
.PHONY: db-seed

db-drop:
	aarau_manage 'config/${extra}.ini#${section}' db drop
.PHONY: db-drop

db-reset:
	aarau_manage 'config/${extra}.ini#${section}' db drop
	aarau_manage 'config/${extra}.ini#${section}' db init
	aarau_manage 'config/${extra}.ini#${section}' db migrate
ifneq (test, $(ENV))
	aarau_manage 'config/${extra}.ini#${section}' db seed
endif
.PHONY: db-reset


# application

# server
serve:
	./bin/serve --env development --config config/development.ini --reload
.PHONY: serve

# worker
worker:
	aarau_worker 'config/${extra}.ini#${section}'
.PHONY: worker

# use `bin/start` via honcho. see Procfile
start:
	honcho start
.PHONY: start

# testing

test:
	ENV=test py.test -c 'config/testing.ini' -s -q
.PHONY: test

coverage:
	ENV=test py.test -c 'config/testing.ini' -s -q --cov=aarau --cov-report \
	  term-missing:skip-covered
.PHONY: coverage

# translation

catalog-extract:
	./bin/linguine extract message
	./bin/linguine extract form
.PHONY: catalog-extract

catalog-compile:
	./bin/linguine compile message en
	./bin/linguine compile form en
.PHONY: catalog-compile

catalog-update:
	./bin/linguine update message en
	./bin/linguine update form en
.PHONY: catalog-update

catalog: | catalog-compile
.PHONY: catalog

# utilities

check-style:
	flake8
.PHONY: check-style

style: | check-style
.PHONY: style

clean:
	find . ! -readable -prune \
	       ! -path "./.git/*" ! -path "./node_modules/*" ! -path "./venv*" \
	       ! -path "./doc/*"  ! -path "./locale/*" \
	       ! -path "./build-output*" | \
	  grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf
ifeq (, $(shell which gulp))
ifneq (test, $(ENV))
	$(error gulp command not found. run `npm install -g gulp-cli`)
endif
else
	gulp clean
endif
.PHONY: clean

.DEFAULT_GOAL = coverage
default: coverage
