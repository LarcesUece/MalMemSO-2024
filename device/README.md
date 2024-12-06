# malware-detection / device

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
