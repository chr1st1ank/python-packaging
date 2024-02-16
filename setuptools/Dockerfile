FROM python:3.11-slim-bookworm

RUN mkdir -p /app
WORKDIR /app

COPY requirements.lock /app/
RUN pip install --no-cache-dir -r requirements.lock

COPY dist/*.whl /app/
RUN pip install *.whl && ls -l /app 

EXPOSE 8080

CMD ["langapi"]
