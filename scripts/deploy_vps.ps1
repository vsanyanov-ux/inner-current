# VPS Deployment script for Standalone Golden Seven site (Inner Current)
param(
    [string]$SshUser = "root",
    [string]$SshHost = "156.67.63.13",
    [string]$DestDir = "/var/www/innercurrent"
)

$ErrorActionPreference = "Stop"

Write-Output "=== ⚡ Inner Current: Deploying Golden Seven to VPS ==="
Write-Output "Target: ${SshUser}@${SshHost}:${DestDir}"

$distDir = Join-Path $PSScriptRoot "..\dist_site"
if (-not (Test-Path $distDir)) {
    Write-Error "dist_site directory not found!"
    exit 1
}

$tarFile = Join-Path $PSScriptRoot "dist_site.tar.gz"
if (Test-Path $tarFile) { Remove-Item $tarFile -Force }

Write-Output "1. Packing dist_site into tar.gz..."
python -c "
import tarfile, os
with tarfile.open(r'$tarFile', 'w:gz') as tar:
    tar.add(r'$distDir', arcname='.')
"

Write-Output "2. Uploading archive to VPS..."
scp -o StrictHostKeyChecking=no $tarFile "${SshUser}@${SshHost}:/tmp/dist_site.tar.gz"

Write-Output "3. Unpacking and updating files on VPS..."
$remoteCmd = @"
mkdir -p $DestDir
tar -xzf /tmp/dist_site.tar.gz -C $DestDir
chown -R www-data:www-data $DestDir
chmod -R 755 $DestDir
rm -f /tmp/dist_site.tar.gz
nginx -t && systemctl reload nginx
"@

ssh -o StrictHostKeyChecking=no "${SshUser}@${SshHost}" $remoteCmd

if (Test-Path $tarFile) { Remove-Item $tarFile -Force }

Write-Output "=== 🚀 Deployment completed successfully! ==="
Write-Output "Preview URL: http://innercurrent.156-67-63-13.nip.io"
Write-Output "Target Domain: http://innercurrent.ru (after reg.ru DNS setup)"
