#!/bin/bash

echo "╔═══════════════════════════════════════════════════════╗"
echo "║     NixOS Kitchen iMac - Fixing Issues                ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo

echo "=== FIXING AUDIO CONFIGURATION ==="
echo "Current default sink: $(pactl get-default-sink)"
echo

echo "Available sinks:"
pactl list short sinks
echo

echo "Setting Intel PCH as default audio device..."
# Find the Intel PCH sink
PCH_SINK=$(pactl list short sinks | grep -i "pch\|analog" | awk '{print $2}' | head -1)
if [ -n "$PCH_SINK" ]; then
    echo "Found PCH sink: $PCH_SINK"
    pactl set-default-sink "$PCH_SINK"
    echo "Default sink set to: $(pactl get-default-sink)"
else
    echo "PCH sink not found in PulseAudio. Checking ALSA..."
    echo "ALSA cards:"
    cat /proc/asound/cards
    echo
    echo "Creating PulseAudio configuration for Intel PCH..."
    mkdir -p ~/.config/pulse
    cat > ~/.config/pulse/default.pa << 'EOF'
.include /etc/pulse/default.pa

# Set Intel PCH as default
set-default-sink alsa_output.pci-0000_00_1f.3.analog-stereo
set-default-source alsa_input.pci-0000_00_1f.3.analog-stereo

# Load Intel PCH module if not loaded
.ifexists module-alsa-card.so
load-module module-alsa-card device_id="0" name="pci-0000_00_1f.3" card_name="alsa_card.pci-0000_00_1f.3" namereg_fail=false tsched=yes fixed_latency_range=no ignore_dB=no deferred_volume=yes use_ucm=yes avoid_resampling=no
.endif
EOF
    echo "PulseAudio config created. Restarting PulseAudio..."
    systemctl --user restart pipewire pipewire-pulse 2>/dev/null || pulseaudio -k && pulseaudio --start
fi

echo
echo "Testing audio..."
# Generate a test tone
speaker-test -c 2 -l 1 -t sine 2>/dev/null &
TEST_PID=$!
sleep 2
kill $TEST_PID 2>/dev/null
echo "Audio test complete. Did you hear a test tone?"
echo

echo "=== CHECKING WAKE-ON-LAN ==="
echo "Installing ethtool if needed..."
which ethtool || echo "ethtool not found - add to configuration.nix"

echo
echo "Current network interfaces:"
ip link show | grep -E "^[0-9]"
echo

echo "=== SUGGESTED NIXOS CONFIGURATION CHANGES ==="
cat << 'EOF'

Add these to your /etc/nixos/configuration.nix:

1. For Audio (Intel PCH as default):
-----------------------------------
  # Audio configuration
  hardware.pulseaudio.enable = false;
  services.pipewire = {
    enable = true;
    alsa.enable = true;
    alsa.support32Bit = true;
    pulse.enable = true;
    jack.enable = true;
    
    # Set Intel PCH as default
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

2. For Wake-on-LAN:
-------------------
  # Network configuration
  networking.interfaces.enp4s0f0 = {
    useDHCP = true;
    wakeOnLan = {
      enable = true;
      policy = ["magic" "unicast"];
    };
  };
  
  # Install ethtool for WoL management
  environment.systemPackages = with pkgs; [
    ethtool
    wakeonlan
  ];
  
  # Enable WoL service
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

3. Add to systemPackages:
-------------------------
  environment.systemPackages = with pkgs; [
    pavucontrol     # GUI for PulseAudio control
    alsa-utils      # ALSA utilities
    ethtool         # Network interface control
    wakeonlan       # WoL packet sender
  ];

After editing, rebuild with:
sudo nixos-rebuild switch

EOF

echo
echo "╔═══════════════════════════════════════════════════════╗"
echo "║     Immediate Actions Completed                       ║"
echo "╚═══════════════════════════════════════════════════════╝"
