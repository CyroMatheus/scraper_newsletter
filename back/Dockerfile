FROM python:3.9-slim

WORKDIR /app

COPY ./app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY /app/ .

EXPOSE 8000

COPY bin/migration.sh /usr/bin

RUN chmod -R +x /usr/bin

RUN migration.sh

CMD ["gunicorn", "back.wsgi:application", "--bind", "0.0.0.0:8000"]
    