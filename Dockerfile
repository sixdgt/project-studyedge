FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

RUN apt update
RUN apt-get install -y libpq-dev gcc && rm -rf /var/apt/lists/*

# creating user inside docker
RUN adduser -h /home/studyedge -s /bin/bash -D -u 2000 studyedge
WORKDIR /home/studyedge
COPY . /home/studyedge
# making the file executable
RUN chmod +x /home/studyedge/entrypoint.sh

RUN python -m pip install --upgrade pip
RUN pip install gunicorn
RUN pip install pipenv
RUN pipenv install --deploy --ignore-pipfile --system
RUN python manage.py collectstatic --noinput
RUN python manage.py tailwindcss build ./theme/static_src/css/tailwind.css -o ./theme/static/css/tailwind.css
