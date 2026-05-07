FROM python:3.12-alpine

ENV PATH="${PATH}:/root/.local/bin"
COPY ./src /app/src
COPY main.py /app/
COPY entrypoint.sh /app/
COPY alembic /app/alembic
COPY alembic.ini /app/
COPY pyproject.toml /app/
COPY requirements.txt /app/
COPY tests /app/tests

ENV PYTHONPATH /app/src
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod +x /app/entrypoint.sh
RUN mkdir -p /app/images

EXPOSE 8000
