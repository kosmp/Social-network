FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /home/appuser

# Copy only requirements.txt first to leverage Docker cache
COPY ./requirements.txt /home/appuser/requirements.txt

RUN apt-get update && apt-get install -y default-libmysqlclient-dev

RUN pip install --no-cache-dir -r requirements.txt

COPY . /home/appuser
