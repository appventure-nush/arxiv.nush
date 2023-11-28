FROM python:3.10-alpine AS build

WORKDIR /server
RUN apk add --no-cache --virtual build-deps pkgconf mariadb-dev gcc musl-dev

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt


FROM python:3.10-alpine AS runtime

WORKDIR /server
RUN apk add --no-cache mariadb-connector-c

COPY --from=build /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . .
EXPOSE 5000
CMD ["python", "-m", "app"]
