# syntax=docker/dockerfile:1
FROM python:3.8-alpine
WORKDIR /backend
#ENV FLASK_APP=backend/app.py
#ENV FLASK_RUN_HOST=0.0.0.0
#RUN apk add --no-cache gcc musl-dev linux-headers
RUN apk update && apk add postgresql-dev make gcc libc-dev python3-dev musl-dev libffi-dev openssl-dev cargo
RUN pip install psycopg2
RUN pip install greenlet
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
#EXPOSE 5000
COPY .. .
CMD ["python", "app.py"]