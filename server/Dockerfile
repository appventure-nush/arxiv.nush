FROM python:3.10-alpine

WORKDIR /server
RUN apk add --no-cache --virtual build-deps pkgconf mariadb-dev gcc musl-dev
COPY . .
RUN pip install -r requirements.txt
RUN apk del build-deps
EXPOSE 5000
CMD ["python", "-m", "app"]
