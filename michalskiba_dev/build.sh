#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
mkdir static/blog/posts

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py migrate --database=web_parameter_tampering
