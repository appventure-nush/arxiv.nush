FROM python:3.9-slim-buster as builder

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config python

COPY . .
RUN pwd && ls -l

FROM nginx:alpine
EXPOSE 80
COPY --from=builder /dist /usr/share/nginx/html

FROM python:3.9-slim-buster

WORKDIR /server
RUN pip install -r requirements.txt
CMD ["python", "-m", "app"]