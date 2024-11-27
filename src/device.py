from utils import setup_argparser, setup_logging
from device import (
    extract_dump,
    compress_file,
    send_file,
    disable_network,
    remove_malware,
    enable_network,
    clean_dump,
)

if __name__ == "__main__":
    setup_logging()
    args = setup_argparser()

    raw_dump_filepath = extract_dump(**vars(args))
    compressed_dump_filepath = compress_file(file_path=raw_dump_filepath)
    response = send_file(file_path=compressed_dump_filepath)

    if response:
        disable_network()
        remove_malware()
        enable_network()

    clean_dump()
