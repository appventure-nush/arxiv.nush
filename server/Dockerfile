FROM python:3.9-slim-buster

WORKDIR /home/arxiv.nush/server


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "-m", "app.py"]