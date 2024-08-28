FROM python:3.12.1

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod 644 /app/config.ini

RUN chmod 644 /app/urls.ini

EXPOSE 6700

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run"]