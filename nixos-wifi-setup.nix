# NixOS WiFi Configuration
# Add this to your /etc/nixos/configuration.nix once you have a WiFi adapter

{ config, pkgs, ... }:

{
  # Enable NetworkManager for easier WiFi management
  networking.networkmanager.enable = true;
  
  # Ensure WiFi drivers are included
  boot.kernelModules = [ "iwlwifi" "rt2800usb" "rtl8192cu" "ath9k_htc" ];
  
  # Include firmware for various WiFi chipsets
  hardware.enableRedistributableFirmware = true;
  hardware.firmware = with pkgs; [
    linux-firmware
    rtl8192su-firmware
    rtl8192cu-firmware
  ];
  
  # Packages for WiFi management
  environment.systemPackages = with pkgs; [
    networkmanager
    networkmanagerapplet
    wirelesstools
    iw
    wpa_supplicant
  ];

  # Enable wpa_supplicant
  networking.wireless.enable = false; # Disable if using NetworkManager
  
  # Your WiFi network (replace with your details)
  # networking.wireless.networks = {
  #   "YourWiFiName" = {
  #     psk = "YourWiFiPassword";
  #   };
  # };
}

# After adding this:
# 1. sudo nixos-rebuild switch
# 2. sudo nmcli device wifi list
# 3. sudo nmcli device wifi connect "YourWiFiName" password "YourPassword"
