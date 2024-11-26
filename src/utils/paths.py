from os.path import dirname, realpath, abspath, join, pardir

# src/
SRC_PATH = abspath(join(dirname(realpath(__file__)), pardir))

# /
ROOT_PATH = abspath(join(SRC_PATH, pardir))
INI_PATH = abspath(join(ROOT_PATH, "config.ini"))

# bin/
BIN_PATH = abspath(join(ROOT_PATH, "bin"))
X64_PATH = abspath(join(BIN_PATH, "x64"))
X86_PATH = abspath(join(BIN_PATH, "x86"))

# dumps/
DUMPS_PATH = abspath(join(ROOT_PATH, "dumps"))
COMPRESSED_PATH = abspath(join(DUMPS_PATH, "compressed"))
RAW_PATH = abspath(join(DUMPS_PATH, "raw"))

# logs/
LOGS_PATH = abspath(join(ROOT_PATH, "logs"))
