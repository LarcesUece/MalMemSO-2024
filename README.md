# MalMemSO / device

## Overview

MalMemSO is a tool for extracting and processing memory dump files on Windows 10 devices. It automates the extraction, compression, and transmission of memory dumps for further analysis.

## Requirements

- **Operating System:** Windows 10
- **Dependencies:** [Python 3](https://www.python.org/downloads/windows/)

## Installation

### For Users

1. **Download** the repository and save it in your `Downloads` folder.
2. **Unzip** the downloaded folder.
3. **Open an elevated terminal:**
   - Right-click the Windows Start button.
   - Select **"Terminal (Admin)"** or **"Windows PowerShell (Admin)"**.
4. **Run the setup script:**

   ```powershell
   powershell -ExecutionPolicy Bypass -File ".\Downloads\MalMemSO_device\setup.ps1"
   ```

5. **To uninstall**, run:

   ```powershell
   Unregister-ScheduledTask -TaskName "RunMalMemSO" -Confirm:$false
   ```

### For Developers

1. **Configure the application:**
   - Edit `config.example.ini` with the fog server settings and rename it to `config.ini`.
2. **Run the program:**

   ```powershell
   python src/main.py -t <extraction_tool> -a <system_architecture>
   ```

   **Options:**
   - Extraction tools: `winpmem` (default), `dumpit`.
   - System architectures: `32bit`, `64bit` (default).
   - For help, run:

     ```powershell
     python src/main.py -h
     ```

## Modules (Execution Flow)

### 1. **dump_extractor**

- Extracts a `.raw` memory dump file based on the selected tool (`WinPmem` by default) and system architecture.
- Saves the file in `outputs/raw/`.

### 2. **file_compressor**

- Compresses the `.raw` file into a `.zip` archive.
- Saves the compressed file in `outputs/zip/`.

### 3. **file_sender**

- Connects to the fog server and uploads the compressed dump file for analysis.

### 4. **response_getter** *(To be implemented)*

- Retrieves analysis results from the fog server.

### 5. **disable_network** *(To be implemented)*

- Disables network connectivity for security reasons during analysis.

### 6. **malware_remover** *(To be implemented)*

- Identifies and removes detected malware threats.

### 7. **network_enabler** *(To be implemented)*

- Re-enables network connectivity after analysis.

### 8. **dump_cleaner** *(To be implemented)*

- Deletes temporary files and cleans up the system.

## License

This project is under development. Licensing details will be provided upon release.
