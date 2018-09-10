# Scrolliris Console

Code Name: `Aarau /ɑ́ːràu/`

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

[https://gitlab.com/scrolliris/scrolliris-console](
https://gitlab.com/scrolliris/scrolliris-console)


## Requirements

* Python `>= 3.6.6`
* PostgreSQL `>= 9.6.3`
* Redis `>= 3.2.0`
* Memcached `>= 1.4.33`
  * libmemcached (via pylibmc) (worker)
* Node.js `>= 8.11.4` (build)
* GNU gettext `>= 0.19.8.1` (translation)
* [Scrolliris Console Translation (Neuchâtel)](https://gitlab.com/scrolliris/scrolliris-console-translation) as git subtree
* Graphviz (document)


## Setup

```zsh
% cd /path/to/aarau

: use python\'s virtualenv
% python3.6 -m venv venv
% source venv/bin/activate
(venv) % pip install --upgrade pip setuptools

: Node.js (e.g. nodeenv)
(venv) % pip install nodeenv
(venv) % nodeenv --python-virtualenv --with-npm --node=8.11.4
: re-activate for node.js at this time
(venv) % source venv/bin/activate
(venv) % npm update --global npm
(venv) % npm --version
6.4.1
```

Then, check `make help`.

```zsh
(venv) % make help
...
```

### Dependencies

#### Neuchâtel

See translation project [Scrolliris Console Translation (Neuchâtel)](
https://gitlab.com/scrolliris/scrolliris-console-translation).

Don't commit directly the changes on above translation project into this repo.

```zsh
: setup `locale`
% git remote add translation https://gitlab.com/scrolliris/scrolliris-console-translation.git
% git subtree add --prefix locale console-translation master

: synchronize with updates into specified branch
% git  pull -s subtree -Xsubtree=locale console-translation master

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
(venv) % make db:init
: or create it manually
(venv) % psql -U <user> postgres -c "CREATE DATABASE <datname>;"

: prepare database (default env: development)
(venv) % make db:migrate
```

#### Redis

TODO

#### Memcached

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

: install node modules & run gulp task
(venv) % npm install --global gulp-cli i18next-conv karma-cli eslint
(venv) % npm install

: run gulp
(venv) % make pack

: compile translation data (gettext .mo in locale and .json in static/locale)
(venv) % make i18n:compile

: import seed data into database for development
(venv) % make db:seed

: use runner script
(venv) % make serve
(venv) % make serve:worker
```

### Migration

Create migration file manually into `db/migrations`.

```zsh
(venv) % make db:migrate # migrate remains all migrations
(venv) % make db:rollback # rollback latest migration
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

### Style, Lint and Analyze

* pycodestyle
* pydocstyle
* pylint
* eslint
* codeclimate

#### Python

```zsh
(venv) % make vet:style
(venv) % make vet:lint

: run both
(venv) % make vet
```

##### Codequality

```zsh
: run codeclimate in docker
(venv) % make vet:quality
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

### Deployment

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
```

```zs
: check current versions (default service)
(venv) % ACTION=list make deploy

: see delivery script `plate`
(venv) % ACTION=deliver VERSION=v9 make deploy

: put plate (delete)
(venv) % ACTION=clean VERSION=v8 make deploy
```



## Testing

Run unit and functional tests.
See also `.gitlab-ci.yml`.

```zsh
(venv) % ENV=test make setup
: or manually install packages
(venv) % pip install -e ".[testing]" -c constraints.txt

(venv) % ENV=test make db:init
(venv) % ENV=test make db:migrate

: build assets
(venv) % make pack

: compile translation files
(venv) % make i18n:compile

: use make (unit tests and functional tests)
(venv) % make test

: run a test case
(venv) % ENV=test py.test -c config/testing.ini \
  test/unit/views/settings_test.py \
  -k test_view_settings_account -v
```

Check test coverage

```zsh
(venv) % make test:coverage
```

See also

```zsh
(venv) % make test:js
(venv) % make test:integration
```

### CI

You can check it by yourself using `gitlab-runner` on local machine.
It requires `docker`.

```zsh
% ./bin/setup-gitlab-runner

: use script
% ./bin/ci-runner test
```

#### Links

See documents.

* https://docs.gitlab.com/runner/
* https://docs.gitlab.com/runner/install/linux-manually.html


## Documentation

```zsh
(venv) % cd doc
: e.g. use feh to display image
(venv) % dot -T png er.dot > er.png; feh er.png
```


## Translation

See `./bin/linguine --help` and translation project [repository](
https://gitlab.com/scrolliris/scrolliris-console-translation)

### Generate new catalog

Generate `xxx.pot` file.

```zsh
: edit Makefile (see also `bin/linguine` script)
(venv) % make i18n:extract
```

### Update and Compile translation catalog

See `Makefile`.
The translation needs GNU gettext.

```zsh
(venv) % make i18n:update

: alias `make i18n` is also available
(venv) % make i18n:compile
```

Translations for frontend (json) needs `i18next-conv`.

```zsh
% npm install -g i18next-conv
% make i18n:compile
```

### Work-flow

0. sync
1. extract
2. update
3. compile


## Note

Subdomains

* carrell
* console
* registry


## License

This project is distributed as various licenses by parts.

```txt
Scrolliris Console
Copyright (c) 2017-2018 Lupine Software LLC
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


[pipeline]: https://gitlab.com/scrolliris/scrolliris-console/badges/master/pipeline.svg
[coverage]: https://gitlab.com/scrolliris/scrolliris-console/badges/master/coverage.svg
[commit]: https://gitlab.com/scrolliris/scrolliris-console/commits/master
