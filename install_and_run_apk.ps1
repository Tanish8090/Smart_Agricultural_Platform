# Script to install and launch SAP on-device AI APK on connected Android device/emulator
$ErrorActionPreference = "Stop"

$adb = "$env:LOCALAPPDATA\Android\Sdk\platform-tools\adb.exe"
if (-not (Test-Path $adb)) {
    Write-Host "[!] ADB not found at $adb. Checking PATH..." -ForegroundColor Yellow
    $adb = "adb"
}

$apk = Join-Path $PSScriptRoot "android\app\build\outputs\apk\debug\app-debug.apk"
if (-not (Test-Path $apk)) {
    Write-Host "[!] APK not found at $apk. Please run assembleDebug first." -ForegroundColor Red
    exit 1
}

Write-Host "==========================================================" -ForegroundColor Green
Write-Host "  Smart Agriculture Platform (SAP) - On-Device AI Runner" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "Waiting for device/emulator..." -ForegroundColor Cyan

& $adb wait-for-device

$devices = & $adb devices
Write-Host "$devices" -ForegroundColor Gray

Write-Host "`n[*] Installing $apk..." -ForegroundColor Cyan
& $adb install -r -d $apk

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n[✓] APK Installed Successfully!" -ForegroundColor Green
    Write-Host "[*] Launching com.sap.agri/.MainActivity..." -ForegroundColor Cyan
    & $adb shell am start -n com.sap.agri/.MainActivity
    Write-Host "`n[✓] SAP Farmer App is now running on your device!" -ForegroundColor Green
} else {
    Write-Host "`n[!] Failed to install APK. Please check device connection and permissions." -ForegroundColor Red
}
