FROM python:3.10
WORKDIR /app
EXPOSE 5000

RUN apt update -y && apt upgrade -y && apt install -y wget unzip

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["flask", "run"]
