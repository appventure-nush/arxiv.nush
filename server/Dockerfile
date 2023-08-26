FROM python:3.9-slim-buster as builder

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config
WORKDIR /frontend

FROM nginx:alpine
EXPOSE 80
COPY --from=builder /frontend/dist /usr/share/nginx/html

WORKDIR /server
RUN pip install -r requirements.txt
CMD ["python", "-m", "app"]