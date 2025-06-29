# Monitoring service installation script
$ErrorActionPreference = "Stop"

# Service configuration
$serviceName = "HospitalDeviceMonitor"
$serviceDisplayName = "Hospital Device Monitoring Service"
$serviceDescription = "Monitors medical devices and reports data to the IDS"
$installPath = "C:\Program Files\Hospital-IDS"
$monitoredDevices = $env:MONITORED_DEVICES -split ','

# Create installation directory
New-Item -ItemType Directory -Force -Path $installPath

# Create monitoring configuration
$config = @{
    "devices" = $monitoredDevices
    "ports" = @{
        "xray" = 11112
        "heart_monitor" = 2575
    }
    "log_path" = "C:\ProgramData\Hospital-IDS\logs"
}

# Save configuration
$config | ConvertTo-Json | Set-Content "$installPath\config.json"

# Create and start the service
New-Service -Name $serviceName `
    -DisplayName $serviceDisplayName `
    -Description $serviceDescription `
    -StartupType Automatic `
    -BinaryPathName "C:\Program Files\Hospital-IDS\monitor_service.exe"

Start-Service -Name $serviceName