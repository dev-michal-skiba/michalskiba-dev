FROM python:3.12
ENV PYTHONUNBUFFERED 1

RUN mkdir code
RUN touch code/__init__.py
COPY ./pyproject.toml code/
COPY ./.coveragerc code/

COPY ./requirements.txt code/
COPY ./test.requirements.txt code/
RUN pip install -r code/test.requirements.txt

COPY ./modules/core /code/core
RUN pip install -e /code/core/src/
ENV PYTHONPATH=/code/core/src/core:$PYTHONPATH

COPY ./modules/auth /code/auth
RUN pip install -e /code/auth/src/
ENV PYTHONPATH=/code/auth/src/auth:$PYTHONPATH

COPY ./modules/sql_injection /code/sql_injection
RUN pip install -e /code/sql_injection/src/
ENV PYTHONPATH=/code/sql_injection/src/sql_injection:$PYTHONPATH

COPY ./modules/web_parameter_tampering /code/web_parameter_tampering
RUN pip install -e /code/web_parameter_tampering/src/
ENV PYTHONPATH=/code/web_parameter_tampering/src/web_parameter_tampering:$PYTHONPATH

COPY ./modules/host_header_injection /code/host_header_injection
RUN pip install -e /code/host_header_injection/src/
ENV PYTHONPATH=/code/host_header_injection/src/host_header_injection:$PYTHONPATH

WORKDIR /code
