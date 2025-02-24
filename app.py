"""
Main module to run the memory dump extraction, compression and sending 
process.

Functions:
    run: Executes the full pipeline from extraction to sending the 
        compressed dump.
"""

from src import initialize
from src.modules.dump_extractor import extract_dump
from src.modules.file_compressor import compress_file
from src.modules.file_sender import send_file


def run() -> str:
    """Runs the extraction, compression, and sending process.

    Returns:
        str: The name of the sent file.
    """
    args = initialize()
    raw_dump_filepath = extract_dump(**vars(args))
    zip_dump_filepath = compress_file(filepath=raw_dump_filepath)
    filename = send_file(filepath=zip_dump_filepath)
    return filename


if __name__ == "__main__":
    run()
