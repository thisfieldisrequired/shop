# Pull official base Python Docker image
FROM python:3.10.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

# Install dependencies
RUN apt-get update
RUN curl https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

RUN adduser app && usermod -aG sudo app

RUN chown -R app:app /code/

COPY ./pyproject.toml ./poetry.lock* /code/

RUN poetry install

# Copy the Django project
COPY . /code/
