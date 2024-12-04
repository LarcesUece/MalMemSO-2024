from os.path import dirname, realpath, abspath, join, pardir

# src/utils/
UTILS_PATH = abspath(dirname(realpath(__file__)))

# src/
SRC_PATH = abspath(join(UTILS_PATH, pardir))
MODULES_PATH = abspath(join(SRC_PATH, "modules"))

# /
ROOT_PATH = abspath(join(SRC_PATH, pardir))
INI_PATH = abspath(join(ROOT_PATH, "config.ini"))
INI_EXAMPLE_PATH = abspath(join(ROOT_PATH, "config.example.ini"))

# bin/
BIN_PATH = abspath(join(ROOT_PATH, "bin"))

# logs/
LOGS_PATH = abspath(join(ROOT_PATH, "logs"))

# outputs/
OUTPUTS_PATH = abspath(join(ROOT_PATH, "outputs"))
ZIP_PATH = abspath(join(OUTPUTS_PATH, "zip"))
RAW_PATH = abspath(join(OUTPUTS_PATH, "raw"))
