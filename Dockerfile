FROM python:3.12

RUN apt update -y && apt upgrade -y

WORKDIR /app

COPY src src
COPY app.py app.py
COPY config.py config.py
COPY requirements.txt requirements.txt

RUN mkdir -p data/csv data/raw data/symbols data/zip libs
RUN touch app.log

RUN pip install -r requirements.txt

WORKDIR /app/libs

RUN wget https://github.com/volatilityfoundation/volatility3/archive/refs/tags/v2.8.0.zip -O volatility3.zip
RUN wget https://github.com/ahlashkari/VolMemLyzer/archive/refs/tags/V2.0.0.zip -O volmemlyzer.zip

RUN unzip volatility3.zip
RUN unzip volmemlyzer.zip

WORKDIR /app

EXPOSE 5000

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--debug"]