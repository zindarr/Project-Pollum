FROM python:3.10.10

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

# CMD ["python", "-u", "main.py"]

CMD ["uvicorn", "--host", "127.0.0.1", "--port", "8000", "main:app"]