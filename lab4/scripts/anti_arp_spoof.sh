#!/bin/bash
# Anti-ARP Spoofing Prevention Script

GATEWAY_IP="192.168.1.1"
GATEWAY_MAC="74:24:9f:67:c9:14"

echo "=========================================="
echo "Anti-ARP Spoofing Prevention Script"
echo "=========================================="

if [ "$EUID" -ne 0 ]; then 
    echo "[!] Please run as root (use sudo)"
    exit 1
fi

echo "[*] Gateway IP: $GATEWAY_IP"
echo "[*] Gateway MAC: $GATEWAY_MAC"
echo ""

# Show current ARP entry
echo "[*] Current ARP entry:"
arp -a | grep $GATEWAY_IP
echo ""

# Set static ARP entry
echo "[*] Setting static ARP entry..."
arp -s $GATEWAY_IP $GATEWAY_MAC

# Verify static entry
echo "[*] Verifying static ARP entry:"
arp -a | grep $GATEWAY_IP

echo ""
echo "[✓] Static ARP entry set. ARP spoofing prevented!"
