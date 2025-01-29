FROM python:3.13.1-alpine as builder

COPY . . 

RUN apk add --no-cache gcc musl-dev libffi-dev

RUN pip install poetry

RUN poetry install

CMD ["task", "run"]