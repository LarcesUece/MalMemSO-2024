from os.path import join
from zipfile import ZipFile

from app import app
from src import raw


def process_zip_file(file_path, file_id):
    raw_file_path = _unzip_file(file_path)
    raw.process_raw_file(raw_file_path, file_id)


def _unzip_file(file_path):
    unprocessed_raw_dir = app.config.get("UNPROCESSED_RAW_DIR")

    with ZipFile(file_path, "r") as file:
        if len(file.namelist()) != 1:
            raise Exception("Zip file should contain only one file.")
        if not file.namelist()[0].endswith(".raw"):
            raise Exception("Zip file should contain a .raw file.")

        file.extractall(unprocessed_raw_dir)
        raw_file_path = join(unprocessed_raw_dir, file.namelist()[0])
        return raw_file_path
