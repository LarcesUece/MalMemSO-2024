FROM python:3.12

RUN apt update -y && apt upgrade -y

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5002

CMD ["python", "app.py"]