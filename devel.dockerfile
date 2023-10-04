FROM python:3.12.0
ENV PYTHONUNBUFFERED 1
COPY michalskiba_dev /code
WORKDIR /code
RUN pip install -r requirements.txt
