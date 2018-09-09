ifeq (, $(ENV))
	ENV := development
	env := development
else ifeq (test, $(ENV))
	env := testing
else
	env := $(ENV)
endif

ifeq (, $(NODE_ENV))
	NODE_ENV := development
endif

app := aarau

.DEFAULT_GOAL = test\:coverage
default: test\:coverage


# -- setup

setup:  ## Install Python packages
	pip install -e '.[${env}]' -c constraints.txt
.PHONY: setup

setup\:force:  ## Install Python packages with `--force-reinstall`
	pip install --upgrade --force-reinstall -e '.[${env}]' -c constraints.txt
.PHONY: setup\:force

setup\:update:  ## Update Python packages
	pip install --upgrade -e '.[${env}]' -c constraints.txt
.PHONY: setup\:update


# -- db

db\:init:  ## Create database
	ENV=$(ENV) ${app}_manage 'config/${env}.ini#${app}' db init
.PHONY: db\:init

db\:migrate:  ## Run migrations
	ENV=$(ENV) ${app}_manage 'config/${env}.ini#${app}' db migrate
.PHONY: db\:migrate

db\:rollback:  ## Rollback latest migration
	ENV=$(ENV) ${app}_manage 'config/${env}.ini#${app}' db rollback
.PHONY: db\:rollback

db\:seed:  ## Put seed records for development (See db/seeds)
	ENV=$(ENV) ${app}_manage 'config/${env}.ini#${app}' db seed
.PHONY: db\:seed

db\:drop:  ## Drop database
	ENV=$(ENV) ${app}_manage 'config/${env}.ini#${app}' db drop
.PHONY: db\:drop

db\:reset:  ## Reset database
	${app}_manage 'config/${env}.ini#${app}' db drop
	${app}_manage 'config/${env}.ini#${app}' db init
	${app}_manage 'config/${env}.ini#${app}' db migrate
ifneq (test, $(ENV))
	${app}_manage 'config/${env}.ini#${app}' db seed
endif
.PHONY: db\:reset


# -- serve

serve:  ## Run server process (development)
	./bin/serve --env development --config config/development.ini --reload
.PHONY: serve

serve\:worker:  ## Run worker process (development)
	ENV=$(ENV) ${app}_worker 'config/${env}.ini#${app}'
.PHONY: serve\:worker

serve\:production:  ## Run {server,worker} process both in production mode (see Procfile)
	honcho start
.PHONY: serve\:production


# -- test

test:  ## Run unit tests and functional tests both
	ENV=test py.test -c 'config/testing.ini' -s -q \
	  test/unit test/func test/route_test.py
.PHONY: test

test\:unit:  ## Run unit tests
	ENV=test py.test -c 'config/testing.ini' -s -q \
	  test/unit
.PHONY: test\:unit

test\:func:  ## Run functional tests
	ENV=test py.test -c 'config/testing.ini' -s -q \
	  test/func
.PHONY: test\:func

test\:route:  ## Run only route tests
	ENV=test py.test -c 'config/testing.ini' -s -q \
	  test/route_test.py
.PHONY: test\:route

test\:integration:  ## Run integration tests on browser (Firefox Headless)
	ENV=test TEST_DOMAIN=localhost TEST_SESSION_COOKIE_DOMAIN=localhost \
	  py.test -c 'config/testing.ini' -s -v \
	  --driver Firefox --driver-path ./bin/geckodriver test/integration
.PHONY: test\:integration

test\:doc:  ## Run doctest in Python code
	ENV=test ./bin/run_doctest
.PHONY: test\:doc

test\:js:  ## Run JavaScript unit tests
	NODE_ENV=development karma start
.PHONY: test\:js

test\:coverage:  ## Run `test` with coverage outputs
	ENV=test py.test -c 'config/testing.ini' -s -q \
	  test/unit test/func \
	  --cov=${app} --cov-report term-missing:skip-covered
.PHONY: test\:coverage


# -- i18n (translation)

i18n: | i18n\:compile  ## An alias of `i18n:compile`
.PHONY: i18n

i18n\:extract:  ## Extract translation targets from code
	./bin/linguine extract message
	./bin/linguine extract form
.PHONY: i18n\:extract

i18n\:compile:  ## Make translation files (catalog)
	for ns in message form console\.json ; do \
	  for locale in en ; do \
	    ./bin/linguine compile $$ns $$locale; \
	  done; \
	done
.PHONY: i18n\:compile

i18n\:update:  ## Update catalog (pot)
	for ns in message form console\.json ; do \
	  for locale in en ; do \
	    ./bin/linguine update $$ns $$locale; \
	  done; \
	done
.PHONY: i18n\:update

i18n\:sync:  ## Fetch translation updates from upstrm (scrolliris/scrolliris-console-translation)
	./bin/linguine sync
.PHONY: i18n\:sync


# -- vet

vet: | vet\:style vet\:lint  ## Run `vet:style` and `vet:lint` both (without vet:quality)
.PHONY: vet

vet\:style:  ## Check style using py{code,doc}style (see setup.cfg)
	pycodestyle test aarau
	pydocstyle test aarau
.PHONY: vet\:style

vet\:lint:  ## Lint python codes
	pylint test ${app}
.PHONY: vet\:lint

vet\:quality:  ## Generate codequality.txt using codeclimate (require Docker)
	docker run --interactive --tty --rm --env CODECLIMATE_CODE="${PWD}" \
	  --volume "${PWD}":/code \
	  --volume /var/run/docker.sock:/var/run/docker.sock \
	  --volume /tmp/cc:/tmp/cc \
	  codeclimate/codeclimate analyze -f text > tmp/codequality.txt
	cat tmp/codequality.txt
.PHONY: vet\:quality


# -- utilities

pack:  ## Build assets using gulp-cli
ifeq (, $(shell which gulp 2>/dev/null))
	$(info gulp command not found. run `npm install -g gulp-cli`)
	$(info )
else
	NODE_ENV=$(NODE_ENV) gulp
endif
.PHONY: pack

clean:  ## Delete unnecessary cache etc.
	find . ! -readable -prune -o \
	  ! -path "./.git/*" ! -path "./node_modules/*" ! -path "./venv*" \
	  ! -path "./doc/*" ! -path "./locale/*" ! -path "./tmp/*" \
	  ! -path "./lib/*" -print | \
	  grep -E "(__pycache__|\.egg-info|\.pyc|\.pyo)" | \
	  xargs rm -rf
ifeq (, $(shell which gulp 2>/dev/null))
	$(info gulp command not found. run `npm install -g gulp-cli`)
	$(info )
else
	NODE_ENV=$(NODE_ENV) gulp clean
endif
.PHONY: clean

expose:  ## Print untracked (volatile) files
	git ls-files --others | \
	  grep -vE '(lib|tmp|test|static|db|locale|node_modules|\.?cache)/' | \
	  grep -vE '(__pycache__|\.egg-info|venv)/' | \
	  grep -vE '(\.coverage|\.*-version|bin\/gitlab*)'
.PHONY: expose

deploy:  ## Deploy app to production server
	./bin/plate $(ACTION) $(VERSION)
.PHONY: deploy

help:  ## Display this message
	@grep -E '^[0-9a-z\:\\]+: ' $(MAKEFILE_LIST) | grep -E '  ## ' | \
	  sed -e 's/\(\s|\(\s[0-9a-z\:\\]*\)*\)  /  /' | tr -d \\\\ | \
	  awk 'BEGIN {FS = ":  ## "}; {printf "\033[36m%-17s\033[0m %s\n", $$1, $$2}' | \
	  sort
.PHONY: help
