# Stage 1: Build dependencies
FROM python:3.12 AS builder

WORKDIR /home/appuser

# Copy only requirements.txt first to leverage Docker cache
COPY ./requirements.txt /home/appuser/requirements.txt

# Install system dependencies
RUN apt-get update && apt-get install -y default-libmysqlclient-dev

RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final image
FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /home/appuser

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

COPY . /home/appuser
