"""
Initialization module to set up logging, check OS support and parse 
arguments.

Functions:
    initialize: Sets up the environment and returns parsed arguments.
"""

from argparse import Namespace

from .config.argparser import setup_argparser
from .config.logging import setup_logging
from .utils.system import check_supported_os


def initialize() -> Namespace:
    """Initializes logging, checks OS and parses command-line arguments.

    Returns:
        argparser.Namespace: Parsed command-line arguments.
    """

    setup_logging()
    check_supported_os()
    args = setup_argparser()
    return args
