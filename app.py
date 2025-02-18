from src import initialize
from src.modules.dump_extractor import extract_dump
from src.modules.file_compressor import compress_file


def run():
    args = initialize()
    raw_dump_filepath = extract_dump(**vars(args))
    zip_dump_filepath = compress_file(raw_dump_filepath)
    return zip_dump_filepath


if __name__ == "__main__":
    run()
