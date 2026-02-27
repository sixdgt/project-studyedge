FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /home/studyedge

RUN apt update
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# creating user inside docker
RUN adduser -h /home/studyedge -s /bin/bash -D -u 2000 studyedge
RUN chown -R studyedge:studyedge /home/studyedge
USER studyedge

COPY . /home/studyedge
# making the file executable
RUN chmod +x /home/studyedge/entrypoint.sh

RUN python -m pip install --upgrade pip
RUN pip install gunicorn
RUN pip install pipenv
RUN pipenv install --deploy --ignore-pipfile --system