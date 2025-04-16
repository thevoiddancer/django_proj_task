FROM python:3.11.11-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update
RUN apt-get install -y --no-install-recommends curl git build-essential
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.2.2

RUN git clone https://oauth2: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@github.com/thevoiddancer/django_proj_task.git
WORKDIR /usr/src/app/django_proj_task

RUN /root/.local/bin/poetry install

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
