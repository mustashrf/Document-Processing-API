FROM python:latest

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN git clone https://github.com/mustashrf/Document-Processing-System.git /app

RUN pip install -r requirements.txt

EXPOSE 8000

RUN python manage.py makemigrations api

RUN python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]