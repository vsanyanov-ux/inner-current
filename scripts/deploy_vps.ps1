# VPS Deployment script for Standalone Golden Seven site (Inner Current)
# With Autonomous Telemetry & Download Tracker
param(
    [string]$SshUser = "root",
    [string]$SshHost = "156.67.63.13",
    [string]$DestDir = "/var/www/innercurrent"
)

$ErrorActionPreference = "Stop"

Write-Output "=== ⚡ Inner Current: Deploying Site, Telemetry & Admin to VPS ==="
Write-Output "Target: ${SshUser}@${SshHost}:${DestDir}"

$distDir = Join-Path $PSScriptRoot "..\dist_site"
if (-not (Test-Path $distDir)) {
    Write-Error "dist_site directory not found!"
    exit 1
}

$indexFile = Join-Path $distDir "index.html"
$indexContent = Get-Content -Path $indexFile -Raw -Encoding utf8
if ($indexContent -match "lamp-red-active" -or $indexContent -notmatch "scroll-smooth") {
    Write-Error "CRITICAL: dist_site/index.html is NOT the Golden Seven book library site! Refusing to deploy."
    exit 1
}

Write-Output "0. Injecting high-precision telemetry tracker into HTML pages..."
python (Join-Path $PSScriptRoot "inject_tracker.py")

Write-Output "0.1 Building static wiki data from Obsidian Vault and MOC..."
python (Join-Path $PSScriptRoot "build_wiki_static.py")

Write-Output "0.2 Copying stats engine files to dist_site..."
Copy-Item (Join-Path $PSScriptRoot "stats_server.js") (Join-Path $distDir "stats_server.js") -Force
Copy-Item (Join-Path $PSScriptRoot "stats_service.js") (Join-Path $distDir "stats_service.js") -Force
Copy-Item (Join-Path $PSScriptRoot "..\public\admin.html") (Join-Path $distDir "admin.html") -Force

$tarFile = Join-Path $PSScriptRoot "dist_site.tar.gz"
if (Test-Path $tarFile) { Remove-Item $tarFile -Force }

Write-Output "1. Packing dist_site into tar.gz..."
python -c "
import tarfile, os
with tarfile.open(r'$tarFile', 'w:gz') as tar:
    tar.add(r'$distDir', arcname='.')
"

Write-Output "2. Uploading archive, Nginx conf and Systemd service to VPS..."
scp -o StrictHostKeyChecking=no $tarFile "${SshUser}@${SshHost}:/tmp/dist_site.tar.gz"
scp -o StrictHostKeyChecking=no (Join-Path $PSScriptRoot "nginx_innercurrent.conf") "${SshUser}@${SshHost}:/tmp/nginx_innercurrent.conf"
scp -o StrictHostKeyChecking=no (Join-Path $PSScriptRoot "innercurrent-stats.service") "${SshUser}@${SshHost}:/tmp/innercurrent-stats.service"

Write-Output "3. Unpacking, configuring Systemd service and reloading Nginx on VPS..."
$remoteCmd = @"
mkdir -p $DestDir
mkdir -p $DestDir/data
tar -xzf /tmp/dist_site.tar.gz -C $DestDir
chown -R www-data:www-data $DestDir
chmod -R 755 $DestDir
chmod -R 775 $DestDir/data
rm -f /tmp/dist_site.tar.gz

# 1. Setup systemd service for stats engine
cp /tmp/innercurrent-stats.service /etc/systemd/system/innercurrent-stats.service
systemctl daemon-reload
systemctl enable innercurrent-stats.service
systemctl restart innercurrent-stats.service
rm -f /tmp/innercurrent-stats.service

# 2. Setup Nginx configuration
cp /tmp/nginx_innercurrent.conf /etc/nginx/sites-available/innercurrent
rm -f /tmp/nginx_innercurrent.conf
nginx -t && systemctl reload nginx

# 3. Status verification
systemctl is-active innercurrent-stats.service
"@

ssh -o StrictHostKeyChecking=no "${SshUser}@${SshHost}" $remoteCmd

if (Test-Path $tarFile) { Remove-Item $tarFile -Force }

Write-Output ""
Write-Output "=== 🚀 Deployment completed successfully! ==="
Write-Output "🌐 Public Site:      https://innercurrent.ru"
Write-Output "📊 Closed Admin:     https://innercurrent.ru/admin"
Write-Output "🔑 Master Password:  innercurrent2026"
Write-Output "Preview URL:         http://innercurrent.156-67-63-13.nip.io"
