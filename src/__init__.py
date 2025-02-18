from .config.config import LOGGING_DATA, PARSER_DATA
from .utils.argparser_utils import setup_argparser
from .utils.logging_utils import setup_logging


def initialize():
    setup_logging(LOGGING_DATA)
    args = setup_argparser(PARSER_DATA)
    return args
