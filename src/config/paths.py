"""
Defines and resolves paths used across the application.
"""

from os.path import abspath, dirname, join, pardir, realpath

# src/config/
CONFIG_DIR = abspath(dirname(realpath(__file__)))

# src/
SRC_DIR = abspath(join(CONFIG_DIR, pardir))
MODULES_DIR = abspath(join(SRC_DIR, "modules"))
UTILS_DIR = abspath(join(SRC_DIR, "utils"))

# /
ROOT_DIR = abspath(join(SRC_DIR, pardir))
INI_PATH = abspath(join(ROOT_DIR, "config.ini"))
INI_EXAMPLE_PATH = abspath(join(ROOT_DIR, "config.example.ini"))

# bin/
BIN_DIR = abspath(join(ROOT_DIR, "bin"))

# logs/
LOGS_DIR = abspath(join(ROOT_DIR, "logs"))

# outputs/
OUTPUTS_DIR = abspath(join(ROOT_DIR, "outputs"))
ZIP_DIR = abspath(join(OUTPUTS_DIR, "zip"))
RAW_DIR = abspath(join(OUTPUTS_DIR, "raw"))
