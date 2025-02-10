from dotenv import load_dotenv
import os


class Config:
    load_dotenv(".env")

    DIR_SRC = os.path.dirname(os.path.abspath(__file__))
    DIR_ROOT = os.path.join(DIR_SRC, os.pardir)
    DIR_DATA = os.path.join(DIR_ROOT, "data")
    DIR_INITIAL_DATA = os.path.join(DIR_DATA, "initial_data")
    DIR_PICKLE = os.path.join(DIR_DATA, "pickle")
    DIR_LIBS = os.path.join(DIR_ROOT, "libs")
    DIR_VOLATILITY = os.path.join(DIR_LIBS, "volatility3")
    DIR_VOLMEMLYZER = os.path.join(DIR_LIBS, "volmemlyzer")

    TABLE_REPORT = "reports"
    TABLE_FILE = "files"
    TABLE_MODEL = "models"

    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")

    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TZ = "UTC"
    LOCAL_TZ = os.getenv("LOCAL_TZ", "UTC")

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
        "report_file_class",
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

    VOLMEMLYZER_NEW_VOL_MODULES = """
        {
            # 'info': extract_winInfo_features,
            "pslist": extract_pslist_features,
            "dlllist": extract_dlllist_features,
            "handles": extract_handles_features,
            "ldrmodules": extract_ldrmodules_features,
            "malfind": extract_malfind_features,
            "modules": extract_modules_features,
            "callbacks": extract_callbacks_features,
            # 'cmdline': extract_cmdline_features,
            # 'devicetree': extract_devicetree_features,
            # 'driverirp': extract_driverirp_features,
            # 'drivermodule': extract_drivermodule_features,
            # 'driverscan': extract_driverscan_features,
            #####'dumpfiles': extract_dumpfiles_features,        # Creates Junk files in the Folder where VolMemLyzer is present [TRY NOT TO USE]
            # 'envars': extract_envars_features,
            # 'filescan': extract_filescan_features,
            # 'getsids': extract_getsids_features,
            # 'mbrscan': extract_mbrscan_features,
            #####'memmap': extract_memmap_features,             # Volatility Incompatibility [DO NOT USE]
            # 'mftscan': extract_mftscan_features,
            # 'modscan': extract_modscan_features,
            # 'mutantscan': extract_mutantscan_features,
            # 'netscan': extract_netscan_features,
            # 'netstat': extract_netstat_features,
            # 'poolscanner': extract_poolscanner_features,
            # 'privileges': extract_privileges_features,
            # 'pstree': extract_pstree_features,
            # 'registry.certificates': extract_registry_certificates_features,
            # 'registry.hivelist': extract_registry_hivelist_features,
            # 'registry.hivescan': extract_registry_hivescan_features,
            # 'registry.printkey': extract_registry_printkey_features,
            # 'registry.userassist': extract_registry_userassist_features,
            # 'sessions': extract_sessions_features,
            # 'skeleton_key': extract_skeleton_key_features,
            # 'ssdt': extract_ssdt_features,
            # 'statistics': extract_statistics_features,
            "svcscan": extract_svcscan_features,
            # 'symlinkscan': extract_symlinkscan_features,
            # 'vadinfo': extract_vadinfo_features,
            # 'vadwalk': extract_vadwalk_features,
            # 'verinfo': extract_verinfo_features,
            # 'virtmap': extract_virtmap_features
        }
        """

    TRAINING_ALGORITHMS = [
        "cart",
        "knn",
        "mlp",
        "rf",
        #    "svm"
    ]
