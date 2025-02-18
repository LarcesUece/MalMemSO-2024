from logging import error, info
from os.path import basename, exists, join
from time import time
from zipfile import ZIP_DEFLATED, ZipFile

from ..config import ZIP_DIR


def compress_file(filepath: str) -> str:
    """Compresses a file into a ZIP archive.

    Compresses the file at the given path into a ZIP archive and saves
    it in the zip output directory. The compressed file is named after
    the original file with a .zip extension.

    Args:
        filepath (str): Path to the file to compress.

    Returns:
        str: Path to the compressed file.

    Raises:
        FileNotFoundError: If the file does not exist.
        RuntimeError: If an error occurs while compressing the file.
    """

    info("Running dump file compression.")

    if not exists(filepath):
        error_message = f"File does not exist at {filepath}."
        error(error_message)
        raise FileNotFoundError(error_message)

    info("Getting output path for compressed file.")

    file_name = basename(filepath)
    zip_filepath = join(ZIP_DIR, file_name + ".zip")

    info("Compressing file into ZIP archive.")

    try:
        start = time()
        with ZipFile(zip_filepath, "w", ZIP_DEFLATED) as zipf:
            zipf.write(filepath, arcname=file_name)
        end = time()
        duration = end - start
    except Exception as exc:
        error_message = f"An error occurred while compressing file: {exc}."
        error(error_message)
        raise RuntimeError(error_message) from exc

    info(f"File compressed successfully in {duration:.2f} seconds.")
    info(f"Compressed file saved at {zip_filepath}.")

    return zip_filepath
