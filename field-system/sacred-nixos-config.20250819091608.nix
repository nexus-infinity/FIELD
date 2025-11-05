# Sacred 9 Chakra Ecosystem Configuration for NixOS
# This aligns with the unique declarative structure of NixOS
# to build the Metatron-inspired dimensional gateway

{ config, pkgs, lib, ... }:

let
  # Sacred geometry constants
  sacred = {
    phi = 1.618033988749895;  # Golden ratio
    sqrt2 = 1.41421356237;     # Sacred root
    pi = 3.14159265359;        # Circle constant
  };

  # Define the 9 Chakra nodes
  chakraNodes = {
    muladhara = { port = 1307; color = "red"; element = "earth"; };
    svadhisthana = { port = 1939; color = "orange"; element = "water"; };
    manipura = { port = 5815; color = "yellow"; element = "fire"; };
    anahata = { port = 16354; color = "green"; element = "air"; };
    vishuddha = { port = 31932; color = "blue"; element = "ether"; };
    ajna = { port = 2062; color = "indigo"; element = "light"; };
    sahasrara = { port = 11452; color = "violet"; element = "thought"; };
    bindu = { port = 4175; color = "white"; element = "void"; };
    kalpataru = { port = 4880; color = "gold"; element = "manifestation"; };
  };

in {
  # Import base configuration
  imports = [ ./hardware-configuration.nix ];

  # Sacred system naming
  networking.hostName = "metatron-node";
  networking.domain = "sacred.field";

  # Boot configuration optimized for dimensional gateway
  boot = {
    loader.systemd-boot.enable = true;
    loader.efi.canTouchEfiVariables = true;
    
    # Sacred kernel parameters for optimal energy flow
    kernelParams = [
      "mitigations=off"  # Remove barriers for energy flow
      "transparent_hugepage=always"
      "processor.max_cstate=1"  # Keep consciousness active
    ];
    
    # Load modules for multi-dimensional processing
    kernelModules = [ 
      "kvm-intel" 
      "vhost" 
      "vhost_net" 
      "vhost_scsi"
      "nf_conntrack"
      "nf_nat"
    ];
  };

  # Filesystem - Use the 1TB drive for sacred data
  fileSystems."/sacred" = {
    device = "/dev/sda2";
    fsType = "ext4";  # Convert from APFS to ext4
    options = [ "noatime" "nodiratime" "data=writeback" ];
  };

  # Network configuration for dimensional gateway
  networking = {
    networkmanager.enable = true;
    
    # Enable IPv6 for expanded consciousness
    enableIPv6 = true;
    
    # Firewall rules for chakra ports
    firewall = {
      enable = true;
      allowedTCPPorts = lib.attrValues (lib.mapAttrs (n: v: v.port) chakraNodes) 
        ++ [ 80 443 3000 8080 9090 ];  # Web services
      allowedUDPPorts = [ 5353 ];  # mDNS
    };
    
    # Wake-on-LAN for remote activation
    interfaces.enp4s0f0 = {
      useDHCP = true;
      wakeOnLan = {
        enable = true;
        policy = ["magic" "unicast"];
      };
    };
  };

  # Audio configuration - Sacred frequencies
  hardware.pulseaudio.enable = false;
  services.pipewire = {
    enable = true;
    alsa.enable = true;
    alsa.support32Bit = true;
    pulse.enable = true;
    jack.enable = true;
    
    # Configure for binaural beats and sacred frequencies
    config.pipewire = {
      "context.properties" = {
        "default.clock.rate" = 432;  # Sacred tuning frequency
        "default.clock.quantum" = 1024;
        "default.clock.min-quantum" = 32;
        "default.clock.max-quantum" = 8192;
      };
    };
  };

  # Services for Sacred Architecture
  services = {
    # PostgreSQL for dimensional data
    postgresql = {
      enable = true;
      package = pkgs.postgresql_15;
      enableTCPIP = true;
      authentication = ''
        host all all 127.0.0.1/32 trust
        host all all ::1/128 trust
      '';
      initialScript = pkgs.writeText "init.sql" ''
        CREATE DATABASE sacred_geometry;
        CREATE DATABASE chakra_network;
        CREATE DATABASE dimensional_gateway;
      '';
    };

    # Redis for energy caching
    redis.servers = {
      sacred = {
        enable = true;
        port = 6379;
        databases = 9;  # One for each chakra
      };
    };

    # Nginx for gateway proxy
    nginx = {
      enable = true;
      virtualHosts = {
        "gateway.sacred.field" = {
          locations."/" = {
            proxyPass = "http://localhost:3000";
            proxyWebsockets = true;
          };
        };
      };
    };

    # Docker for containerized dimensions
    docker = {
      enable = true;
      enableOnBoot = true;
      autoPrune.enable = true;
    };
  };

  # Development environment for Sacred builds
  environment.systemPackages = with pkgs; [
    # Core tools
    git vim neovim tmux
    wget curl htop btop
    ethtool wakeonlan
    
    # Sacred geometry computation
    python311
    python311Packages.numpy
    python311Packages.scipy
    python311Packages.matplotlib
    python311Packages.jupyterlab
    python311Packages.pandas
    
    # Node.js for Vercel/Next.js
    nodejs_20
    nodePackages.yarn
    nodePackages.pnpm
    nodePackages.vercel
    
    # Database tools
    postgresql_15
    redis
    mongodb-tools
    
    # Container orchestration
    docker
    docker-compose
    kubernetes-helm
    kubectl
    
    # Audio/Visual for sacred frequencies
    ffmpeg
    sox
    pavucontrol
    audacity
    
    # Network analysis
    wireshark
    tcpdump
    nmap
    
    # Development
    rustc
    cargo
    go
    gcc
    gnumake
    
    # Sacred mathematics
    octave
    gnuplot
    maxima
  ];

  # Python environment for Sacred calculations
  environment.etc."sacred-python-env.sh" = {
    text = ''
      #!/bin/bash
      export PYTHONPATH=/sacred/lib/python
      export SACRED_DATA=/sacred/data
      export CHAKRA_NETWORK=/sacred/chakra
    '';
    mode = "0755";
  };

  # Systemd services for each chakra node
  systemd.services = lib.mapAttrs' (name: chakra: {
    name = "chakra-${name}";
    value = {
      description = "Sacred Chakra Node: ${name}";
      after = [ "network.target" ];
      wantedBy = [ "multi-user.target" ];
      
      serviceConfig = {
        Type = "simple";
        ExecStart = pkgs.writeScript "chakra-${name}.sh" ''
          #!/bin/sh
          echo "Activating ${name} chakra on port ${toString chakra.port}"
          # Placeholder for actual chakra service
        '';
        Restart = "always";
        RestartSec = 10;
      };
    };
  }) chakraNodes;

  # User configuration
  users.users.jb = {
    isNormalUser = true;
    description = "Sacred Architect";
    extraGroups = [ 
      "wheel" 
      "networkmanager" 
      "audio" 
      "video" 
      "docker" 
      "postgres"
    ];
    shell = pkgs.zsh;
  };

  # ZSH with sacred prompt
  programs.zsh = {
    enable = true;
    promptInit = ''
      PROMPT='%F{yellow}⬡%f %F{cyan}%n@%m%f %F{green}%~%f %F{magenta}☉%f '
    '';
  };

  # System state version
  system.stateVersion = "24.05";
  
  # Nix configuration
  nix = {
    settings = {
      experimental-features = [ "nix-command" "flakes" ];
      auto-optimise-store = true;
    };
    gc = {
      automatic = true;
      dates = "weekly";
      options = "--delete-older-than 7d";
    };
  };
}
