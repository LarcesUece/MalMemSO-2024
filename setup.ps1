# MalMemSO_device
# Author: LARCES/UECE
# Date: 2025-02-17
# Description: This script sets up an automated scheduled task to run 
# the "init.ps1" script every 30 minutes with administrator privileges. 
# It also copies all necessary program files to a protected directory 
# in "C:\Program Files\MalMemSO" to prevent accidental deletion. The 
# task is configured to run in the background without prompting the 
# user.

$admin = [Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()
if (-not $admin.IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "Error: The script must be run as an administrator." -ForegroundColor Red
    Exit 1
}

$taskName = "RunMalMemSO"
$programFolder = "C:\Program Files\MalMemSO"
$scriptPath = Join-Path -Path $PSScriptRoot -ChildPath "init.ps1"
$protectedScriptPath = Join-Path -Path $programFolder -ChildPath "init.ps1"

try {
    if (-not (Test-Path -Path $programFolder)) {
        New-Item -Path $programFolder -ItemType Directory -Force -ErrorAction Stop
    }
} catch {
    Write-Host "Error: Unable to create directory '$programFolder'. Check permissions." -ForegroundColor Red
    Exit 1
}

try {
    Get-ChildItem -Path $PSScriptRoot -File | Where-Object { $_.Name -ne "setup.ps1" } | ForEach-Object {
        Copy-Item -Path $_.FullName -Destination $programFolder -Force -ErrorAction Stop
    }
} catch {
    Write-Host "Error: Unable to copy files to '$programFolder'. Check permissions." -ForegroundColor Red
    Exit 1
}

$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -WindowStyle Hidden -File `"$protectedScriptPath`""

$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 30)

$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

try {
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -RunLevel Highest -Force -ErrorAction Stop *> $null
} catch {
    Write-Host "Error: Unable to register scheduled task. Check permissions." -ForegroundColor Red
    Exit 1
}

Write-Host "MalMemSO has been successfully set up."