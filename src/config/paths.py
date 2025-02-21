"""
Paths Configuration

This module defines and stores the absolute paths used throughout the 
application. It calculates and stores the locations of various 
directories and files, including configuration files, logs, outputs and 
binaries.

Paths:
    - BIN_DIR: The directory for binary executables.
    - CONFIG_DIR: The directory where the configuration files are 
        located.
    - INI_EXAMPLE_PATH: The absolute path to the example configuration 
        file (config.example.ini).
    - INI_PATH: The absolute path to the main configuration file 
        (config.ini).
    - LOGS_DIR: The directory where logs are stored.
    - MODULES_DIR: The directory containing the modules.
    - OUTPUTS_DIR: The directory where output files are stored.
    - RAW_DIR: The directory where raw output files are stored.
    - ROOT_DIR: The root directory of the project.
    - SRC_DIR: The root source directory of the application.
    - UTILS_DIR: The directory containing utility functions.
    - ZIP_DIR: The directory where zip archives are stored.

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
