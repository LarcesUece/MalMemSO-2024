from dotenv import load_dotenv
import os


class Config:
    load_dotenv(".env")

    SRC_DIR = os.path.dirname(os.path.abspath(__file__))
    ROOT_DIR = os.path.join(SRC_DIR, os.pardir)
    DATA_DIR = os.path.join(ROOT_DIR, "data")
    INITIAL_DATA_DIR = os.path.join(DATA_DIR, "initial_data")

    TABLE_ANALYSIS = "analyses"
    TABLE_FILE = "files"
    TABLE_MODEL = "models"

    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")

    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TZ = os.getenv("TZ", "UTC")

    VOLMEMLYZER_OLD_COLUMNS = [
        "Category",
        "Class",
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

    VOLMEMLYZER_NEW_COLUMNS = [
        "mem.name_extn",
        "analysis_file_class",
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

    VOLMEMLYZER_COLUMN_MAPPING = {
        old: new
        for old, new in zip(VOLMEMLYZER_OLD_COLUMNS, VOLMEMLYZER_NEW_COLUMNS)
        if new is not None
    }
