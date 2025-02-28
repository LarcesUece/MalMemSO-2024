from datetime import datetime
from os.path import getsize, join
from zipfile import ZipFile

from flask import Flask
from flask import current_app as app

from .. import volmemlyzer
from ..db import db
from .models import Dump


def process_dump(dump_id: int, app: Flask) -> None:
    with app.app_context():
        dump = Dump.query.get(ident=dump_id)
        dump.raw_path = unzip_file(dump_id=dump_id, app=app)
        db.session.commit()
        dump.size = get_raw_size(dump_id=dump_id, app=app)
        db.session.commit()
        report = analyze_dump(dump_id=dump_id, app=app)


def unzip_file(dump_id: int, app: Flask) -> None:
    with app.app_context():
        output_dir = app.config.get("DIR_RAW")
        dump = Dump.query.get(ident=dump_id)
        zip_file_path = dump.zip_path

        with ZipFile(zip_file_path, "r") as zip_file:
            if len(zip_file.namelist()) != 1:
                raise Exception("Zip file should contain only one file.")
            if not zip_file.namelist()[0].endswith(".raw"):
                raise Exception("Zip file should contain a .raw file.")

            zip_file.extractall(path=output_dir)
            raw_file_path = join(output_dir, zip_file.namelist()[0])
            return raw_file_path


def get_raw_size(dump_id: int, app: Flask) -> int:
    with app.app_context():
        dump = Dump.query.get(ident=dump_id)
        size = getsize(dump.raw_path)
        return size


def analyze_dump(dump_id: int, app: Flask) -> None:
    with app.app_context():
        dump = Dump.query.get(dump_id)
        dump.processing_started_at = datetime.now()
        db.session.commit()
        filename = dump.name + ".raw"
        volmemlyzer.run(filename)
        dump.processing_finished_at = datetime.now()
        db.session.commit()
        report = volmemlyzer.get_report_from_csv(filename)
        return report
