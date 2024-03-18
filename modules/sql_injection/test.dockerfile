FROM python:3.12
ENV PYTHONUNBUFFERED 1
COPY ./src /code
COPY ./requirements.txt /
COPY ./pyproject.toml /
RUN pip install -r requirements.txt
