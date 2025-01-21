FROM python:3.11-slim

WORKDIR /scraper

COPY ./app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app/ .

CMD ["python3", "__init__.py"]