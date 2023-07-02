FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY licensas.txt /app
COPY main.py /app
COPY /templates /app/templates

CMD [ "gunicorn", "-b 0.0.0.0:80", "main:app" ]
