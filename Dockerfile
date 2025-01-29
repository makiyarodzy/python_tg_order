FROM python:3.13.1-alpine as builder

COPY . . 

RUN pip install -r requirements.txt

CMD ["task" "run"]