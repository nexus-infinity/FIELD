# Sacred 9 Chakra Ecosystem Configuration for NixOS
# Updated from Notion: 2025-08-19T05:55:38.900752
# NO DOCKER - Using NixOS native containers and systemd-nspawn

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
    muladhara = { port = 7001; color = "red"; element = "earth"; };
    svadhisthana = { port = 7002; color = "orange"; element = "water"; };
    manipura = { port = 7003; color = "yellow"; element = "fire"; };
    anahata = { port = 7004; color = "green"; element = "air"; };
    vishuddha = { port = 7005; color = "blue"; element = "ether"; };
    ajna = { port = 7006; color = "indigo"; element = "light"; };
    sahasrara = { port = 7007; color = "violet"; element = "thought"; };
    bindu = { port = 7008; color = "white"; element = "void"; };
    kalpataru = { port = 7009; color = "gold"; element = "manifestation"; };
  };

in {
  imports = [ ./hardware-configuration.nix ];

  # Sacred system naming
  networking.hostName = "metatron-node";
  networking.domain = "sacred.field";

  # Boot configuration
  boot = {
    loader.systemd-boot.enable = true;
    loader.efi.canTouchEfiVariables = true;
    kernelParams = [
      "mitigations=off"
      "transparent_hugepage=always"
      "processor.max_cstate=1"
    ];
    kernelModules = [ "kvm-intel" "vhost" "vhost_net" "vhost_scsi" ];
  };

  # Filesystem - 1TB for sacred data
  fileSystems."/sacred" = {
    device = "/dev/sda2";
    fsType = "ext4";
    options = [ "noatime" "nodiratime" ];
  };

  # Network configuration
  networking = {
    networkmanager.enable = true;
    enableIPv6 = true;
    firewall = {
      enable = true;
      allowedTCPPorts = lib.attrValues (lib.mapAttrs (n: v: v.port) chakraNodes) 
        ++ [ 80 443 3000 8080 9090 ];
      allowedUDPPorts = [ 5353 ];
    };
    interfaces.enp4s0f0 = {
      useDHCP = true;
      wakeOnLan = {
        enable = true;
        policy = ["magic" "unicast"];
      };
    };
  };

  # Audio - Sacred frequencies
  services.pipewire = {
    enable = true;
    alsa.enable = true;
    pulse.enable = true;
    jack.enable = true;
    config.pipewire = {
      "context.properties" = {
        "default.clock.rate" = 432;
      };
    };
  };

  # NixOS Containers instead of Docker
  containers = lib.mapAttrs (name: chakra: {
    autoStart = true;
    privateNetwork = false;
    config = { config, pkgs, ... }: {
      services.httpd = {
        enable = true;
        adminAddr = "sacred@field.local";
        virtualHosts."${name}.sacred.field" = {
          listen = [{ port = chakra.port; }];
          documentRoot = "/sacred/chakra/${name}";
        };
      };
      networking.firewall.allowedTCPPorts = [ chakra.port ];
    };
  }) chakraNodes;

  # Systemd services for Sacred processes
  systemd.services = lib.mapAttrs' (name: chakra: {
    name = "chakra-${name}";
    value = {
      description = "Sacred Chakra Node: ${name}";
      after = [ "network.target" ];
      wantedBy = [ "multi-user.target" ];
      serviceConfig = {
        Type = "simple";
        ExecStart = "${pkgs.python3}/bin/python3 /sacred/chakra/${name}/resonance.py";
        Restart = "always";
        User = "jb";
        WorkingDirectory = "/sacred/chakra/${name}";
      };
    };
  }) chakraNodes;

  # Services
  services = {
    postgresql = {
      enable = true;
      package = pkgs.postgresql_15;
      enableTCPIP = true;
      initialScript = pkgs.writeText "init.sql" ''
        CREATE DATABASE sacred_geometry;
        CREATE DATABASE chakra_network;
        CREATE DATABASE dimensional_gateway;
      '';
    };

    redis.servers.sacred = {
      enable = true;
      port = 6379;
      databases = 9;
    };

    nginx = {
      enable = true;
      virtualHosts."gateway.sacred.field" = {
        locations."/" = {
          proxyPass = "http://localhost:3000";
          proxyWebsockets = true;
        };
      };
    };
  };

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
  users.users.jb = {
    isNormalUser = true;
    extraGroups = [ "wheel" "networkmanager" "audio" "video" ];
    shell = pkgs.zsh;
  };

  programs.zsh = {
    enable = true;
    promptInit = ''
      PROMPT='%F{yellow}⬡%f %F{cyan}%n@%m%f %F{green}%~%f %F{magenta}☉%f '
    '';
  };

  system.stateVersion = "24.05";
  
  nix = {
    settings.experimental-features = [ "nix-command" "flakes" ];
    gc = {
      automatic = true;
      dates = "weekly";
    };
  };
}
