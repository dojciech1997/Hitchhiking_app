FROM python:3.10-alpine3.19

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP="/app/app/__init__.py"

CMD ["flask", "run", "--host=0.0.0.0"]