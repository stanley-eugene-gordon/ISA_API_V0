FROM python:alpine

WORKDIR /code
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/code

COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt

# Copy code and .env
COPY api_v0/ code/
COPY .env .env

EXPOSE 5000

CMD ["python3", "code/main.py"]
