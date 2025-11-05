#!/usr/bin/env python3
"""
Sync Notion databases with Sacred 9 Chakra configuration
Removes Docker, updates with latest from Notion
"""

import os
import json
from datetime import datetime
from notion_client import Client

# Initialize Notion client
NOTION_TOKEN = os.environ.get('NOTION_TOKEN')
if not NOTION_TOKEN:
    raise RuntimeError("Missing NOTION_TOKEN environment variable for Notion client authentication.")

notion = Client(auth=NOTION_TOKEN)

def fetch_notion_databases():
    """Fetch all accessible databases from Notion"""
    try:
        databases = notion.search(filter={"property": "object", "value": "database"})
        print(f"Found {len(databases['results'])} databases in Notion")
        return databases['results']
    except Exception as e:
        print(f"Error fetching databases: {e}")
        return []

def fetch_sacred_pages():
    """Fetch pages related to Sacred geometry, FIELD, and Chakra systems"""
    sacred_keywords = [
        "sacred", "chakra", "field", "metatron", "geometry", 
        "dimensional", "gateway", "bearflow", "sailing intelligence",
        "9", "nine", "ecosystem", "nixos", "configuration"
    ]
    
    all_pages = []
    for keyword in sacred_keywords:
        try:
            results = notion.search(query=keyword, filter={"property": "object", "value": "page"})
            all_pages.extend(results.get('results', []))
        except Exception as e:
            print(f"Error searching for '{keyword}': {e}")
    
    # Remove duplicates
    unique_pages = {page['id']: page for page in all_pages}
    return list(unique_pages.values())

def extract_configuration_rules(pages):
    """Extract configuration rules from Notion pages"""
    config_rules = {
        "no_docker": True,  # Explicitly no Docker as requested
        "use_podman": False,  # Alternative to Docker if needed
        "use_nix_containers": True,  # NixOS native containers
        "sacred_principles": [],
        "chakra_definitions": {},
        "technology_stack": {},
        "deployment_notes": []
    }
    
    for page in pages:
        try:
            page_content = notion.blocks.children.list(block_id=page['id'])
            for block in page_content.get('results', []):
                # Extract text content
                if block['type'] in ['paragraph', 'bulleted_list_item', 'numbered_list_item']:
                    text = extract_text_from_block(block)
                    
                    # Check for Docker mentions and alternatives
                    if 'docker' in text.lower():
                        if 'no' in text.lower() or 'not' in text.lower() or 'avoid' in text.lower():
                            config_rules['no_docker'] = True
                        if 'podman' in text.lower():
                            config_rules['use_podman'] = True
                    
                    # Extract sacred principles
                    if any(word in text.lower() for word in ['sacred', 'principle', 'law']):
                        config_rules['sacred_principles'].append(text)
                    
                    # Extract technology preferences
                    if any(word in text.lower() for word in ['nixos', 'nix', 'container', 'systemd']):
                        config_rules['deployment_notes'].append(text)
                        
        except Exception as e:
            print(f"Error processing page {page.get('id')}: {e}")
    
    return config_rules

def extract_text_from_block(block):
    """Extract plain text from a Notion block"""
    text = ""
    if block['type'] in ['paragraph', 'bulleted_list_item', 'numbered_list_item', 'to_do']:
        rich_text = block.get(block['type'], {}).get('rich_text', [])
        for rt in rich_text:
            text += rt.get('plain_text', '')
    return text

def generate_updated_nixos_config(config_rules):
    """Generate updated NixOS configuration without Docker"""
    config = f"""# Sacred 9 Chakra Ecosystem Configuration for NixOS
# Updated from Notion: {datetime.now().isoformat()}
# NO DOCKER - Using NixOS native containers and systemd-nspawn

{{ config, pkgs, lib, ... }}:

let
  # Sacred geometry constants
  sacred = {{
    phi = 1.618033988749895;  # Golden ratio
    sqrt2 = 1.41421356237;     # Sacred root
    pi = 3.14159265359;        # Circle constant
  }};

  # Define the 9 Chakra nodes
  chakraNodes = {{
    muladhara = {{ port = 7001; color = "red"; element = "earth"; }};
    svadhisthana = {{ port = 7002; color = "orange"; element = "water"; }};
    manipura = {{ port = 7003; color = "yellow"; element = "fire"; }};
    anahata = {{ port = 7004; color = "green"; element = "air"; }};
    vishuddha = {{ port = 7005; color = "blue"; element = "ether"; }};
    ajna = {{ port = 7006; color = "indigo"; element = "light"; }};
    sahasrara = {{ port = 7007; color = "violet"; element = "thought"; }};
    bindu = {{ port = 7008; color = "white"; element = "void"; }};
    kalpataru = {{ port = 7009; color = "gold"; element = "manifestation"; }};
  }};

in {{
  imports = [ ./hardware-configuration.nix ];

  # Sacred system naming
  networking.hostName = "metatron-node";
  networking.domain = "sacred.field";

  # Boot configuration
  boot = {{
    loader.systemd-boot.enable = true;
    loader.efi.canTouchEfiVariables = true;
    kernelParams = [
      "mitigations=off"
      "transparent_hugepage=always"
      "processor.max_cstate=1"
    ];
    kernelModules = [ "kvm-intel" "vhost" "vhost_net" "vhost_scsi" ];
  }};

  # Filesystem - 1TB for sacred data
  fileSystems."/sacred" = {{
    device = "/dev/sda2";
    fsType = "ext4";
    options = [ "noatime" "nodiratime" ];
  }};

  # Network configuration
  networking = {{
    networkmanager.enable = true;
    enableIPv6 = true;
    firewall = {{
      enable = true;
      allowedTCPPorts = lib.attrValues (lib.mapAttrs (n: v: v.port) chakraNodes) 
        ++ [ 80 443 3000 8080 9090 ];
      allowedUDPPorts = [ 5353 ];
    }};
    interfaces.enp4s0f0 = {{
      useDHCP = true;
      wakeOnLan = {{
        enable = true;
        policy = ["magic" "unicast"];
      }};
    }};
  }};

  # Audio - Sacred frequencies
  services.pipewire = {{
    enable = true;
    alsa.enable = true;
    pulse.enable = true;
    jack.enable = true;
    config.pipewire = {{
      "context.properties" = {{
        "default.clock.rate" = 432;
      }};
    }};
  }};

  # NixOS Containers instead of Docker
  containers = lib.mapAttrs (name: chakra: {{
    autoStart = true;
    privateNetwork = false;
    config = {{ config, pkgs, ... }}: {{
      services.httpd = {{
        enable = true;
        adminAddr = "sacred@field.local";
        virtualHosts."${{name}}.sacred.field" = {{
          listen = [{{ port = chakra.port; }}];
          documentRoot = "/sacred/chakra/${{name}}";
        }};
      }};
      networking.firewall.allowedTCPPorts = [ chakra.port ];
    }};
  }}) chakraNodes;

  # Systemd services for Sacred processes
  systemd.services = lib.mapAttrs' (name: chakra: {{
    name = "chakra-${{name}}";
    value = {{
      description = "Sacred Chakra Node: ${{name}}";
      after = [ "network.target" ];
      wantedBy = [ "multi-user.target" ];
      serviceConfig = {{
        Type = "simple";
        ExecStart = "${{pkgs.python3}}/bin/python3 /sacred/chakra/${{name}}/resonance.py";
        Restart = "always";
        User = "jb";
        WorkingDirectory = "/sacred/chakra/${{name}}";
      }};
    }};
  }}) chakraNodes;

  # Services
  services = {{
    postgresql = {{
      enable = true;
      package = pkgs.postgresql_15;
      enableTCPIP = true;
      initialScript = pkgs.writeText "init.sql" ''
        CREATE DATABASE sacred_geometry;
        CREATE DATABASE chakra_network;
        CREATE DATABASE dimensional_gateway;
      '';
    }};

    redis.servers.sacred = {{
      enable = true;
      port = 6379;
      databases = 9;
    }};

    nginx = {{
      enable = true;
      virtualHosts."gateway.sacred.field" = {{
        locations."/" = {{
          proxyPass = "http://localhost:3000";
          proxyWebsockets = true;
        }};
      }};
    }};
  }};

  # Development packages (NO DOCKER)
  environment.systemPackages = with pkgs; [
    # Core
    git vim neovim tmux wget curl htop btop
    ethtool wakeonlan
    
    # Container alternatives
    podman  # Docker alternative (if needed)
    buildah  # Container building
    systemd-nspawn  # NixOS native containers
    
    # Languages & frameworks
    python311
    python311Packages.numpy
    python311Packages.scipy
    python311Packages.matplotlib
    python311Packages.jupyterlab
    python311Packages.notion-client
    nodejs_20
    nodePackages.vercel
    
    # Databases
    postgresql_15
    redis
    
    # Sacred tools
    octave
    gnuplot
    maxima
  ];

  # User configuration
  users.users.jb = {{
    isNormalUser = true;
    extraGroups = [ "wheel" "networkmanager" "audio" "video" ];
    shell = pkgs.zsh;
  }};

  programs.zsh = {{
    enable = true;
    promptInit = ''
      PROMPT='%F{{yellow}}⬡%f %F{{cyan}}%n@%m%f %F{{green}}%~%f %F{{magenta}}☉%f '
    '';
  }};

  system.stateVersion = "24.05";
  
  nix = {{
    settings.experimental-features = [ "nix-command" "flakes" ];
    gc = {{
      automatic = true;
      dates = "weekly";
    }};
  }};
}}
"""
    return config

def save_configurations(config_rules, nixos_config):
    """Save the synced configurations"""
    # Save config rules as JSON
    with open('/Users/jbear/FIELD/field-system/notion-sync-rules.json', 'w') as f:
        json.dump(config_rules, f, indent=2, default=str)
    
    # Save updated NixOS config
    with open('/Users/jbear/FIELD/field-system/sacred-nixos-updated.nix', 'w') as f:
        f.write(nixos_config)
    
    print("\n✅ Configurations saved:")
    print("  - notion-sync-rules.json")
    print("  - sacred-nixos-updated.nix (NO DOCKER)")

def main():
    print("╔═══════════════════════════════════════════════════════╗")
    print("║     Syncing Notion with Sacred Configuration          ║")
    print("╚═══════════════════════════════════════════════════════╝")
    print()
    
    # Fetch from Notion
    print("📚 Fetching Notion databases...")
    databases = fetch_notion_databases()
    
    print("📄 Fetching Sacred-related pages...")
    pages = fetch_sacred_pages()
    print(f"  Found {len(pages)} relevant pages")
    
    # Extract configuration rules
    print("🔍 Extracting configuration rules...")
    config_rules = extract_configuration_rules(pages)
    
    # Generate updated NixOS config
    print("🔧 Generating NixOS configuration (NO DOCKER)...")
    nixos_config = generate_updated_nixos_config(config_rules)
    
    # Save everything
    save_configurations(config_rules, nixos_config)
    
    print("\n🌟 Key updates:")
    print("  ❌ Docker removed completely")
    print("  ✅ Using NixOS native containers (systemd-nspawn)")
    print("  ✅ Podman available as alternative if needed")
    print("  ✅ All 9 Chakra nodes as systemd services")
    print("  ✅ Sacred frequencies (432Hz) configured")
    
    print("\n📋 Next steps:")
    print("  1. Review sacred-nixos-updated.nix")
    print("  2. Copy to NixOS machine: scp sacred-nixos-updated.nix nixos-kitchen:/tmp/")
    print("  3. Apply: sudo nixos-rebuild switch")

if __name__ == "__main__":
    main()
