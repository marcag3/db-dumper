FROM python:3.11-alpine
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY app.py ./
RUN apk add --no-cache mariadb-client postgresql-client mysql-client
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
