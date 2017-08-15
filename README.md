# Aarau

`/ɑ́ːràu/`

[![build status](https://gitlab.com/lupine-software/aarau/badges/master/build.svg)](
https://gitlab.com/lupine-software/aarau/commits/master) [![coverage report](
https://gitlab.com/lupine-software/aarau/badges/master/coverage.svg)](
https://gitlab.com/lupine-software/aarau/commits/master)

![Scrolliris](https://gitlab.com/lupine-software/aarau/raw/master/aarau/assets/img/scrolliris-logo-300x300.png)

```txt
  ___,
 /   |
|    |   __,   ,_    __,
|    |  /  |  /  |  /  |  |   |
 \__/\_/\_/|_/   |_/\_/|_/ \_/|_/

Aarau; An Application of scRolliris As User interface
```

The application of [https://scrolliris.com/](https://scrolliris.com/).


## Requirements

* Python `>= 3.5.3`
* PostgreSQL `>= 9.6.3`
* Redis `>= 3.2.0`
* Memcached `>= 1.4.33`
  * libmemcached (via pylibmc) (worker)
* Node.js `>= 7.8.0` (build)
* GNU gettext `>= 0.19.8.1` (translation)
* Graphviz (document)


## Setup environment

```zsh
% cd /path/to/aarau

: use python\'s virtualenv
% python3.5 -m venv venv
% source venv/bin/activate
(venv) % pip install --upgrade pip setuptools

: Node.js (e.g. nodeenv)
(venv) % pip install nodeenv
(venv) % nodeenv --python-virtualenv --with-npm --node=7.10.1
: re-activate for node.js at this time
(venv) % source venv/bin/activate
(venv) % npm update --global npm
```

### PostgreSQl

Setup PostgreSQL database.

```zsh
: URL is postgresql://<user>:<password>@localhost:5432/<datname>
(venv) % psql -U xxx -c "CREATE USER <user> WITH PASSWORD '<password>';"
(venv) % psql -U xxx -c "ALTER USER <user> WITH CREATEDB LOGIN;"
: create database
(venv) % make db-init
: or create it manually
(venv) % psql -U <user> postgres -c "CREATE DATABASE <datname>;"

: prepare database (default env: development)
(venv) % make db-migrate
```

### DynamoDB

See amazon dynamodb [document](http://docs.aws.amazon.com/amazondynamodb/\
latest/developerguide/Tools.DynamoDBLocal.html).

```zsh
: Put dynamodb-local from Amazon
% bin/setup-dynamodb_local

: Or latest dynamodb into lib/dynamodb_local_latest by yourself
% cd lib
% curl -sLO http://dynamodb-local.s3-website-us-west-2.amazonaws.com/\
    dynamodb_local_latest.tar.gz
% mkdir dynamodb_local_latest
% tar zxvf dynamodb_local_latest.tar.gz -C dynamodb_local_latest
% cp ./dynamodb_local ../bin/

: run (on localhost using :8001)
% ./bin/dynamodb_local
```

### Redis

TODO

### Memcached

TODO


## Development

Use `waitress` as wsgi server.  
Check `Makefile`

```zsh
% cd /path/to/aarau
% source venv/bin/activate

: set env and seed(s)
(venv) % cp .env.sample .env
(venv) % cp db/seeds/{users.samyle.yml,users.yml}

: install packages
(venv) % make setup
: or manually install packages
(venv) % pip install -e ".[development]" -c constraints.txt
: additional packages if you want
(venv) % pip install -r requirements.txt -c constraints.txt

: install node modules & run gulp task
(venv) % npm install --global gulp-cli
(venv) % npm install

(venv) % gulp

: import seed data into database for development
(venv) % make db-seed

: use runner script
(venv) % make serve
: see ./bin/serve --help
(venv) % ./bin/serve -r
: or just start server for development using pserve
(venv) % aarau_pserve config/development.ini --reload
```

### Migration

Create migration file manually into `db/migrations`.

```zsh
(venv) % make db-migrate   # migrate remains all migrations
(venv) % make db-rollback  # rollback latest migration
```

#### Note

You can generate with this command a migration file automatically.  
But some custom fields are missing and the result doesn't match 
our desired scheme.

Create manually by your self for now.

```zsh
: it might be hint and usefull as reference
% pw_migrate create --directory db/migrations --auto 'aarau.models' \
  --database 'postgresql://user:pass@localhost:5432/dbname' NAME
```

### Style check & Lint

* flake8
* flake8-docstrings (pep257)
* pylint
* eslint

#### Python

```zsh
: add hook
(venv) % flake8 --install-hook git

(venv) % make style
```

#### JavaScript

```zsh
(venv) % npm install eslint -g

(venv) % eslint gulpfile.js
(venv) % eslint aarau/assets
```


## Deployment

Setup production environment.

Use `CherryPy` as wsgi server.

```zsh
: run install and start server for production
(venv) % ./bin/serve --env production --config config/production.ini --install

: use Procfile (via `bin/start` command)
(venv) % honcho start
```

### Publishing

E.g. Google App Engine

```zsh
: take latest sdk from https://cloud.google.com/sdk/downloads
% cd lib
(venv) % curl -sLO https://dl.google.com/dl/cloudsdk/channels/rapid/ \
  downloads/google-cloud-sdk-<VERSION>-linux-x86_64.tar.gz

: check sha256 checksum
(venv) % echo "<CHECKSUM>" "" ./google-cloud-sdk-<VERSION>-linux-x86_64.tar.gz \
  | sha256sum -c -
./google-cloud-sdk-<VERSION>-linux-x86_64.tar.gz: OK
(venv) % tar zxvf google-cloud-sdk-<VERSION>-linux-x86_64.tar.gz

: setup lib/ as a root for sdk
(venv) % CLOUDSDK_ROOT_DIR=. ./google-cloud-sdk/install.sh
(venv) % cd ../

: load sdk tools
(venv) % source ./bin/load-gcloud
(venv) % gcloud init
```


## Testing

Run unit tests and functional tests.
See also `.gitlab-ci.yml`.

```zsh
(venv) % ENV=test make setup
: or manually install packages
(venv) % pip install -e ".[testing]" -c constraints.txt

(venv) % ENV=test make db-init
(venv) % ENV=test make db-migrate
(venv) % ENV=test make db-clean

: use make
(venv) % make test
: or run manually
(venv) % ENV=test py.test -c config/testing.ini -q

: run a test case
(venv) % ENV=test py.test -c config/testing.ini \
  aarau/tests/unit/views/settings_test.py \
  -k test_view_settings_account -v
```

Check test coverage

```zsh
(venv) % make coverage
```

### CI

For debugging, run **gitlab-ci** localy using `gitlab-ci-multi-runner`.

#### Setup

Prepare `gitlab-ci-multi-runner` in your local machine.

```zsh
: gitlab-ci (localy)
(venv) % curl -sL https://gitlab-ci-multi-runner-downloads.s3.amazonaws.com \
  /latest/binaries/gitlab-ci-multi-runner-linux-amd64 \
  -o bin/gitlab-ci-multi-runner
(venv) % chmod +x bin/gitlab-ci-multi-runner
: run runner container
(venv) % docker run -d --name gitlab-runner --restart always \
  -v /srv/gitlab-runner/config:/etc/gitlab-runner \
  gitlab/gitlab-runner:latest
```

#### Run

Start docker as service, then run `ci-runner`.

```zsh
: run test job in docker (via gitlab-ci-multi-runner)
(venv) % ./bin/ci-runner test

: this is equivalent as above command
(venv) % mkdir -p tmp/_cache
(venv) % ./bin/gitlab-ci-multi-runner exec docker \
  --cache-dir /cache \
  --docker-volumes `pwd`/tmp/_cache:/cache \
  --env TEST_AUTH_SECRET=... \
  --env TEST_DATABASE_URL=... \
  ...
  <JOB>
```

#### Links

See documents.

* https://gitlab.com/gitlab-org/gitlab-ci-multi-runner/issues/312
* https://docs.gitlab.com/runner/install/linux-manually.html


## Document

```zsh
(venv) % cd doc
: e.g. use feh to display image
(venv) % dot -T png er.dot > er.png; feh er.png
```


## Translation

TODO


## License

Aarau; Copyright (c) 2017 Lupine Software LLC

This is free software;  
You can redistribute it and/or modify it under the terms of the
GNU Affero General Public License (AGPL).

See [LICENSE](LICENSE).
