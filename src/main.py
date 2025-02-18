from argparse import Namespace

from .modules import (
    extract_dump,
    compress_file,
    send_file,
    get_response,
    disable_network,
    remove_malware,
    enable_network,
    clean_dump,
)
from .config import (
    SERVER_DATA,
    BIN_DIR,
    LOGS_DIR,
    RAW_DIR,
    ZIP_DIR,
    PARSER_DATA,
    LOGGING_DATA,
    # ENDPOINT_DATA,
)
from .utils import create_dir, setup_logging, setup_argparser


def initialize() -> Namespace:
    create_dir(BIN_DIR)
    create_dir(LOGS_DIR)
    create_dir(RAW_DIR)
    create_dir(ZIP_DIR)

    setup_logging(LOGGING_DATA)
    args = setup_argparser(PARSER_DATA)
    return args


def main():
    args = initialize()

    raw_dump_filepath = extract_dump(**vars(args))
    compressed_dump_filepath = compress_file(raw_dump_filepath)
    filename = send_file(compressed_dump_filepath, SERVER_DATA, ENDPOINT_DATA)
    response = get_response(filename, SERVER_DATA, ENDPOINT_DATA)

    # if response:
    #     disable_network()
    #     remove_malware()
    #     enable_network()

    # clean_dump()


if __name__ == "__main__":
    main()
