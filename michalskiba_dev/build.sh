#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
mkdir static/blog/posts

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py migrate --database=web_parameter_tampering
python manage.py detect_new_raw_files.py
python manage.py detect_new_post_files.py
