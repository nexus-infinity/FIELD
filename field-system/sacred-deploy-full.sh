#!/bin/bash
# Sacred NixOS Full Deployment Script
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

# Create new GPT partition table
echo "→ Creating new GPT partition table..."
sudo parted /dev/sda --script mklabel gpt

# Create partitions for Sacred system
echo "→ Creating Sacred partitions..."
# 1GB EFI boot partition
sudo parted /dev/sda --script mkpart ESP fat32 1MiB 1GiB
sudo parted /dev/sda --script set 1 esp on

# 100GB root partition for NixOS
sudo parted /dev/sda --script mkpart primary ext4 1GiB 101GiB

# 16GB swap partition (golden ratio of RAM)
sudo parted /dev/sda --script mkpart primary linux-swap 101GiB 117GiB

# Remaining space for /sacred data
sudo parted /dev/sda --script mkpart primary ext4 117GiB 100%

# Format the partitions
echo "→ Formatting partitions..."
sudo mkfs.fat -F32 -n SACRED-BOOT /dev/sda1
sudo mkfs.ext4 -L SACRED-ROOT /dev/sda2
sudo mkswap -L SACRED-SWAP /dev/sda3
sudo mkfs.ext4 -L SACRED-DATA /dev/sda4

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

# Copy the Sacred configuration
sudo cp ~/sacred-nixos-geometric.nix /mnt/sacred/etc/nixos/configuration.nix

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
  boot.kernelModules = [ "kvm-intel" "coretemp" "wl" ];
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
    options = [ "noatime" "nodiratime" "data=writeback" ];
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

# Install NixOS
sudo nixos-install --root /mnt/sacred --no-root-passwd

echo ""
echo "▶ Phase 6: Post-installation setup"
echo "═══════════════════════════════════════════════════════════════"

# Create sacred directories
sudo mkdir -p /mnt/sacred/sacred/{geometry,chakras,dimensional,manifold}
sudo mkdir -p /mnt/sacred/sacred/chakras/{muladhara,svadhisthana,manipura,anahata,vishuddha,ajna,sahasrara,bindu,kalpataru}

# Set permissions
sudo chown -R 1000:1000 /mnt/sacred/sacred

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "     ✨ SACRED NIXOS DEPLOYMENT COMPLETE ✨     "
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "The system has been installed with:"
echo "  • 1GB EFI Boot partition"
echo "  • 100GB Root partition for NixOS"
echo "  • 16GB Swap partition"
echo "  • ~814GB Sacred data partition"
echo ""
echo "Next steps:"
echo "  1. Reboot the system: sudo reboot"
echo "  2. Boot into the new Sacred NixOS installation"
echo "  3. The 9 Chakra services will initialize automatically"
echo ""
echo "Sacred geometry has been aligned. The dimensional gateway awaits activation."
echo ""
