FROM python:3.10-alpine3.19

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=/app/__init__.py

CMD ["flask", "db", "init"]
CMD ["flask", "db", "migrate"]
CMD ["flask", "db", "upgrade"]

CMD ["flask", "run", "--host=0.0.0.0"]