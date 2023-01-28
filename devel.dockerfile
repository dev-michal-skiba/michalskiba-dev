FROM python:3.11.1
ENV PYTHONUNBUFFERED 1
COPY michalskiba_dev /code
WORKDIR /code
RUN pip install -r requirements.txt
