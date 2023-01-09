FROM python:latest

ENV PYTHONUNBUFFERED=1
WORKDIR /opt/django-backend
COPY ./Pipfile ./Pipfile.lock .

RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

EXPOSE 8000

CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]