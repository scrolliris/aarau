FROM scrolliris/gentoo:latest
LABEL maintainer "Scrolliris <support@scrolliris.com>"

ARG HOST
ARG PORT
ARG ENV

ADD requirements.txt /app/requirements.txt
ADD constraints.txt /app/constraints.txt
ADD . app/

WORKDIR /app

# venv
RUN python3.6 -m venv /env
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

ENV HOST="${HOST}"
ENV PORT="${PORT}"
ENV ENV="${ENV}"

ENV WSGI_URL_SCHEME http
ENV NO_SQLITE 1

# TODO
RUN npm install && make setup
RUN npm install -g npm i18next-conv && make i18n:compile
RUN npm install -g gulp-cli && make pack

EXPOSE 5000

CMD ["make", "db:init", "db:migrate", "serve"]
