FROM python:3.11.3
ENV PYTHONUNBUFFERED 1
COPY ./app /app
WORKDIR /app
RUN pip install -r requirements.txt
