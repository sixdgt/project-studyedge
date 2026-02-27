FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /home/studyedge

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies as root first
RUN python -m pip install --upgrade pip && \
    pip install gunicorn pipenv

# Copy project files
COPY . /home/studyedge/

# Install project dependencies
RUN pipenv install --deploy --ignore-pipfile --system

# Make entrypoint executable
RUN chmod +x /home/studyedge/entrypoint.sh

# Create user (Debian syntax, NOT Alpine -D flag)
RUN adduser --home /home/studyedge \
            --shell /bin/bash \
            --disabled-password \
            --gecos "" \
            --uid 2000 \
            studyedge

# Transfer ownership AFTER all files are copied
RUN chown -R studyedge:studyedge /home/studyedge

# Switch to non-root user
USER studyedge

ENTRYPOINT ["/bin/sh", "/home/studyedge/entrypoint.sh"]