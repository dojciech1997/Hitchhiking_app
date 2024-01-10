FROM python:3.10-alpine3.19

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=/app/__init__.py

RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]