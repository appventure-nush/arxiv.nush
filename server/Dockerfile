FROM python:3.9-slim-buster

WORKDIR /server

COPY ./server .
RUN pip install -r requirements.txt

CMD ["python", "-m", "app.py"]