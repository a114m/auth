FROM python:3-alpine

RUN apk -U add postgresql-dev gcc musl-dev

WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=app.py

CMD ["flask run --host=0.0.0.0"]
