# Aarau

`/ɑ́ːràu/`

[![pipeline status][pipeline]][commit] [![coverage report][coverage]][commit]


```txt
  ___,
 /   |
|    |   __,   ,_    __,
|    |  /  |  /  |  /  |  |   |
 \__/\_/\_/|_/   |_/\_/|_/ \_/|_/

Aarau; An Application of scRolliris As User interface
```

The application of [https://scrolliris.com/](https://scrolliris.com/).


## Repository

[https://gitlab.com/scrolliris/aarau](
https://gitlab.com/scrolliris/aarau)


## Requirements

* Python `>= 3.5.4`
* PostgreSQL `>= 9.6.3`
* Redis `>= 3.2.0`
* Memcached `>= 1.4.33`
  * libmemcached (via pylibmc) (worker)
* Datastore (emulator)
* Node.js `>= 7.10.1` (build)
* GNU gettext `>= 0.19.8.1` (translation)
* [Neuchâtel](https://gitlab.com/scrolliris/neuchatel) as git subtree
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
https://gitlab.com/scrolliris/neuchatel).

Don't commit directly the changes on above translation project into this repo.

```zsh
: setup `locale`
% git remote add neuchatel https://gitlab.com/scrolliris/neuchatel.git
% git subtree add --prefix locale neuchatel master

: synchronize with updates into specified branch
% git  pull -s subtree -Xsubtree=locale neuchatel master

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
(venv) % npm install --global gulp-cli i18next-conv
(venv) % npm install

: run gulp
(venv) % make build

: compile translation data (gettext .mo in locale and .json in static/locale)
(venv) % make compile

: import seed data into database for development
(venv) % make db-seed

: use runner script
(venv) % make serve
```

### Migration

Create migration file manually into `db/migrations`.

```zsh
(venv) % make db-migrate # migrate remains all migrations
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

### Check, Lint and Analyze

* flake8
* flake8-docstrings (pep257)
* pylint
* eslint
* codeclimate

#### Python

```zsh
: add hook
(venv) % flake8 --install-hook git

(venv) % make check
(venv) % make lint

: run both
(venv) % make vet
```

#### JavaScript

```zsh
(venv) % npm install eslint -g

(venv) % eslint gulpfile.js
(venv) % eslint aarau/assets
```

#### Codequality

```zsh
: run codeclimate in docker
(venv) % make analyze
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
(venv) % echo "CHECKSUM" "" ./google-cloud-sdk-<VERSION>-linux-x86_64.tar.gz \
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

: build assets
(venv) % make build

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
https://gitlab.com/scrolliris/neuchatel)

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

This project is distributed as various licenses by parts.

```txt
Aarau
Copyright (c) 2017 Lupine Software LLC
```

### Documentation

`GFDL-1.3`

The files in the `aarau/doc` directory are distributed as
GNU Free Documentation License. (version 1.3)

```txt
Permission is granted to copy, distribute and/or modify this document
under the terms of the GNU Free Documentation License, Version 1.3
or any later version published by the Free Software Foundation;
with no Invariant Sections, no Front-Cover Texts, and no Back-Cover Texts.
A copy of the license is included in the section entitled "GNU
Free Documentation License".
```

Check the [GNU Free Documentation License](
https://www.gnu.org/licenses/fdl-1.3.en.html).

### Image

`CC-BY-NC-SA-4.0`

The illustration and photos in this project are licensed under the
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
License.

[![Creative Commons License](
https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png)](
http://creativecommons.org/licenses/by-nc-sa/4.0/)

Check the [Legalcode](
https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode).

### Software (program)

`AGPL-3.0`

```txt
This is free software: You can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
```

See [LICENSE](LICENSE).


[pipeline]: https://gitlab.com/scrolliris/aarau/badges/master/pipeline.svg
[coverage]: https://gitlab.com/scrolliris/aarau/badges/master/coverage.svg
[commit]: https://gitlab.com/scrolliris/aarau/commits/master
