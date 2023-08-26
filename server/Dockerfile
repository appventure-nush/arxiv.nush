FROM python:3.9-slim-buster as builder

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash - 
RUN apt-get install -y nodejs

WORKDIR /frontend

COPY package.json .
COPY . .
RUN npm run build


FROM nginx:alpine
EXPOSE 80
COPY --from=builder /frontend/dist /usr/share/nginx/html

WORKDIR /server
RUN pip install -r requirements.txt
CMD ["python", "-m", "app"]