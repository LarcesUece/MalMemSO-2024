"""  
Initialization Module  

This module handles the initialization of the application, including 
setting up logging and parsing command-line arguments.  

Functions:  
    - initialize(): Configures logging and argument parsing.  
"""

from argparse import Namespace

from .config.argparser import setup_argparser
from .config.config import PARSER_DATA
from .config.logging import setup_logging


def initialize() -> Namespace:
    """Initializes the application environment.

    Sets up logging and parses command-line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """

    setup_logging()
    args = setup_argparser(PARSER_DATA)
    return args
