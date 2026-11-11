#!/usr/bin/env bash
set -e

SSH_USER="${1:-root}"
SSH_HOST="${2:-156.67.63.13}"
DEST_DIR="${3:-/var/www/tsimla}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INDEX_FILE="${SCRIPT_DIR}/index.html"
NGINX_CONF="${SCRIPT_DIR}/nginx_tsimla.conf"
TAR_FILE="${SCRIPT_DIR}/tsimla_site.tar.gz"

echo "=== 🌊 Deploying Tsimla Tour Site to VPS ==="
echo "Target: ${SSH_USER}@${SSH_HOST}:${DEST_DIR}"

if [ ! -f "${INDEX_FILE}" ]; then
    echo "Error: index.html not found!" >&2
    exit 1
fi

rm -f "${TAR_FILE}"
echo "1. Packing site..."
tar -czf "${TAR_FILE}" -C "${SCRIPT_DIR}" index.html

echo "2. Uploading files to VPS..."
scp -o StrictHostKeyChecking=no "${TAR_FILE}" "${SSH_USER}@${SSH_HOST}:/tmp/tsimla_site.tar.gz"
scp -o StrictHostKeyChecking=no "${NGINX_CONF}" "${SSH_USER}@${SSH_HOST}:/tmp/nginx_tsimla.conf"

echo "3. Unpacking and reloading Nginx on VPS..."
ssh -o StrictHostKeyChecking=no "${SSH_USER}@${SSH_HOST}" "
mkdir -p ${DEST_DIR}
tar -xzf /tmp/tsimla_site.tar.gz -C ${DEST_DIR}
chown -R www-data:www-data ${DEST_DIR}
chmod -R 755 ${DEST_DIR}
rm -f /tmp/tsimla_site.tar.gz

cp /tmp/nginx_tsimla.conf /etc/nginx/sites-available/tsimla
ln -sf /etc/nginx/sites-available/tsimla /etc/nginx/sites-enabled/tsimla
rm -f /tmp/nginx_tsimla.conf
nginx -t && systemctl reload nginx
"

rm -f "${TAR_FILE}"

echo ""
echo "=== 🚀 Tour Site deployed successfully! ==="
echo "🌐 URL (nip.io):     http://tsimla.156-67-63-13.nip.io"
echo "🌐 Direct IP/Port:   http://156.67.63.13:8090"
echo "🌐 Alt URL:          http://tour.156-67-63-13.nip.io"
