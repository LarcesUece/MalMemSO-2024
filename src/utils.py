from os.path import dirname, realpath, abspath, join, pardir

# /
CURRENT_PATH = dirname(realpath(__file__))

# bin/
BIN_PATH = abspath(join(CURRENT_PATH, pardir, "bin"))
X64_PATH = abspath(join(BIN_PATH, "x64"))
X86_PATH = abspath(join(BIN_PATH, "x86"))

# dumps/
DUMPS_PATH = abspath(join(CURRENT_PATH, pardir, "dumps"))
COMPRESSED_PATH = abspath(join(DUMPS_PATH, "compressed"))
RAW_PATH = abspath(join(DUMPS_PATH, "raw"))

# logs/
LOGS_PATH = abspath(join(CURRENT_PATH, pardir, "logs"))
