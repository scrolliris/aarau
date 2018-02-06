# Neuchâtel

`/nøʃatɛl/`

[![pipeline status][pipeline]][commit]

```txt
 , _                     _                   _
/|/ \                   | |     /\          | |
 |   |   _          __  | |     __, _|_  _  | |
 |   |  |/  |   |  /    |/ \   /  |  |  |/  |/
 |   |_/|__/ \_/|_/\___/|   |_/\_/|_/|_/|__/|__/

Neuchâtel; translatioN projEct Using gnu gettext, it's called neuCHÂTEL
```

This is translation project for the Scrolliris [Application](
https://scrolliris.com/) which called as [Aarau](
https://gitlab.com/scrolliris/aarau) (code name).


## Repository

https://gitlab.com/scrolliris/neuchatel


## Requirements

* Git `>= 2.11.0`
* GNU gettext `>= 0.19.8.1`


## Setup

### OpenBSD

```zsh
;)
```

### GNU/Linux

```zsh
;)

: e.g. Gentoo Linux
% sudo emerge -av dev-vcs/git
% sudo emerge -av sys-devel/gettext
```

### macOS

Try following package managers to install `gettext` (tools)

* https://www.macports.org/
* http://brew.sh/

```
: MacPorts
% sudo port install git gettext

: Homebrew
% brew install git gettext
% brew link --force git
% brew link --force gettext
```

### Windows

TODO


## Compile

Check `Makefile`.

```zsh
% make
```


## Note

### How to apply your changes

Open your `terminal` application, follow these steps, normally.

```zsh
: 0. Fetch and apply new changes from upstream repository
% git pull origin master

: 1. Create a topic branch
% git checkout -b <what-do-you-do>

: 2. Change *.po file at here
% $EDITOR en/LC_MESSAGES/message.po

: 3. Compile as a check of validity (use `make` command described above)
% make

: 4. Commit your changes (Don\'t ad *.mo files)
% git add .
% git commit

: 5. Push your topic branch
% git push origin <what-do-you-do>
```

And then, create a merge request on this [repository](
https://gitlab.com/scrolliris/neuchatel.git).

### How to generate new `*.po` file

Use `./bin/linguine-lite` utility command.

```zsh
% ./bin/linguine-lite generate message de
```

### What's `linguine-lite` command

This is a shell script command for translation files.

```zsh
% ./bin/linguine-lite --help

Usage: linguine-lite <action> <domain> <locale>

The cli command to compile/generate/update gettext catalog files.
...<snip>

Options:
  -h, --help   display this help and exit

Positional arguments:
  <action>   {compile|c},{generate|g},{update|u}
  <domain>   {message,form}
  <locale>   en

Actions:
  compile    compile *.po to *.mo for application
  generate   create new *.po file with latest *.pot
  update     update *.po using *.pot (template)

Examples:
  % linguine-lite update message en
  % linguine-lite g message en
  % linguine-lite c form en
```

### How to compile catalog same condition with CI on local machine

Run **gitlab-ci** localy using `gitlab-ci-multi-runner`.
If you do this, you need docker on linux.

#### Setup

Prepare `gitlab-ci-multi-runner` in your local machine.

```zsh
: gitlab-ci (localy)
% curl -sL https://gitlab-ci-multi-runner-downloads.s3.amazonaws.com \
  /latest/binaries/gitlab-ci-multi-runner-linux-amd64 \
  -o bin/gitlab-ci-multi-runner
% chmod +x bin/gitlab-ci-multi-runner
: run runner container
% docker run -d --name gitlab-runner --restart always \
  -v /srv/gitlab-runner/config:/etc/gitlab-runner \
  gitlab/gitlab-runner:latest
```

#### Run

Start docker as service, then run `ci-runner`.

```zsh
: run docker service
% sudo service docker start

: run compile job in docker (via gitlab-ci-multi-runner)
% ./bin/ci-runner compile

: this is equivalent as above command
% ./bin/gitlab-ci-multi-runner exec docker \
  --cache-dir /cache \
  --docker-volumes `pwd`/build-output:/cache \
  --env <ENVVAR>=... \
  ...
  <JOB>
```

#### links

See documents.

* https://gitlab.com/gitlab-org/gitlab-ci-multi-runner/issues/312
* https://docs.gitlab.com/runner/install/linux-manually.html


## Support

If you have any question, email us `support@scrolliris.com`, or
contact [@scrolliris](https://twitter.com/scrolliris) on Twitter.


## License

This project is distributed as various licenses by parts.

```txt
Neuchâtel
Copyright (c) 2017 Lupine Software LLC
```

### Software (program)

`GPL-3.0`

The programs in this project are distributed as
GNU General Public License. (version 3)

```txt
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
```

### Documentation

`GFDL-1.3`

The translation files (`*.po` and `*.pot`) are distributed as
GNU Free Documentation License. (version 1.3)

```txt
Permission is granted to copy, distribute and/or modify this document
under the terms of the GNU Free Documentation License, Version 1.3
or any later version published by the Free Software Foundation;
with no Invariant Sections, no Front-Cover Texts, and no Back-Cover Texts.
A copy of the license is included in the section entitled "GNU
Free Documentation License".
```

See [LICENSE](LICENSE).


[pipeline]: https://gitlab.com/scrolliris/neuchatel/badges/master/pipeline.svg
[commit]: https://gitlab.com/scrolliris/neuchatel/commits/master
