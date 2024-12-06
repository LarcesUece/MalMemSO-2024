from utils import setup_argparser, setup_logging
from modules import (
    extract_dump,
    compress_file,
    send_file,
    disable_network,
    remove_malware,
    enable_network,
    clean_dump,
)
from config import (
    SERVER_DATA,
    PARSER_DATA,
    LOGGING_DATA,
)

if __name__ == "__main__":
    setup_logging(LOGGING_DATA)
    args = setup_argparser(PARSER_DATA)

    raw_dump_filepath = extract_dump(**vars(args))
    # compressed_dump_filepath = compress_file(raw_dump_filepath)
    # response = send_file(compressed_dump_filepath, SERVER_DATA)

    # if response:
    #     disable_network()
    #     remove_malware()
    #     enable_network()

    # clean_dump()
