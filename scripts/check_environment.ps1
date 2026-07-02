Write-Host "=== Sistema operativo ==="
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsArchitecture

Write-Host ""
Write-Host "=== CPU ==="
Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors

Write-Host ""
Write-Host "=== RAM ==="
$os = Get-CimInstance Win32_OperatingSystem
[PSCustomObject]@{
    TotalGB = [math]::Round($os.TotalVisibleMemorySize / 1MB, 2)
    FreeGB = [math]::Round($os.FreePhysicalMemory / 1MB, 2)
}

Write-Host ""
Write-Host "=== GPU ==="
Get-CimInstance Win32_VideoController | Select-Object Name, AdapterRAM, DriverVersion

Write-Host ""
Write-Host "=== Ollama ==="
ollama --version
ollama list

