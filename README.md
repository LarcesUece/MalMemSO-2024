# MalMemSO / device

- Extraction of a memory dump file (.raw)
- Compression of the raw file (.zip)
- Sending the compressed file to the fog server
- To be implemented.

Operating systems supported: Windows 10.

## instructions

Edit the content of `config.example.ini` with the fog server settings and rename it to `config.ini`.

Run `python src/main.py -t <extraction_tool> -a <system_architecture>`.

- Extraction tool options: "winpmem" (default), "dumpit".
- System architecture options: "32bit", "64bit" (default).
- Run `python src/main.py -h` for help.

## modules (in order of execution)

### dump_extractor

Based on the specified extraction tool and system architecture (WinPmem and 64bit, by default, respectively), extracts a .raw memory dump file and save it on the outputs/raw/ directory.

### file_compressor

Compresses the .raw file to a .zip file and save it on the outputs/zip/ directory.

### file_sender

Connects with the fog server and sends the extracted dump .zip file to be analyzed.

### response_getter
### disable_network
### malware_remover
### network_enabler
### dump_cleaner
