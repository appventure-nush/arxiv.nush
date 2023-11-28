FROM python:3.9-slim-bookworm

WORKDIR /server
RUN apt-get update \
     && apt-get upgrade -y \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config gnutls-bin
COPY ./server .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "-m", "app"]

# FROM python:3.9-slim-buster

# WORKDIR /server
# RUN apt-get update \
#     && apt-get upgrade -y \
#     && apt-get install -y gcc default-libmysqlclient-dev pkg-config
# COPY ./server .
# RUN pip install -r requirements.txt
# CMD ["python", "-m", "app"]
