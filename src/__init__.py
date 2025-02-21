"""  
Initialization Module  

This module handles the initialization of the application, including 
setting up logging and parsing command-line arguments.  

Functions:  
    - initialize(): Configures logging and argument parsing.  
"""

from argparse import Namespace

from .config.argparser import setup_argparser
from .config.logging import setup_logging
from .utils.utils import check_supported_os


def initialize() -> Namespace:
    """Initializes the application environment.

    Sets up logging and parses command-line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """

    setup_logging()
    check_supported_os()
    args = setup_argparser()
    return args
