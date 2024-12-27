import logging
from logging import basicConfig, INFO


def setup():
    basicConfig(
        filename="app.log",
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
        level=INFO,
        encoding="utf-8",
    )
