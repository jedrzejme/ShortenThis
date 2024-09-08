FROM python:3.12.1

WORKDIR /app

COPY . /app/

RUN touch /app/database.db

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run"]