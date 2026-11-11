# VPS Deployment script for Standalone Tsimla Tour Site
param(
    [string]$SshUser = "root",
    [string]$SshHost = "156.67.63.13",
    [string]$DestDir = "/var/www/tsimla"
)

$ErrorActionPreference = "Stop"

Write-Output "=== 🌊 Deploying Tsimla Tour Site to VPS ==="
Write-Output "Target: ${SshUser}@${SshHost}:${DestDir}"

$siteDir = $PSScriptRoot
$indexFile = Join-Path $siteDir "index.html"
$nginxConf = Join-Path $siteDir "nginx_tsimla.conf"

if (-not (Test-Path $indexFile)) {
    Write-Error "index.html not found in $siteDir!"
    exit 1
}

$tarFile = Join-Path $siteDir "tsimla_site.tar.gz"
if (Test-Path $tarFile) { Remove-Item $tarFile -Force }

Write-Output "1. Packing site into tar.gz..."
python -c "
import tarfile, os
with tarfile.open(r'$tarFile', 'w:gz') as tar:
    tar.add(r'$indexFile', arcname='index.html')
"

Write-Output "2. Uploading archive and Nginx conf to VPS..."
scp -o StrictHostKeyChecking=no $tarFile "${SshUser}@${SshHost}:/tmp/tsimla_site.tar.gz"
scp -o StrictHostKeyChecking=no $nginxConf "${SshUser}@${SshHost}:/tmp/nginx_tsimla.conf"

Write-Output "3. Unpacking and configuring Nginx on VPS..."
$remoteCmd = @"
mkdir -p $DestDir
tar -xzf /tmp/tsimla_site.tar.gz -C $DestDir
chown -R www-data:www-data $DestDir
chmod -R 755 $DestDir
rm -f /tmp/tsimla_site.tar.gz

# Setup Nginx configuration
cp /tmp/nginx_tsimla.conf /etc/nginx/sites-available/tsimla
ln -sf /etc/nginx/sites-available/tsimla /etc/nginx/sites-enabled/tsimla
rm -f /tmp/nginx_tsimla.conf
nginx -t && systemctl reload nginx
"@

ssh -o StrictHostKeyChecking=no "${SshUser}@${SshHost}" $remoteCmd

if (Test-Path $tarFile) { Remove-Item $tarFile -Force }

Write-Output ""
Write-Output "=== 🚀 Tour Site deployed successfully! ==="
Write-Output "🌐 URL (nip.io):     http://tsimla.156-67-63-13.nip.io"
Write-Output "🌐 Direct IP/Port:   http://156.67.63.13:8090"
Write-Output "🌐 Alt URL:          http://tour.156-67-63-13.nip.io"
