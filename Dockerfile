# Stage 1: Build dependencies
FROM python:3.12 AS builder

WORKDIR /usr/src/app

# Copy only requirements.txt first to leverage Docker cache
COPY ./requirements.txt /usr/src/app/requirements.txt

# Install system dependencies
RUN apt-get update && apt-get install -y default-libmysqlclient-dev

# Stage 2: Final image
FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

# Install Python dependencies
COPY --from=builder /usr/src/app/requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files from the innoter directory to the main directory
COPY . /usr/src/app

WORKDIR /usr/src/app/innoter
