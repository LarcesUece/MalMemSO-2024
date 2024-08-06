# MalMemSO

## Setup Ubuntu 24.04 Server

### Update server
`apt update`

`apt upgrade`

### Install server packages
`apt install openssh-server`

`apt install git`

`apt install python3-virtualenv`

`apt install cifs-utils`


### Create directories

`mkdir /var/app`

`mkdir /var/app/dumps`

`mkdir /var/app/webapp`


### Move to work directory
`cd /var`

### Create virtual env
`virtualenv app`

`cd /var/app`

### Activate virtual env
`source bin/activate`

### Install dependencies
`pip3 install pefile`

`pip3 install yara-python`

`pip3 install capstone`

`pip3 install pycryptodome`

`#pip3 install pandas`

`pip3 install flask`

`pip3 install setuptools`

`pip3 install bigquery`

`pip3 install numpy==1.26.4`

`pip3 install pywinrm`

### Install Volatility3 and VolMemLyzer

`cd /var/app/`

`git clone https://github.com/volatilityfoundation/volatility3.git`

`git clone https://github.com/ahlashkari/VolMemLyzer`


### Configure VolMemLyzer

Update `/var/app/VolMemLyzer/VolMemLyzer-V2.py`, change this code:

```
VOL_MODULES = {
    'info': extract_winInfo_features,
    'pslist': extract_pslist_features,
    'dlllist': extract_dlllist_features,
    'handles': extract_handles_features,
    'ldrmodules': extract_ldrmodules_features,
    'malfind': extract_malfind_features,
    'modules': extract_modules_features,
    'callbacks': extract_callbacks_features,
    'cmdline': extract_cmdline_features,
    'devicetree': extract_devicetree_features,
    'driverirp': extract_driverirp_features,
    'drivermodule': extract_drivermodule_features,
    'driverscan': extract_driverscan_features,
    #####'dumpfiles': extract_dumpfiles_features,        # Creates Junk files in the Folder where VolMemLyzer is present [TRY NOT TO USE]
    'envars': extract_envars_features,
    'filescan': extract_filescan_features,
    'getsids': extract_getsids_features,
    'mbrscan': extract_mbrscan_features,
    #####'memmap': extract_memmap_features,             # Volatility Incompatibility [DO NOT USE]
    'mftscan': extract_mftscan_features,
    'modscan': extract_modscan_features,
    'mutantscan': extract_mutantscan_features,
    'netscan': extract_netscan_features,
    'netstat': extract_netstat_features,
    'poolscanner': extract_poolscanner_features,
    'privileges': extract_privileges_features,
    'pstree': extract_pstree_features,
    'registry.certificates': extract_registry_certificates_features,
    'registry.hivelist': extract_registry_hivelist_features,
    'registry.hivescan': extract_registry_hivescan_features,
    'registry.printkey': extract_registry_printkey_features,
    'registry.userassist': extract_registry_userassist_features,
    'sessions': extract_sessions_features,
    'skeleton_key': extract_skeleton_key_features,
    'ssdt': extract_ssdt_features,
    'statistics': extract_statistics_features,
    'svcscan': extract_svcscan_features,
    'symlinkscan': extract_symlinkscan_features,
    'vadinfo': extract_vadinfo_features,
    'vadwalk': extract_vadwalk_features,
    'verinfo': extract_verinfo_features,
    'virtmap': extract_virtmap_features

}

```

to this code:

```
VOL_MODULES = {
#   'info': extract_winInfo_features,
    'pslist': extract_pslist_features,
    'dlllist': extract_dlllist_features,
    'handles': extract_handles_features,
    'ldrmodules': extract_ldrmodules_features,
    'malfind': extract_malfind_features,
    'modules': extract_modules_features,
    'callbacks': extract_callbacks_features,
#    'cmdline': extract_cmdline_features,
#    'devicetree': extract_devicetree_features,
#    'driverirp': extract_driverirp_features,
#    'drivermodule': extract_drivermodule_features,
#    'driverscan': extract_driverscan_features,
    #####'dumpfiles': extract_dumpfiles_features,        # Creates Junk files in the Folder where VolMemLyzer is present [TRY NOT TO USE]
#    'envars': extract_envars_features,
#    'filescan': extract_filescan_features,
#    'getsids': extract_getsids_features,
#    'mbrscan': extract_mbrscan_features,
    #####'memmap': extract_memmap_features,             # Volatility Incompatibility [DO NOT USE]
#    'mftscan': extract_mftscan_features,
#    'modscan': extract_modscan_features,
#    'mutantscan': extract_mutantscan_features,
#    'netscan': extract_netscan_features,
#    'netstat': extract_netstat_features,
#    'poolscanner': extract_poolscanner_features,
#    'privileges': extract_privileges_features,
#    'pstree': extract_pstree_features,
#    'registry.certificates': extract_registry_certificates_features,
#    'registry.hivelist': extract_registry_hivelist_features,
#    'registry.hivescan': extract_registry_hivescan_features,
#    'registry.printkey': extract_registry_printkey_features,
#    'registry.userassist': extract_registry_userassist_features,
#    'sessions': extract_sessions_features,
#    'skeleton_key': extract_skeleton_key_features,
#    'ssdt': extract_ssdt_features,
#    'statistics': extract_statistics_features,
    'svcscan': extract_svcscan_features,
#    'symlinkscan': extract_symlinkscan_features,
#    'vadinfo': extract_vadinfo_features,
#    'vadwalk': extract_vadwalk_features,
#    'verinfo': extract_verinfo_features,
#    'virtmap': extract_virtmap_features

}
```

