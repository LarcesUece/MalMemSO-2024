from os.path import dirname, realpath, abspath, join, pardir

# src/utils/
UTILS_PATH = abspath(dirname(realpath(__file__)))

# src/
SRC_PATH = abspath(join(UTILS_PATH, pardir))
CLOUD_PATH = abspath(join(SRC_PATH, "cloud"))
DEVICE_PATH = abspath(join(SRC_PATH, "device"))
FOG_PATH = abspath(join(SRC_PATH, "fog"))
UTILS_PATH = abspath(join(SRC_PATH, "utils"))

# /
ROOT_PATH = abspath(join(SRC_PATH, pardir))
INI_PATH = abspath(join(ROOT_PATH, "config.ini"))
INI_EXAMPLE_PATH = abspath(join(ROOT_PATH, "config.example.ini"))

# bin/
BIN_PATH = abspath(join(ROOT_PATH, "bin"))
EXTRACTION_TOOLS_PATH = abspath(join(BIN_PATH, "extraction_tools"))
X64_PATH = abspath(join(EXTRACTION_TOOLS_PATH, "x64"))
X86_PATH = abspath(join(EXTRACTION_TOOLS_PATH, "x86"))

# libs/
LIBS_PATH = abspath(join(ROOT_PATH, "libs"))
ANALYSIS_TOOLS_PATH = abspath(join(LIBS_PATH, "analysis_tools"))
VOLATILITY_PATH = abspath(join(ANALYSIS_TOOLS_PATH, "volatility3"))
VOLMEMLYZER_PATH = abspath(join(ANALYSIS_TOOLS_PATH, "VolMemLyzer"))

# logs/
LOGS_PATH = abspath(join(ROOT_PATH, "logs"))

# outputs/
OUTPUTS_PATH = abspath(join(ROOT_PATH, "outputs"))
COMPRESSED_DUMPS_PATH = abspath(join(OUTPUTS_PATH, "compressed_dumps"))
DUMP_ANALYSES_PATH = abspath(join(OUTPUTS_PATH, "dump_analyses"))
RAW_DUMPS_PATH = abspath(join(OUTPUTS_PATH, "raw_dumps"))
