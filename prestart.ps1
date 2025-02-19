# MalMemSO_device prestarter script
# Version: 1.0
# Author: LARCES/UECE
# Date: 2025-02-18
# Description: This script ensures that all necessary conditions are met
# before the MalMemSO_device python script is executed.

# Checks if there are admin privileges
$admin = [Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()
if (-not $admin.IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "Error: The script must be run as an administrator." -ForegroundColor Red
    Start-Sleep -Seconds 5
    Exit 1
}

# Checks if Python 3 is installed
$program = Get-Command python3 -ErrorAction SilentlyContinue
if (-not $program) {
    Write-Host "Error: Python 3 is not installed." -ForegroundColor Red
    Start-Sleep -Seconds 5
    Exit 1
}

# Guarantees that the config.ini file exists
$configFile = Join-Path -Path $PSScriptRoot -ChildPath "config.ini"
$exampleConfigFile = Join-Path -Path $PSScriptRoot -ChildPath "config.example.ini"
if (-not (Test-Path $configFile)) {
    if (Test-Path $exampleConfigFile) {
        Copy-Item -Path $exampleConfigFile -Destination $configFile
        Write-Host "Info: config.ini not found. Copied from config.example.ini." -ForegroundColor Yellow
    } else {
        Write-Host "Error: Neither config.ini nor config.example.ini were found." -ForegroundColor Red
        Start-Sleep -Seconds 5
        Exit 1
    }
}

# Creates the necessary folders and files
$requiredFolders = @("logs", "outputs")
$outputsSubFolders = @("raw", "zip")
foreach ($folder in $requiredFolders) {
    $fullPath = Join-Path -Path $PSScriptRoot -ChildPath $folder
    if (-not (Test-Path $fullPath)) {
        New-Item -ItemType Directory -Path $fullPath | Out-Null
        Write-Host "Info: Created missing folder: $folder" -ForegroundColor Yellow
    }

    if ($folder -eq "outputs") {
        foreach ($subFolder in $outputsSubFolders) {
            $outputsSubFolderPath = Join-Path -Path $fullPath -ChildPath $subFolder
            if (-not (Test-Path $outputsSubFolderPath)) {
                New-Item -ItemType Directory -Path $outputsSubFolderPath | Out-Null
                Write-Host "Info: Created missing subfolder: outputs\$subFolder" -ForegroundColor Yellow
            }
        }
    }
}

$requiredFiles = @("device.log")
$targetFolder = Join-Path -Path $PSScriptRoot -ChildPath "logs"
foreach ($file in $requiredFiles) {
    $filePath = Join-Path -Path $targetFolder -ChildPath $file
    if (-not (Test-Path $filePath)) {
        New-Item -ItemType File -Path $filePath | Out-Null
        Write-Host "Info: Created missing file in logs/: $file" -ForegroundColor Yellow
    }
}

# Creates the arguments to be passed to the main program
$script_path = Join-Path -Path $PSScriptRoot -ChildPath "app.py"
$args = @($script_path)

# Determines the OS architecture
$arch = (Get-CimInstance Win32_OperatingSystem).OSArchitecture
if ($arch -match "32[\s-]?bits?") {
    $args += "-a 32bit"
}

# Executes the main program
Start-Process -FilePath "python3" -ArgumentList $args -NoNewWindow -Wait
