from utils import setup_argparser, setup_logging
from dump_extractor import extract_dump


if __name__ == "__main__":
    setup_logging()
    args = setup_argparser()
    extract_dump(**vars(args))
