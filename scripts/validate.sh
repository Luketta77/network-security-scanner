#!/usr/bin/env bash

set -e

cd "$(dirname "$0")/.."

if [ ! -f ".env" ]; then
    echo "[!] Arquivo .env não encontrado."
    echo "[!] Copie .env.example para .env."
    exit 1
fi

if [ -z "$1" ]; then
    read -r -p "Digite a rede autorizada [ex: 192.168.1.0/24]: " TARGET
else
    TARGET="$1"
fi

export TARGET_CIDR="$TARGET"

echo
echo "============================================"
echo "    CYBERSECURITY EXPOSURE PLATFORM"
echo "============================================"
echo

python3 src/main.py
