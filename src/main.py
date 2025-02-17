from time import sleep

from modules import (
    extract_dump,
    compress_file,
    send_file,
    get_response,
    disable_network,
    remove_malware,
    enable_network,
    clean_dump,
)
from config import SERVER_DATA, ENDPOINT_DATA, initialize

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
