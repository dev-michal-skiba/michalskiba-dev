FROM python:3.12
ENV PYTHONUNBUFFERED=1

RUN mkdir /code
RUN touch /code/__init__.py

COPY ./modules /code
COPY ./pyproject.toml /code/pyproject.toml
COPY ./.coveragerc /code/.coveragerc
COPY ./requirements.test.txt /code/requirements.test.txt
RUN pip install -r /code/requirements.test.txt

RUN for module in $(find /code -maxdepth 1 -mindepth 1 -type d -exec basename {} \; | grep -v '^[.]'); do \
    if [ -f "/code/$module/.env.test" ]; then \
        echo "Processing module: $module" && \
        pip install -e "/code/$module/src/" && \
        ([ -f "/code/$module/src/requirements.txt" ] && pip install -r "/code/$module/src/requirements.txt" || echo "No requirements.txt found for $module") && \
        export PYTHONPATH="/code/$module/src/$module:$PYTHONPATH"; \
    fi \
    done
ENV PYTHONPATH=$PYTHONPATH

WORKDIR /code
