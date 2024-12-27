from os.path import dirname, abspath, join


class Config:
    ROOT_DIR = dirname(abspath(__file__))
    DATA_DIR = join(ROOT_DIR, "data")
    CSV_DIR = join(DATA_DIR, "csv")
    RAW_DIR = join(DATA_DIR, "raw")
    PROCESSED_RAW_DIR = join(RAW_DIR, "processed")
    PROCESSING_RAW_DIR = join(RAW_DIR, "processing")
    UNPROCESSED_RAW_DIR = join(RAW_DIR, "unprocessed")
    REPORT_DIR = join(DATA_DIR, "report")
    ZIP_DIR = join(DATA_DIR, "zip")
    LIBS_DIR = join(ROOT_DIR, "libs")
    SRC_DIR = join(ROOT_DIR, "src")

    REPORT_FILE = join(REPORT_DIR, "report.csv")
    LOG_FILE = join(ROOT_DIR, "app.log")
    VOLMEMLYZER_FILE = join(LIBS_DIR, "VolMemLyzer-2.0.0", "VolMemLyzer-V2.py")
    VOLATILITY_FILE = join(LIBS_DIR, "volatility3-2.8.0", "vol.py")

    STATUS = {
        "CREATED": "Created",
        "PROCESSING": "Processing",
        "PROCESSED": "Processed",
        "ERROR": "Error",
    }

    TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

    UPDATED_VOL_MODULES = """
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
