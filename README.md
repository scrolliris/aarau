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
* Datastore (emulator)
* Node.js `>= 7.8.0` (build)
* GNU gettext `>= 0.19.8.1` (translation)
* [Neuchâtel](https://gitlab.com/lupine-software/neuchatel) as git subtree
* Graphviz (document)


## Integrations

TODO


## Setup

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
(venv) % npm --version
5.3.0
```

### Dependencies

#### Neuchâtel

See translation project [Neuchâtel](
https://gitlab.com/lupine-software/neuchatel).

Don't commit directly the changes on above translation project into this repo.

```zsh
: setup `locale`
(venv) % git remote add neuchatel https://gitlab.com/lupine-software/neuchatel.git
(venv) % git subtree add --prefix locale neuchatel master

: synchronize with updates into specified branch
(venv) % git  pull -s subtree -Xsubtree=locale neuchatel master

: subtree list
% git log | grep git-subtree-dir | tr -d ' ' | cut -d ":" -f2 | sort | uniq
```

#### PostgreSQl

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

#### Redis

TODO

#### Memcached

TODO

#### Datastore

See GCP datastore [document]().

```zsh
TODO
```


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

: install node modules & run gulp task
(venv) % npm install --global gulp-cli
(venv) % npm install

(venv) % gulp

: import seed data into database for development
(venv) % make db-seed

: use runner script
(venv) % make serve
```

### Migration

Create migration file manually into `db/migrations`.

```zsh
(venv) % make db-migrate   # migrate remains all migrations
(venv) % make db-rollback  # rollback latest migration
```

#### Note

You can generate a migration file with a command below, automatically.  
But some custom fields are missing and the result doesn't match 
our desired scheme.

Create manually by your self for now.

```zsh
: it might be hint and usefull as reference
% pw_migrate create --directory db/migrations --auto 'aarau.models' \
  --database 'postgresql://user:pass@localhost:5432/dbname' NAME
```

### Style & Lint

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

```zs
: publish website
(venv) % source ./bin/load-gcloud
(venv) % gcloud app deploy ./app.yaml --project <project-id> --verbosity=info
```


## Testing

Run unit and functional tests.
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
  aarau/test/unit/views/settings_test.py \
  -k test_view_settings_account -v
```

Check test coverage

```zsh
(venv) % make coverage
```

### CI

You can check it by yourself using `gitlab-ci-multi-runner` on local machine.
It requires `docker`.

```zsh
% ./bin/setup-gitlab-ci-multi-runner

: use script
% ./bin/ci-runner test
```

#### Links

See documents.

* https://gitlab.com/gitlab-org/gitlab-ci-multi-runner/issues/312
* https://docs.gitlab.com/runner/install/linux-manually.html


## Documentation

```zsh
(venv) % cd doc
: e.g. use feh to display image
(venv) % dot -T png er.dot > er.png; feh er.png
```


## Translation

See `./bin/linguine --help` and translation project [repository](
https://gitlab.com/lupine-software/neuchatel)

### Generate new catalog

Generate `xxx.pot` file.

```zsh
: edit Makefile (see also `bin/linguine` script)
(venv) % make catalog-extract
```

### Update and Compile translation catalog

See `Makefile`.
The translation catalog needs GNU gettext.

```zsh
(venv) % make catalog-update

: alias `make catalog` is also available
(venv) % make catalog-compile
```

### Work-flow

0. extract
1. generate
2. update
3. compile



## License

Aarau; Copyright (c) 2017 Lupine Software LLC

This is free software;  
You can redistribute it and/or modify it under the terms of the
GNU Affero General Public License (AGPL).

See [LICENSE](LICENSE).
