FROM python:3.12
ENV PYTHONUNBUFFERED 1

RUN mkdir code
RUN touch code/__init__.py
COPY ./pyproject.toml code/
COPY ./.coveragerc code/

COPY ./requirements.test.txt code/
RUN pip install -r code/requirements.test.txt

COPY ./modules/core /code/core
RUN pip install -e /code/core/src/
RUN [ -f /code/core/src/requirements.txt ] && pip install -r /code/core/src/requirements.txt || echo "No requirements.txt found for core"
ENV PYTHONPATH=/code/core/src/core:$PYTHONPATH

COPY ./modules/auth /code/auth
RUN pip install -e /code/auth/src/
RUN [ -f /code/auth/src/requirements.txt ] && pip install -r /code/auth/src/requirements.txt || echo "No requirements.txt found for auth"
ENV PYTHONPATH=/code/auth/src/auth:$PYTHONPATH

COPY ./modules/sql_injection /code/sql_injection
RUN pip install -e /code/sql_injection/src/
RUN [ -f /code/sql_injection/src/requirements.txt ] && pip install -r /code/sql_injection/src/requirements.txt || echo "No requirements.txt found for sql_injection"
ENV PYTHONPATH=/code/sql_injection/src/sql_injection:$PYTHONPATH

COPY ./modules/web_parameter_tampering /code/web_parameter_tampering
RUN pip install -e /code/web_parameter_tampering/src/
RUN [ -f /code/web_parameter_tampering/src/requirements.txt ] && pip install -r /code/web_parameter_tampering/src/requirements.txt || echo "No requirements.txt found for web_parameter_tampering"
ENV PYTHONPATH=/code/web_parameter_tampering/src/web_parameter_tampering:$PYTHONPATH

COPY ./modules/host_header_injection /code/host_header_injection
RUN pip install -e /code/host_header_injection/src/
RUN [ -f /code/host_header_injection/src/requirements.txt ] && pip install -r /code/host_header_injection/src/requirements.txt || echo "No requirements.txt found for host_header_injection"
ENV PYTHONPATH=/code/host_header_injection/src/host_header_injection:$PYTHONPATH

WORKDIR /code
