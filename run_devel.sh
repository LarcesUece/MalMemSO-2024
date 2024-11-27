mkdir -p libs/analysis_tools logs outputs/compressed_dumps outputs/dump_analyses outputs/raw_dumps
mv config.example.ini config.ini
cd libs/analysis_tools
git clone https://github.com/volatilityfoundation/volatility3.git
git clone https://github.com/ahlashkari/VolMemLyzer.git
cd ..
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt