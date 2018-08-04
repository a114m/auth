FROM python:3-alpine

WORKDIR /app
COPY ./requirements.txt .
RUN pip install requirements.txt

COPY . .

CMD ["./app.py"]
