FROM nginx:alpine
EXPOSE 80

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config


COPY . .
RUN pwd && ls -l


COPY /dist /usr/share/nginx/html

WORKDIR /server
RUN pip install -r requirements.txt
CMD ["python", "-m", "app"]