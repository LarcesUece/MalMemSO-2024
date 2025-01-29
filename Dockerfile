FROM python:3.10
WORKDIR /app

RUN apt update -y && apt upgrade -y
COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 5000
ENTRYPOINT ["/entrypoint.sh"]
CMD ["flask", "run"]
