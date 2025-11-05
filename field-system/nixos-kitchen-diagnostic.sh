#!/bin/bash

echo "╔═══════════════════════════════════════════════════════╗"
echo "║     NixOS Kitchen iMac Diagnostic Report              ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo

echo "=== SYSTEM INFORMATION ==="
echo "Hostname: $(hostname)"
echo "Kernel: $(uname -r)"
echo "NixOS Version: $(nixos-version 2>/dev/null || echo 'N/A')"
echo

echo "=== DISK CONFIGURATION ==="
echo "Block Devices:"
lsblk -f
echo
echo "Disk Usage:"
df -h
echo
echo "Fusion Drive Components (if present):"
diskutil list 2>/dev/null || echo "diskutil not available in NixOS"
echo

echo "=== SOUND CONFIGURATION ==="
echo "ALSA Devices:"
aplay -l 2>/dev/null || echo "aplay not found"
echo
echo "PulseAudio Status:"
pactl info 2>/dev/null || echo "PulseAudio not running/installed"
echo
echo "Sound Cards:"
cat /proc/asound/cards 2>/dev/null || echo "No /proc/asound/cards"
echo
echo "Audio Modules:"
lsmod | grep -E "snd|audio" || echo "No audio modules loaded"
echo

echo "=== NETWORK CONFIGURATION ==="
echo "Network Interfaces:"
ip addr show
echo
echo "Wake-on-LAN Status:"
for iface in $(ls /sys/class/net/ | grep -v lo); do
    echo "Interface: $iface"
    ethtool $iface 2>/dev/null | grep -E "Wake-on|Supports Wake" || echo "  ethtool not available or no WoL info"
done
echo
echo "Network Manager Status:"
systemctl status NetworkManager 2>/dev/null | head -10 || echo "NetworkManager not found"
echo

echo "=== NIXOS CONFIGURATION ==="
echo "Hardware Configuration:"
if [ -f /etc/nixos/hardware-configuration.nix ]; then
    echo "Found hardware-configuration.nix"
    grep -E "sound|audio|network|ethernet|wake" /etc/nixos/hardware-configuration.nix 2>/dev/null | head -20
else
    echo "hardware-configuration.nix not found"
fi
echo
echo "Main Configuration:"
if [ -f /etc/nixos/configuration.nix ]; then
    echo "Found configuration.nix"
    grep -E "sound|audio|pulse|alsa|network|wake|wol" /etc/nixos/configuration.nix 2>/dev/null | head -20
else
    echo "configuration.nix not found"
fi
echo

echo "=== SYSTEM SERVICES ==="
echo "Audio Services:"
systemctl list-units | grep -E "sound|audio|pulse|alsa" || echo "No audio services found"
echo
echo "Network Services:"
systemctl list-units | grep -E "network|wpa|dhcp" | head -10
echo

echo "=== HARDWARE DETECTION ==="
echo "PCI Audio Devices:"
lspci 2>/dev/null | grep -i audio || echo "lspci not available"
echo
echo "USB Devices:"
lsusb 2>/dev/null | head -10 || echo "lsusb not available"
echo

echo "=== DMESG AUDIO/NETWORK ERRORS ==="
dmesg | grep -E "audio|sound|snd|network|eth|wake" | tail -20 2>/dev/null || echo "Cannot read dmesg"
echo

echo "╔═══════════════════════════════════════════════════════╗"
echo "║     End of Diagnostic Report                          ║"
echo "╚═══════════════════════════════════════════════════════╝"
