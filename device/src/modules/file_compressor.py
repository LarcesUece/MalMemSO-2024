from zipfile import ZipFile, ZIP_DEFLATED
from time import time
from logging import error, info
from os.path import basename, join, exists

from utils import ZIP_PATH


def compress_file(filepath):
    """Compress a file into a ZIP archive."""

    if not exists(filepath):
        error_message = f"File does not exist at {filepath}."
        error(error_message)
        raise FileNotFoundError(error_message)

    file_name = basename(filepath)
    zip_filepath = join(ZIP_PATH, file_name + ".zip")

    try:
        start = time()
        with ZipFile(join(ZIP_PATH, file_name + ".zip"), "w", ZIP_DEFLATED) as zipf:
            zipf.write(filepath, arcname=file_name)
        end = time()
        duration = end - start
    except Exception as e:
        error_message = f"An error occurred while compressing file: {e}."
        error(error_message)
        raise Exception(error_message)

    info(f"File compressed successfully in {duration:.2f} seconds.")
    return zip_filepath
