#!/bin/bash

echo "╔═══════════════════════════════════════════════════════╗"
echo "║   NixOS Configuration Update for Kitchen iMac         ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo

# Create a backup of current configuration
echo "Creating backup of current configuration..."
sudo cp /etc/nixos/configuration.nix /etc/nixos/configuration.nix.backup.$(date +%Y%m%d_%H%M%S)

echo "Current audio configuration:"
grep -A5 "audio\|pulse\|pipewire" /etc/nixos/configuration.nix

echo
echo "Updating configuration.nix with fixes..."
echo

# Create the updated configuration snippet
cat << 'EOF' > /tmp/nixos-updates.nix

# === AUDIO CONFIGURATION FIX ===
# Disable old PulseAudio, use PipeWire with proper Intel PCH defaults
hardware.pulseaudio.enable = false;
services.pipewire = {
  enable = true;
  alsa.enable = true;
  alsa.support32Bit = true;
  pulse.enable = true;
  jack.enable = true;
  
  # Set Intel PCH as default audio device
  wireplumber.configPackages = [
    (pkgs.writeTextDir "share/wireplumber/wireplumber.conf.d/51-alsa-custom.conf" ''
      monitor.alsa.rules = [
        {
          matches = [
            { device.name = "~alsa_card.pci-0000_00_1f.3" }
          ]
          actions = {
            update-props = {
              device.description = "Mac Intel Audio"
              device.profile-set = "default.conf"
              api.alsa.use-acp = true
              priority.driver = 2000
              priority.session = 2000
            }
          }
        }
      ]
    '')
  ];
};

# === NETWORK WAKE-ON-LAN FIX ===
networking.interfaces.enp4s0f0 = {
  useDHCP = true;
  wakeOnLan = {
    enable = true;
    policy = ["magic" "unicast"];
  };
};

# Enable WoL service to persist across reboots
systemd.services.wake-on-lan = {
  description = "Enable Wake-on-LAN";
  after = [ "network.target" ];
  serviceConfig = {
    Type = "oneshot";
    ExecStart = "${pkgs.ethtool}/bin/ethtool -s enp4s0f0 wol g";
    RemainAfterExit = true;
  };
  wantedBy = [ "multi-user.target" ];
};

# === ADDITIONAL PACKAGES ===
# Add these to your existing environment.systemPackages
# ethtool - for network interface control
# wakeonlan - for sending WoL packets
# pavucontrol - GUI for audio control
# alsa-utils - ALSA utilities

EOF

echo "Configuration snippet created at /tmp/nixos-updates.nix"
echo
echo "IMPORTANT: You need to manually edit /etc/nixos/configuration.nix to:"
echo "1. Replace the audio configuration section"
echo "2. Add/update the network configuration"
echo "3. Add ethtool, wakeonlan, pavucontrol to systemPackages"
echo
echo "After editing, run: sudo nixos-rebuild switch"
echo

echo "╔═══════════════════════════════════════════════════════╗"
echo "║   Fusion Drive (1TB HDD) Status                       ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo

echo "Current partition table:"
sudo fdisk -l /dev/sda

echo
echo "The 1TB drive currently has:"
echo "- 200MB EFI partition (/dev/sda1)"
echo "- 931.3GB APFS partition (/dev/sda2)"
echo
echo "To prepare for macOS Catalina backup, you would need to:"
echo "1. Boot from a macOS installer USB"
echo "2. Use Disk Utility to format as APFS or Mac OS Extended (Journaled)"
echo "3. Install macOS Catalina as a backup system"
echo
echo "OR keep it as storage accessible from NixOS by mounting the APFS partition"
echo

echo "To check if APFS is readable from NixOS:"
which apfs-fuse >/dev/null 2>&1 && echo "apfs-fuse is installed" || echo "apfs-fuse not found - install with: nix-env -iA nixos.apfs-fuse"
