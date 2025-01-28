FROM python:3.12

WORKDIR /app

COPY . .

RUN apt update -y && apt upgrade -y

RUN pip install -r requirements.txt

EXPOSE 5002

WORKDIR /app/src

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5002"]