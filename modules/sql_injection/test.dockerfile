FROM python:3.12
ENV PYTHONUNBUFFERED 1
COPY ./ /code
WORKDIR /code
RUN pip install -r test.requirements.txt
RUN pip install -e src/
ENV PYTHONPATH=/code/src/sql_injection:$PYTHONPATH
