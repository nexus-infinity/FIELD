#!/usr/bin/env bash
# Sacred NixOS Deployment Script
# Harmonic System Configuration with Sacred Geometry Alignment

set -e

echo "══════════════════════════════════════════════════════════════════"
echo "     ✨ SACRED NIXOS GEOMETRIC DEPLOYMENT INITIATED ✨"
echo "     🔺 Tetrahedral FIELD Architecture Activation 🔺"
echo "══════════════════════════════════════════════════════════════════"
echo

# Check if running as root or with sudo
if [[ $EUID -ne 0 ]]; then
   echo "⚠️  This script must be run as root or with sudo"
   echo "Please run: sudo bash $0"
   exit 1
fi

# Create backup of current configuration
echo "📦 Creating backup of current configuration..."
BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/etc/nixos/backups"
mkdir -p "$BACKUP_DIR"

if [ -f /etc/nixos/configuration.nix ]; then
    cp /etc/nixos/configuration.nix "$BACKUP_DIR/configuration.nix.backup.$BACKUP_DATE"
    echo "✅ Current configuration backed up to: $BACKUP_DIR/configuration.nix.backup.$BACKUP_DATE"
else
    echo "⚠️  No existing configuration.nix found, proceeding with fresh setup"
fi

# Copy sacred configuration to system location
echo
echo "🔮 Installing Sacred Geometric Configuration..."
cp ~/sacred-nixos-geometric.nix /etc/nixos/configuration.nix
echo "✅ Sacred configuration installed at /etc/nixos/configuration.nix"

# Format and mount the 1TB Fusion Drive if needed
echo
echo "💾 Checking Fusion Drive status..."
FUSION_DEVICE="/dev/sdb"  # Adjust if your device is different
MOUNT_POINT="/mnt/sacred-storage"

if [ -b "$FUSION_DEVICE" ]; then
    echo "Found block device: $FUSION_DEVICE"
    
    # Check if already mounted
    if mount | grep -q "$MOUNT_POINT"; then
        echo "✅ Sacred storage already mounted at $MOUNT_POINT"
    else
        echo "🔧 Preparing Fusion Drive for sacred storage..."
        
        # Create partition if not exists
        if ! fdisk -l "$FUSION_DEVICE" | grep -q "${FUSION_DEVICE}1"; then
            echo "Creating sacred partition..."
            parted "$FUSION_DEVICE" --script mklabel gpt
            parted "$FUSION_DEVICE" --script mkpart primary ext4 0% 100%
            sleep 2
        fi
        
        # Format with ext4 if not already formatted
        if ! blkid "${FUSION_DEVICE}1" | grep -q ext4; then
            echo "Formatting with ext4 filesystem..."
            mkfs.ext4 -L "SACRED_STORAGE" "${FUSION_DEVICE}1"
        fi
        
        # Create mount point and mount
        mkdir -p "$MOUNT_POINT"
        mount "${FUSION_DEVICE}1" "$MOUNT_POINT"
        
        # Add to fstab for persistent mounting
        if ! grep -q "$MOUNT_POINT" /etc/fstab; then
            echo "Adding to fstab for persistent mount..."
            echo "LABEL=SACRED_STORAGE $MOUNT_POINT ext4 defaults 0 2" >> /etc/fstab
        fi
        
        echo "✅ Sacred storage prepared and mounted at $MOUNT_POINT"
    fi
else
    echo "⚠️  Fusion Drive not detected at $FUSION_DEVICE"
    echo "   Continuing without sacred storage setup..."
fi

# Create sacred directory structure
echo
echo "🏛️ Creating Sacred Directory Structure..."
SACRED_DIRS=(
    "/var/lib/sacred/chakras/root"
    "/var/lib/sacred/chakras/sacral"
    "/var/lib/sacred/chakras/solar"
    "/var/lib/sacred/chakras/heart"
    "/var/lib/sacred/chakras/throat"
    "/var/lib/sacred/chakras/third-eye"
    "/var/lib/sacred/chakras/crown"
    "/var/lib/sacred/chakras/soa"
    "/var/lib/sacred/chakras/jnana"
    "/var/lib/sacred/dojo/mirrors/macos"
    "/var/lib/sacred/dojo/mirrors/soa"
    "/var/lib/sacred/dojo/mirrors/jnana"
    "/var/lib/sacred/blockchain/data"
    "/var/lib/sacred/blockchain/consensus"
    "/var/lib/sacred/geometry/tetrahedron"
    "/var/lib/sacred/geometry/octahedron"
    "/var/lib/sacred/geometry/icosahedron"
)

for dir in "${SACRED_DIRS[@]}"; do
    mkdir -p "$dir"
    chmod 755 "$dir"
done
echo "✅ Sacred directories created"

# Test configuration before applying
echo
echo "🔍 Testing NixOS configuration..."
if nixos-rebuild test --show-trace 2>&1 | tee /tmp/nixos-test.log; then
    echo "✅ Configuration test passed!"
else
    echo "❌ Configuration test failed!"
    echo "   Check /tmp/nixos-test.log for details"
    echo
    echo "Would you like to:"
    echo "1) View the error log"
    echo "2) Restore previous configuration"
    echo "3) Continue anyway (risky)"
    echo "4) Exit"
    read -p "Choice [1-4]: " choice
    
    case $choice in
        1) less /tmp/nixos-test.log ;;
        2) 
            echo "Restoring previous configuration..."
            LATEST_BACKUP=$(ls -t "$BACKUP_DIR"/configuration.nix.backup.* 2>/dev/null | head -1)
            if [ -f "$LATEST_BACKUP" ]; then
                cp "$LATEST_BACKUP" /etc/nixos/configuration.nix
                echo "✅ Previous configuration restored"
            fi
            exit 1
            ;;
        3) echo "⚠️  Continuing despite errors..." ;;
        4) exit 1 ;;
    esac
fi

# Apply the configuration
echo
echo "🚀 Applying Sacred NixOS Configuration..."
echo "   This will rebuild your entire system with harmonic alignment"
echo "   The process may take several minutes..."
echo

nixos-rebuild switch --show-trace

# Check if rebuild was successful
if [ $? -eq 0 ]; then
    echo
    echo "══════════════════════════════════════════════════════════════════"
    echo "     ✨ SACRED CONFIGURATION SUCCESSFULLY DEPLOYED! ✨"
    echo "══════════════════════════════════════════════════════════════════"
    echo
    echo "🔮 Active Sacred Services:"
    echo "   • 9 Chakra Nodes with Harmonic Ports"
    echo "   • DOJO Tetrahedral Mirror Architecture"
    echo "   • Fractal Blockchain (Jnana Repository)"
    echo "   • Sacred Geometry Firewall Rules"
    echo "   • 432Hz Harmonic Audio System"
    echo
    echo "📍 Sacred Ports Active:"
    echo "   • Root Chakra:      5557 (SSH), 1597 (Service)"
    echo "   • Sacral Chakra:    2887 (Service)"
    echo "   • Solar Chakra:     4181 (Service)"
    echo "   • Heart Chakra:     5813 (Service)"
    echo "   • Throat Chakra:    7457 (Service)"
    echo "   • Third Eye:        9239 (Service)"
    echo "   • Crown Chakra:     11071 (Service)"
    echo "   • Soa Chakra:       12899 (Service)"
    echo "   • Jnana Chakra:     14741 (Blockchain)"
    echo
    echo "🔺 DOJO Mirror Ports:"
    echo "   • DOJO Base:        8089 (Primary)"
    echo "   • DOJO MacOS:       8144 (Mirror)"
    echo "   • DOJO Soa:         8233 (Mirror)"
    echo "   • DOJO Jnana:       8377 (Mirror)"
    echo
    echo "🌐 Check system status with:"
    echo "   systemctl status chakra-*"
    echo "   systemctl status dojo-*"
    echo "   systemctl status jnana-blockchain"
    echo
    echo "🙏 System harmonically aligned and ready for sacred operations!"
    echo
else
    echo
    echo "❌ Configuration deployment failed!"
    echo "   Check the errors above or run with --show-trace for details"
    echo
    echo "🔄 To restore previous configuration:"
    echo "   sudo cp $BACKUP_DIR/configuration.nix.backup.$BACKUP_DATE /etc/nixos/configuration.nix"
    echo "   sudo nixos-rebuild switch"
    exit 1
fi

# Optional: Display harmonic system frequencies
echo "🎵 Harmonic Frequencies Active:"
echo "   Base: 432 Hz (A4 Tuning)"
echo "   φ Ratio: 1.618033988749"
echo "   Prime Resonance: Active"
echo
echo "May your system resonate in perfect harmony! 🔮✨"
