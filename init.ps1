# MalMemSO_device
# Author: LARCES/UECE
# Date: 2025-02-17
# Description: This script ensures that the program is run with 
# administrator privileges, verifies if Python 3 is installed, 
# determines the OS architecture, and then executes the main program 
# named "app.py", located in the same directory.

$admin = [Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()
if (-not $admin.IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "Error: The script must be run as an administrator."
    Start-Sleep -Seconds 5
    Exit 1
}

$program = Get-Command python3 -ErrorAction SilentlyContinue
if (-not $program) {
    Write-Host "Error: Python 3 is not installed."
    Start-Sleep -Seconds 5
    Exit 1
}

$arch = (Get-CimInstance Win32_OperatingSystem).OSArchitecture
if (-not $arch) {
    Write-Host "Error: Unable to determine OS architecture."
    Start-Sleep -Seconds 5
    Exit 1
}

$script_path = Join-Path -Path $PSScriptRoot -ChildPath "app.py"

$args = @($script_path)
if ($arch -match "32 bits") {
    $args += "-a 32bit"
}

Start-Process -FilePath "python3" -ArgumentList $args -NoNewWindow -Wait
