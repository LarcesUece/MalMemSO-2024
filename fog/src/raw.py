import shutil
import os

from app import app
from src import volmemlyzer


def process_raw_file(file_path, file_id):
    updated_vol_modules = app.config["UPDATED_VOL_MODULES"]
    volmemlyzer_file = app.config["VOLMEMLYZER_FILE"]
    csv_output = f"{file_id}.csv"

    processing_file_path = _move_raw(file_path)
    volmemlyzer.edit_vol_modules(volmemlyzer_file, updated_vol_modules)
    volmemlyzer.edit_output_file(volmemlyzer_file, csv_output)
    volmemlyzer.run()
    processed_file_path = _move_raw(processing_file_path, processed=True)

    return processed_file_path


def _move_raw(file_path, processed=False):
    new_dir = (
        app.config["PROCESSED_RAW_DIR"]
        if processed
        else app.config["PROCESSING_RAW_DIR"]
    )

    shutil.move(file_path, new_dir)
    new_file_path = os.path.join(new_dir, os.path.basename(file_path))
    return new_file_path
