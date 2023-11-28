FROM python:3.10-alpine

WORKDIR /server
RUN apk add --no-cache pkgconf mariadb-dev gcc musl-dev
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "-m", "app"]
