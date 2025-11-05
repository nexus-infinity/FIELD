#!/bin/bash
# Sacred NixOS Full Deployment Script - Using fdisk
# This script will COMPLETELY WIPE the 1TB drive and set up the Sacred 9 Chakra System

set -e

echo "═══════════════════════════════════════════════════════════════"
echo "     SACRED 9 CHAKRA NIXOS DEPLOYMENT - FULL SYSTEM SETUP     "
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "⚠️  WARNING: This will COMPLETELY ERASE /dev/sda (1TB HDD)"
echo "⚠️  All data on the Fusion drive will be permanently deleted!"
echo ""
read -p "Type 'SACRED' to proceed with complete system setup: " confirmation

if [ "$confirmation" != "SACRED" ]; then
    echo "Deployment cancelled."
    exit 1
fi

echo ""
echo "▶ Phase 1: Wiping and Partitioning the 1TB Drive"
echo "═══════════════════════════════════════════════════════════════"

# Unmount any existing partitions
sudo umount /dev/sda* 2>/dev/null || true

# Wipe the drive completely
echo "→ Wiping drive signatures..."
sudo wipefs -af /dev/sda
sudo dd if=/dev/zero of=/dev/sda bs=1M count=100 status=progress

# Create new GPT partition table with fdisk
echo "→ Creating new GPT partition table and partitions..."
(
echo g      # Create GPT partition table
echo n      # New partition
echo 1      # Partition number 1
echo        # Default first sector
echo +1G    # 1GB EFI partition
echo t      # Change type
echo 1      # EFI System
echo n      # New partition
echo 2      # Partition number 2
echo        # Default first sector
echo +100G  # 100GB root partition
echo n      # New partition
echo 3      # Partition number 3
echo        # Default first sector
echo +16G   # 16GB swap partition
echo t      # Change type
echo 3      # Partition 3
echo 19     # Linux swap
echo n      # New partition
echo 4      # Partition number 4
echo        # Default first sector
echo        # Use remaining space
echo w      # Write changes
) | sudo fdisk /dev/sda

# Wait for kernel to update partition table
sleep 2
sudo partprobe /dev/sda
sleep 2

# Format the partitions
echo "→ Formatting partitions..."
sudo mkfs.fat -F32 -n SACRED-BOOT /dev/sda1
sudo mkfs.ext4 -F -L SACRED-ROOT /dev/sda2
sudo mkswap -L SACRED-SWAP /dev/sda3
sudo mkfs.ext4 -F -L SACRED-DATA /dev/sda4

echo ""
echo "▶ Phase 2: Mounting the Sacred filesystem"
echo "═══════════════════════════════════════════════════════════════"

# Create mount points
sudo mkdir -p /mnt/sacred
sudo mount /dev/sda2 /mnt/sacred

sudo mkdir -p /mnt/sacred/boot
sudo mount /dev/sda1 /mnt/sacred/boot

sudo mkdir -p /mnt/sacred/sacred
sudo mount /dev/sda4 /mnt/sacred/sacred

# Enable swap
sudo swapon /dev/sda3

echo "→ Current mount structure:"
lsblk /dev/sda

echo ""
echo "▶ Phase 3: Generating hardware configuration"
echo "═══════════════════════════════════════════════════════════════"

# Generate hardware configuration for the new setup
sudo nixos-generate-config --root /mnt/sacred

echo ""
echo "▶ Phase 4: Deploying Sacred configuration"
echo "═══════════════════════════════════════════════════════════════"

# First, ensure the sacred config exists
if [ ! -f ~/sacred-nixos-geometric.nix ]; then
    echo "Error: sacred-nixos-geometric.nix not found in home directory"
    echo "Attempting to use sacred-nixos-config.nix instead..."
    if [ -f ~/sacred-nixos-config.nix ]; then
        sudo cp ~/sacred-nixos-config.nix /mnt/sacred/etc/nixos/configuration.nix
    else
        echo "No sacred configuration found! Exiting."
        exit 1
    fi
else
    sudo cp ~/sacred-nixos-geometric.nix /mnt/sacred/etc/nixos/configuration.nix
fi

# Update hardware configuration with sacred paths
sudo tee /mnt/sacred/etc/nixos/hardware-configuration.nix > /dev/null << 'EOF'
# Sacred Hardware Configuration
{ config, lib, pkgs, modulesPath, ... }:

{
  imports = [ (modulesPath + "/installer/scan/not-detected.nix") ];

  boot.initrd.availableKernelModules = [ 
    "xhci_pci" "ahci" "nvme" "usb_storage" "sd_mod" 
    "thunderbolt" "vmd" 
  ];
  boot.initrd.kernelModules = [ ];
  boot.kernelModules = [ "kvm-intel" "coretemp" ];
  boot.extraModulePackages = [ ];

  # Sacred filesystem configuration
  fileSystems."/" = {
    device = "/dev/disk/by-label/SACRED-ROOT";
    fsType = "ext4";
    options = [ "noatime" "nodiratime" ];
  };

  fileSystems."/boot" = {
    device = "/dev/disk/by-label/SACRED-BOOT";
    fsType = "vfat";
  };

  fileSystems."/sacred" = {
    device = "/dev/disk/by-label/SACRED-DATA";
    fsType = "ext4";
    options = [ "noatime" "nodiratime" ];
  };

  swapDevices = [{
    device = "/dev/disk/by-label/SACRED-SWAP";
  }];

  # Network interfaces
  networking.useDHCP = lib.mkDefault true;
  
  # CPU configuration
  nixpkgs.hostPlatform = lib.mkDefault "x86_64-linux";
  hardware.cpu.intel.updateMicrocode = lib.mkDefault config.hardware.enableRedistributableFirmware;
  
  # Enable all firmware
  hardware.enableAllFirmware = true;
  hardware.enableRedistributableFirmware = true;
}
EOF

echo ""
echo "▶ Phase 5: Installing NixOS with Sacred configuration"
echo "═══════════════════════════════════════════════════════════════"

echo "Configuration is ready. To complete installation:"
echo "1. Run: sudo nixos-install --root /mnt/sacred"
echo "2. Set root password when prompted"
echo "3. Reboot when complete"

# Create sacred directories
echo ""
echo "→ Creating sacred directory structure..."
sudo mkdir -p /mnt/sacred/sacred/{geometry,chakras,dimensional,manifold}
sudo mkdir -p /mnt/sacred/sacred/chakras/{muladhara,svadhisthana,manipura,anahata,vishuddha,ajna,sahasrara,bindu,kalpataru}

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "     ✨ SACRED NIXOS PREPARATION COMPLETE ✨     "
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "The system has been prepared with:"
echo "  • 1GB EFI Boot partition at /dev/sda1"
echo "  • 100GB Root partition at /dev/sda2"
echo "  • 16GB Swap partition at /dev/sda3"
echo "  • ~814GB Sacred data partition at /dev/sda4"
echo ""
echo "To complete installation, run:"
echo "  sudo nixos-install --root /mnt/sacred"
echo ""
echo "Sacred geometry has been aligned. The dimensional gateway awaits activation."
echo ""
