FROM python:3.10
WORKDIR /app
EXPOSE 5000

RUN apt update -y && apt upgrade -y && apt install -y wget unzip

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

COPY src data .env app.py requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["flask", "run"]
