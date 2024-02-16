#!/bin/bash
python innoter/manage.py migrate
python innoter/manage.py runserver 0.0.0.0:8000
