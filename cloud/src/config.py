from dotenv import load_dotenv
from os.path import join, dirname, abspath
from os import getenv, pardir

# Directories paths
SRC_DIR = dirname(abspath(__file__))
ROOT_DIR = join(SRC_DIR, pardir)
DATA_DIR = join(ROOT_DIR, "csv")

# Files paths
INITIAL_DATA_FILES = [
    join(DATA_DIR, "Obfuscated-MalMem2022.csv"),
    join(DATA_DIR, "Output1.csv"),
    join(DATA_DIR, "output2.csv"),
    join(DATA_DIR, "output3.csv"),
]
ENV_FILE = join(ROOT_DIR, ".env")

# Tables names
DATA_TABLE = "data"
MODEL_TABLE = "model"

# Database variables
load_dotenv(ENV_FILE)
DB_USER = getenv("POSTGRES_USER")
DB_PASS = getenv("POSTGRES_PASSWORD")
DB_HOST = getenv("POSTGRES_HOST")
DB_PORT = getenv("PORTGRES_PORT")
DB_NAME = getenv("POSTGRES_DB")

# VolMemLyzer features
FEATURES_VOLMEMLYZER_V2 = [
    "callbacks.nanonymous",
    "callbacks.ncallbacks",
    "callbacks.ngeneric",
    "dlllist.avg_dlls_per_proc",
    "dlllist.ndlls",
    "handles.avg_handles_per_proc",
    "handles.ndesktop",
    "handles.ndirectory",
    "handles.nevent",
    "handles.nfile",
    "handles.nhandles",
    "handles.nkey",
    "handles.nmutant",
    "handles.nport",
    "handles.nsection",
    "handles.nsemaphore",
    "handles.nthread",
    "handles.ntimer",
    "ldrmodules.not_in_init",
    "ldrmodules.not_in_init_avg",
    "ldrmodules.not_in_load",
    "ldrmodules.not_in_load_avg",
    "ldrmodules.not_in_mem",
    "ldrmodules.not_in_mem_avg",
    "malfind.commitCharge",
    "malfind.ninjections",
    "malfind.protection",
    "malfind.uniqueInjections",
    "modules.nmodules",
    "pslist.avg_handlers",
    "pslist.avg_threads",
    "pslist.nppid",
    "pslist.nproc",
    "pslist.nprocs64bit",
    "psxview.not_in_csrss_handles",
    "psxview.not_in_csrss_handles_false_avg",
    "psxview.not_in_deskthrd",
    "psxview.not_in_deskthrd_false_avg",
    "psxview.not_in_eprocess_pool",
    "psxview.not_in_eprocess_pool_false_avg",
    "psxview.not_in_ethread_pool",
    "psxview.not_in_ethread_pool_false_avg",
    "psxview.not_in_pslist",
    "psxview.not_in_pslist_false_avg",
    "psxview.not_in_pspcid_list",
    "psxview.not_in_pspcid_list_false_avg",
    "psxview.not_in_session",
    "psxview.not_in_session_false_avg",
    "svcscan.fs_drivers",
    "svcscan.interactive_process_services",
    "svcscan.kernel_drivers",
    "svcscan.nactive",
    "svcscan.nservices",
    "svcscan.process_services",
    "svcscan.shared_process_services",
]

FEATURES_VOLMEMLYZER_V2_2024 = [
    None,
    "callbacks.ncallbacks",
    None,
    "dlllist.avg_dllPerProc",
    "dlllist.ndlls",
    "handles.avgHandles_per_proc",
    "handles.nTypeDesk",
    "handles.nTypeDir",
    "handles.nTypeEvent",
    "handles.nTypeFile",
    "handles.nHandles",
    "handles.nTypeKey",
    "handles.nTypeMutant",
    "handles.nTypePort",
    "handles.nTypeSec",
    "handles.nTypeSemaph",
    "handles.nTypeThread",
    "handles.nTypeTimer",
    "ldrmodules.not_in_init",
    "ldrmodules.not_in_init_avg",
    "ldrmodules.not_in_load",
    "ldrmodules.not_in_load_avg",
    "ldrmodules.not_in_mem",
    "ldrmodules.not_in_mem_avg",
    "malfind.commitCharge",
    "malfind.ninjections",
    "malfind.protection",
    "malfind.uniqueInjections",
    "modules.nmodules",
    "pslist.avg_handlers",
    "pslist.avg_threads",
    "pslist.nppid",
    "pslist.nproc",
    "pslist.nprocs64bit",
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    "svcscan.Type_FileSys_Driver",
    None,
    "svcscan.Type_Kernel_Driver",
    "svcscan.State_Run",
    "svcscan.nServices",
    "svcscan.Type_Own",
    "svcscan.Type_Share",
]

COLUMN_FILENAME_NAME = "mem.name_extn"

# Table columns names and optional types
DATA_COLUMNS_NAMES = ["Class", COLUMN_FILENAME_NAME] + [
    old
    for old, new in zip(FEATURES_VOLMEMLYZER_V2, FEATURES_VOLMEMLYZER_V2_2024)
    if new is None
]

MODEL_COLUMNS_NAMES_TYPES = [
    ("algorithm", "TEXT"),
    ("model_pickle", "BYTEA"),
    ("accuracy", "DOUBLE PRECISION"),
    ("precision", "DOUBLE PRECISION"),
    ("recall", "DOUBLE PRECISION"),
    ("f1", "DOUBLE PRECISION"),
    ("init_time", "TIMESTAMPTZ"),
    ("end_time", "TIMESTAMPTZ"),
    ("training_duration", "INTERVAL"),
]

# Timestamps timezone
PYTZ_TIMEZONE = "UTC"

# Training algorithms available
ALGORITHMS = ["cart", "knn", "mlp", "rf", "svm"]
