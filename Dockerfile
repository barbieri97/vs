FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY . /app

CMD [ "gunicorn", "-b 0.0.0.0:80", "main:app" ]
