"""  
Application Entry Point  

This module serves as the entry point for the application. It 
initializes the environment, extracts a dump file, compresses it, and 
returns the path to the compressed file.  

Functions:  
    - run(): Executes the main process of extraction and compression.  
"""

from src import initialize
from src.modules.dump_extractor import extract_dump
from src.modules.file_compressor import compress_file
from src.modules.file_sender import send_file


def run() -> str:
    """Executes the main workflow of the application.

    Initializes the application environment, extracts a dump file based
    on the provided arguments, compresses it, and returns the path to
    the compressed dump file.

    Returns:
        str: The path to the compressed dump file.
    """

    args = initialize()
    raw_dump_filepath = extract_dump(**vars(args))
    zip_dump_filepath = compress_file(filepath=raw_dump_filepath)
    filename = send_file(filepath=zip_dump_filepath)
    return filename


if __name__ == "__main__":
    run()
