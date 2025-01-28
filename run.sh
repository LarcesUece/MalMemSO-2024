python -m venv venv
source venv/bin/activate
mkdir -p data/csv data/raw data/report data/zip libs
touch app.log
python -m pip install -r requirements.txt
cd libs
wget https://github.com/volatilityfoundation/volatility3/archive/refs/tags/v2.8.0.zip -O volatility3.zip
wget https://github.com/ahlashkari/VolMemLyzer/archive/refs/tags/V2.0.0.zip -O volmemlyzer.zip
unzip volatility3.zip
unzip volmemlyzer.zip
cd ..
python app.py