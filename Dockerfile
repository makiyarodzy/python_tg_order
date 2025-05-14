FROM python:3.13.1-alpine as builder

COPY . . 

RUN apk add --no-cache curl

RUN curl -sSL https://taskfile.dev/install.sh | sh


RUN curl -LsSf https://astral.sh/uv/install.sh | less

RUN uv sync

CMD ["task", "run"]