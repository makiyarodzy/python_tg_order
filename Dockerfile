FROM python:3.13.1-alpine as builder

COPY . . 

RUN apk add --no-cache curl

RUN curl -sSL https://taskfile.dev/install.sh | sh

RUN pip install poetry

RUN poetry install

CMD ["task", "run"]