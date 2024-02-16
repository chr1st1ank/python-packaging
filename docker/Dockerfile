FROM python:3.11-slim-bookworm

ARG SRC_FOLDER

RUN mkdir -p /app
WORKDIR /app

COPY $SRC_FOLDER/requirements.lock /app/
RUN pip install --no-cache-dir -r requirements.lock

COPY $SRC_FOLDER/dist/*.whl /app/
RUN pip install *.whl && ls -l /app 

EXPOSE 8080

CMD ["langapi"]
