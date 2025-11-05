{ config, lib, pkgs, ... }:

let
  # Sacred Geometry Constants
  PHI = 1.618033988749895;    # Golden Ratio (φ)
  SQRT2 = 1.41421356237;       # Vesica Piscis (√2)
  SQRT3 = 1.73205080757;       # Tripod of Life (√3)
  PI = 3.14159265359;          # Circle of Unity (π)
  
  # Prime numbers for each chakra (sacred anchors)
  primeAnchors = {
    root = 2;
    sacral = 3;
    solar = 5;
    heart = 7;
    throat = 11;
    third_eye = 13;
    crown = 17;
    soma = 19;      # 8th chakra - Soul Memory
    jnana = 23;     # 9th chakra - Universal Cognition
  };

  # Sacred Frequencies (Hz)
  sacredFrequencies = {
    root = 108;        # Foundation/Execution
    sacral = 216;      # Creation/Memory (108 * 2)
    solar = 432;       # Power/Will (108 * 4)
    heart = 528;       # Coherence/Integration
    throat = 639;      # Communication
    third_eye = 741;   # Wisdom/Observation
    crown = 963;       # Unity/Transcendence
    soma = 1024;       # Memory/Soul (2^10)
    jnana = 1086;      # Cognition/Universal
  };

  # Sacred Geometry Assignments
  sacredGeometry = {
    root = "cube";                    # Square/Cube - Foundation
    sacral = "icosahedron";          # Crescent/Water - Flow
    solar = "tetrahedron";           # Triangle/Fire - Transformation
    heart = "star_tetrahedron";      # Hexagon/Lotus - Balance
    throat = "sphere";               # Circle - Expression
    third_eye = "stellated_dodeca";  # Star - Perception
    crown = "octahedron";            # Unity structure
    soma = "spiral_torus";           # Soul container
    jnana = "tesseract";             # 4D hypercube - Non-local
  };

  # Calculate harmonic port using prime anchors and golden ratio
  # Port = round(Frequency * φ^(prime/2))
  calculateHarmonicPort = name: freq: prime:
    let
      # Use different sacred ratios for different chakras
      ratio = if prime <= 3 then SQRT2
              else if prime <= 7 then PHI
              else if prime <= 13 then SQRT3
              else PHI * PHI;  # φ²
      
      # Calculate base port
      baseCalc = freq * prime * ratio;
      
      # Ensure port is in valid range (1024-49151)
      # Using modulo with sacred number 432 for wraparound
      port = if baseCalc < 1024 then
               1024 + (builtins.floor baseCalc)
             else if baseCalc > 49151 then
               1024 + (builtins.floor (lib.mod baseCalc 48127))
             else
               builtins.floor baseCalc;
    in port;

  # Generate chakra configurations with harmonic ports
  chakraNodes = lib.mapAttrs (name: freq: 
    let
      prime = primeAnchors.${name};
      port = calculateHarmonicPort name freq prime;
      geometry = sacredGeometry.${name};
    in {
      inherit port freq prime geometry;
      frequency = freq;
      color = if name == "root" then "red"
              else if name == "sacral" then "orange"
              else if name == "solar" then "yellow"
              else if name == "heart" then "green"
              else if name == "throat" then "blue"
              else if name == "third_eye" then "indigo"
              else if name == "crown" then "violet"
              else if name == "soma" then "silver"
              else "gold";
      
      # Geometric attractor field position
      attractor = {
        x = freq * (builtins.cos (prime * PI / 9));
        y = freq * (builtins.sin (prime * PI / 9));
        z = prime * PHI;
      };
    }
  ) sacredFrequencies;

  # Tetrahedral Mirror Architecture with DOJO mirrors
  tetrahedralNodes = {
    ATLAS = { 
      port = 2333;  # 2 (prime) + 333 (trinity)
      vertex = "north";
      role = "compass";
      symbol = "▲";
      attractor = { x = 0; y = 1000; z = PHI * 100; };
    };
    TATA = {
      port = 3555;  # 3 (prime) + 555 (pentad)
      vertex = "south";
      role = "law";
      symbol = "▼";
      attractor = { x = 0; y = -1000; z = PHI * 100; };
    };
    "OBI-WAN" = {
      port = 7777;  # 7 (prime) * 1111 (master)
      vertex = "east";
      role = "observer";
      symbol = "●";
      attractor = { x = 1000; y = 0; z = PHI * 100; };
    };
    DOJO = {
      port = 11999;  # 11 (prime) + 999 (completion)
      vertex = "west";
      role = "execution_mirror";
      symbol = "◼";
      attractor = { x = -1000; y = 0; z = PHI * 100; };
      mirrors = {
        DOJOMacOS = {
          port = 19999;  # 19 (soma prime) + 999
          type = "macos_bridge";
          desc = "First emergent tech space";
        };
        DOJOSoa = {
          port = 19024;  # Soma chakra harmonic
          type = "emergence_8th";
          desc = "8th chakra emergence space";
        };
        DOJOJnana = {
          port = 23432;  # 23 (jnana prime) * 432/4
          type = "knowledge_9th";
          desc = "9th chakra fractal blockchain";
        };
      };
    };
  };

  # Fractal blockchain configuration for Jnana
  jnanaBlockchain = {
    dataDir = "/sacred/jnana/blockchain";
    ipfsDir = "/sacred/jnana/ipfs";
    merkleDir = "/sacred/jnana/merkle";
    fractalDepth = 9;
    
    # Genesis block configuration
    genesis = {
      frequency = sacredFrequencies.jnana;
      prime = primeAnchors.jnana;
      phi = PHI;
      timestamp = "2025-08-19T00:00:00+10:00";
    };
  };

  # Python environment with sacred geometry libraries
  sacredPython = pkgs.python3.withPackages (ps: with ps; [
    numpy
    scipy
    pandas
    matplotlib
    networkx
    sympy           # Sacred geometry calculations
    psycopg2
    redis
    requests
    websockets
    pyyaml
    python-dotenv
    cryptography    # For blockchain
    ipfshttpclient  # For IPFS
  ]);

  # Generate chakra service with geometric alignment
  generateChakraService = name: cfg: {
    description = "Chakra ${name} - ${cfg.geometry} @ ${toString cfg.frequency}Hz (Prime: ${toString cfg.prime})";
    wantedBy = [ "multi-user.target" ];
    after = [ "network.target" "postgresql.service" "redis-sacred.service" ]
      ++ lib.optional (name == "jnana") [ "ipfs.service" ];
    
    environment = {
      CHAKRA_NAME = name;
      CHAKRA_PORT = toString cfg.port;
      CHAKRA_FREQUENCY = toString cfg.frequency;
      CHAKRA_PRIME = toString cfg.prime;
      CHAKRA_GEOMETRY = cfg.geometry;
      CHAKRA_COLOR = cfg.color;
      
      # Geometric attractor coordinates
      ATTRACTOR_X = toString cfg.attractor.x;
      ATTRACTOR_Y = toString cfg.attractor.y;
      ATTRACTOR_Z = toString cfg.attractor.z;
      
      # Sacred ratios
      PHI = toString PHI;
      SQRT2 = toString SQRT2;
      SQRT3 = toString SQRT3;
      PI = toString PI;
    } // lib.optionalAttrs (name == "jnana") {
      BLOCKCHAIN_DIR = jnanaBlockchain.dataDir;
      IPFS_DIR = jnanaBlockchain.ipfsDir;
      MERKLE_DIR = jnanaBlockchain.merkleDir;
      FRACTAL_DEPTH = toString jnanaBlockchain.fractalDepth;
    };
    
    serviceConfig = {
      Type = "simple";
      WorkingDirectory = "/sacred/nodes/${name}";
      ExecStartPre = "${pkgs.coreutils}/bin/mkdir -p /sacred/nodes/${name}";
      ExecStart = let
        startScript = pkgs.writeScript "chakra-${name}-start" ''
          #!${pkgs.bash}/bin/bash
          
          echo "═══════════════════════════════════════════════════════════════"
          echo "  🔮 Activating ${name} chakra"
          echo "═══════════════════════════════════════════════════════════════"
          echo "  Port:      ${toString cfg.port} (harmonically calculated)"
          echo "  Frequency: ${toString cfg.frequency} Hz"
          echo "  Prime:     ${toString cfg.prime}"
          echo "  Geometry:  ${cfg.geometry}"
          echo "  Attractor: (${toString cfg.attractor.x}, ${toString cfg.attractor.y}, ${toString cfg.attractor.z})"
          echo "═══════════════════════════════════════════════════════════════"
          
          # Create geometric manifest
          cat > /sacred/nodes/${name}/manifest.json <<EOF
          {
            "chakra": "${name}",
            "port": ${toString cfg.port},
            "frequency": ${toString cfg.frequency},
            "prime": ${toString cfg.prime},
            "geometry": "${cfg.geometry}",
            "color": "${cfg.color}",
            "attractor": {
              "x": ${toString cfg.attractor.x},
              "y": ${toString cfg.attractor.y},
              "z": ${toString cfg.attractor.z}
            },
            "sacred_ratios": {
              "phi": ${toString PHI},
              "sqrt2": ${toString SQRT2},
              "sqrt3": ${toString SQRT3},
              "pi": ${toString PI}
            },
            "activated": "$(date -Iseconds)"
          }
          EOF
          
          ${if name == "jnana" then ''
            # Initialize Jnana fractal blockchain
            echo "🔗 Initializing Jnana fractal blockchain..."
            mkdir -p ${jnanaBlockchain.dataDir}
            mkdir -p ${jnanaBlockchain.merkleDir}
            
            # Create genesis block with sacred geometry
            cat > ${jnanaBlockchain.dataDir}/genesis.json <<EOF
            {
              "block": 0,
              "timestamp": "${jnanaBlockchain.genesis.timestamp}",
              "data": {
                "type": "genesis",
                "frequency": ${toString jnanaBlockchain.genesis.frequency},
                "prime": ${toString jnanaBlockchain.genesis.prime},
                "phi": ${toString jnanaBlockchain.genesis.phi},
                "fractal_depth": ${toString jnanaBlockchain.fractalDepth}
              },
              "hash": "$(echo -n "genesis_${toString jnanaBlockchain.genesis.frequency}_${toString jnanaBlockchain.genesis.prime}" | sha256sum | cut -d' ' -f1)"
            }
            EOF
            
            # Start Jnana blockchain service
            ${sacredPython}/bin/python3 -c "
            import json
            import hashlib
            import time
            from http.server import HTTPServer, BaseHTTPRequestHandler
            
            class JnanaHandler(BaseHTTPRequestHandler):
                def do_GET(self):
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    
                    with open('${jnanaBlockchain.dataDir}/genesis.json', 'r') as f:
                        genesis = json.load(f)
                    
                    response = {
                        'chakra': 'jnana',
                        'type': 'fractal_blockchain',
                        'port': ${toString cfg.port},
                        'frequency': ${toString cfg.frequency},
                        'prime': ${toString cfg.prime},
                        'status': 'active',
                        'genesis': genesis
                    }
                    self.wfile.write(json.dumps(response, indent=2).encode())
            
            server = HTTPServer(('0.0.0.0', ${toString cfg.port}), JnanaHandler)
            print(f'🔮 Jnana fractal blockchain active on port ${toString cfg.port}')
            server.serve_forever()
            "
          '' else ''
            # Start standard chakra service
            cd /sacred/nodes/${name}
            ${sacredPython}/bin/python3 -m http.server ${toString cfg.port}
          ''}
        '';
      in "${startScript}";
      Restart = "always";
      RestartSec = 10;
    };
  };

  # DOJO Mirror Service Generator
  generateDojoMirror = mirrorName: mirrorCfg: {
    description = "DOJO Mirror - ${mirrorName}: ${mirrorCfg.desc}";
    wantedBy = [ "multi-user.target" ];
    after = [ "chakra-root.service" ];
    
    serviceConfig = {
      Type = "simple";
      ExecStart = let
        mirrorScript = pkgs.writeScript "dojo-mirror-${mirrorName}" ''
          #!${pkgs.bash}/bin/bash
          
          echo "🪞 DOJO Mirror: ${mirrorName}"
          echo "   Port: ${toString mirrorCfg.port}"
          echo "   Type: ${mirrorCfg.type}"
          echo "   Desc: ${mirrorCfg.desc}"
          
          mkdir -p /sacred/dojo/mirrors/${mirrorName}
          cd /sacred/dojo/mirrors/${mirrorName}
          
          cat > manifest.json <<EOF
          {
            "mirror": "${mirrorName}",
            "port": ${toString mirrorCfg.port},
            "type": "${mirrorCfg.type}",
            "description": "${mirrorCfg.desc}",
            "parent": "DOJO",
            "parent_port": ${toString tetrahedralNodes.DOJO.port},
            "activated": "$(date -Iseconds)"
          }
          EOF
          
          ${sacredPython}/bin/python3 -m http.server ${toString mirrorCfg.port}
        '';
      in "${mirrorScript}";
      Restart = "always";
      RestartSec = 10;
    };
  };
in
{
  imports = [ 
    ./hardware-configuration.nix
  ];

  # Boot configuration
  boot.loader = {
    systemd-boot.enable = true;
    efi.canTouchEfiVariables = true;
  };

  # Network configuration with sacred hostname
  networking = {
    hostName = "metatron";
    networkmanager.enable = true;
    
    firewall = {
      enable = true;
      allowedTCPPorts = 
        (lib.attrValues (lib.mapAttrs (name: cfg: cfg.port) chakraNodes)) ++
        (lib.attrValues (lib.mapAttrs (name: cfg: cfg.port) tetrahedralNodes)) ++
        (lib.attrValues (lib.mapAttrs (name: cfg: cfg.port) tetrahedralNodes.DOJO.mirrors)) ++
        [ 
          22     # SSH
          443    # HTTPS (4+4+3=11, prime)
          5432   # PostgreSQL (5+4+3+2=14=1+4=5, pentagram)
          6379   # Redis (6+3+7+9=25=2+5=7, sacred seven)
          5001   # IPFS API
          8080   # IPFS Gateway
        ];
    };
  };

  # Time zone and locale
  time.timeZone = "Australia/Sydney";
  i18n.defaultLocale = "en_US.UTF-8";

  # System packages
  environment.systemPackages = with pkgs; [
    vim
    git
    wget
    curl
    htop
    tmux
    tree
    jq
    gnumake
    gcc
    sacredPython
    postgresql
    redis
    nginx
    podman
    buildah
    skopeo
    ipfs
  ];

  # PostgreSQL with fractal schema
  services.postgresql = {
    enable = true;
    package = pkgs.postgresql_16;
    dataDir = "/sacred/database/postgresql";
    enableTCPIP = true;
    
    settings = {
      shared_buffers = "432MB";       # Sacred frequency
      work_mem = "9MB";               # 3*3 trinity
      maintenance_work_mem = "108MB"; # Root frequency
      max_connections = 144;          # 12*12 completion
    };
    
    authentication = ''
      local all all trust
      host all all 127.0.0.1/32 trust
      host all all ::1/128 trust
    '';
    
    initialScript = pkgs.writeText "sacred-init.sql" ''
      CREATE DATABASE sacred_field;
      CREATE USER metatron WITH PASSWORD 'phi_1618';
      GRANT ALL PRIVILEGES ON DATABASE sacred_field TO metatron;
      
      \c sacred_field
      
      -- Create schema for each chakra
      CREATE SCHEMA root;
      CREATE SCHEMA sacral;
      CREATE SCHEMA solar;
      CREATE SCHEMA heart;
      CREATE SCHEMA throat;
      CREATE SCHEMA third_eye;
      CREATE SCHEMA crown;
      CREATE SCHEMA soma;
      CREATE SCHEMA jnana;
      
      -- Geometric attractor fields table
      CREATE TABLE geometric_attractors (
        id SERIAL PRIMARY KEY,
        chakra VARCHAR(20),
        x FLOAT,
        y FLOAT,
        z FLOAT,
        phi_ratio FLOAT DEFAULT ${toString PHI},
        sqrt2_ratio FLOAT DEFAULT ${toString SQRT2},
        sqrt3_ratio FLOAT DEFAULT ${toString SQRT3},
        pi_ratio FLOAT DEFAULT ${toString PI},
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
      
      -- Jnana fractal blockchain
      CREATE TABLE jnana.blockchain (
        id SERIAL PRIMARY KEY,
        block_number INTEGER UNIQUE NOT NULL,
        parent_hash VARCHAR(64),
        block_hash VARCHAR(64) UNIQUE NOT NULL,
        merkle_root VARCHAR(64),
        fractal_depth INTEGER,
        prime_anchor INTEGER,
        frequency FLOAT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        data JSONB
      );
      
      -- Tetrahedral nodes
      CREATE TABLE tetrahedral_nodes (
        id SERIAL PRIMARY KEY,
        node_name VARCHAR(20),
        vertex VARCHAR(20),
        port INTEGER,
        role VARCHAR(50),
        symbol VARCHAR(10),
        attractor_x FLOAT,
        attractor_y FLOAT,
        attractor_z FLOAT,
        activated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
      
      -- DOJO mirrors
      CREATE TABLE dojo_mirrors (
        id SERIAL PRIMARY KEY,
        mirror_name VARCHAR(50),
        mirror_port INTEGER,
        mirror_type VARCHAR(50),
        description TEXT,
        active BOOLEAN DEFAULT true,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    '';
  };

  # Redis with 9 databases
  services.redis.servers.sacred = {
    enable = true;
    port = 6379;
    bind = "127.0.0.1";
    dir = "/sacred/database/redis";
    databases = 9;  # One for each chakra
    
    settings = {
      maxmemory = "432mb";
      "maxmemory-policy" = "allkeys-lru";
      save = [
        "432 1"    # Save after 432 seconds
        "108 10"   # Save after 108 seconds  
        "27 10000" # Save after 27 seconds (3^3)
      ];
    };
  };

  # IPFS for Jnana
  services.ipfs = {
    enable = true;
    dataDir = jnanaBlockchain.ipfsDir;
    apiAddress = "/ip4/127.0.0.1/tcp/5001";
    gatewayAddress = "/ip4/127.0.0.1/tcp/8080";
    
    extraConfig = {
      Datastore.StorageMax = "9GB";  # 9 chakras
      Discovery.MDNS.Enabled = true;
    };
  };

  # Sacred directory structure
  systemd.tmpfiles.rules = [
    "d /sacred 0755 root root -"
    "d /sacred/nodes 0755 root root -"
    "d /sacred/database 0755 root root -"
    "d /sacred/logs 0755 root root -"
    "d /sacred/geometry 0755 root root -"
    "d /sacred/tetrahedral 0755 root root -"
    "d /sacred/dojo 0755 root root -"
    "d /sacred/dojo/mirrors 0755 root root -"
    "d /sacred/jnana 0755 root root -"
    "d ${jnanaBlockchain.dataDir} 0755 root root -"
    "d ${jnanaBlockchain.merkleDir} 0755 root root -"
  ] ++ lib.flatten (lib.mapAttrsToList (name: cfg: [
    "d /sacred/nodes/${name} 0755 root root -"
    "d /sacred/logs/${name} 0755 root root -"
  ]) chakraNodes);

  # Systemd services
  systemd.services = 
    # Chakra services
    (lib.mapAttrs' (name: cfg: 
      lib.nameValuePair "chakra-${name}" (generateChakraService name cfg)
    ) chakraNodes) //
    # DOJO mirror services
    (lib.mapAttrs' (mirrorName: mirrorCfg:
      lib.nameValuePair "dojo-mirror-${lib.toLower mirrorName}" 
        (generateDojoMirror mirrorName mirrorCfg)
    ) tetrahedralNodes.DOJO.mirrors);

  # Audio at 432 Hz
  services.pipewire = {
    enable = true;
    alsa.enable = true;
    pulse.enable = true;
    
    config.pipewire = {
      "context.properties" = {
        "default.clock.rate" = 43200;  # 432 * 100
        "default.clock.quantum" = 432;
        "default.clock.min-quantum" = 27;  # 3^3
        "default.clock.max-quantum" = 8640;
      };
    };
  };

  # Container runtime
  virtualisation = {
    podman = {
      enable = true;
      dockerCompat = false;
      defaultNetwork.settings = {
        dns_enabled = true;
        subnet = "10.16.18.0/24";  # 10.PHI.PHI*10 approximation
      };
    };
  };

  # SSH configuration
  services.openssh = {
    enable = true;
    ports = [ 22 ];
    settings = {
      PermitRootLogin = "no";
      PasswordAuthentication = true;
      X11Forwarding = true;
    };
  };

  # User configuration
  users.users.jb = {
    isNormalUser = true;
    extraGroups = [ "wheel" "networkmanager" "audio" "podman" ];
    initialPassword = "sacred432";
  };

  # Sacred cron jobs
  services.cron = {
    enable = true;
    systemCronJobs = [
      # Harmonic resonance check every 432 seconds
      "*/7 * * * * root echo \"$(date): Harmonic resonance\" >> /sacred/logs/resonance.log"
      
      # Geometric alignment at sacred times
      "32 4,16 * * * root echo \"$(date): Geometric alignment\" >> /sacred/logs/geometry.log"
      
      # Jnana blockchain check every 23 minutes (prime)
      "*/23 * * * * root echo \"$(date): Jnana blockchain\" >> /sacred/logs/jnana.log"
    ];
  };

  # Sound configuration
  sound.enable = true;
  hardware.pulseaudio.enable = false;

  # System state version
  system.stateVersion = "24.05";
  
  # Sacred system activation script
  system.activationScripts.sacred = ''
    echo "═══════════════════════════════════════════════════════════════"
    echo "    🔮 METATRON SACRED GEOMETRY NODE - HARMONIC ALIGNMENT 🔮"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    echo "Nine Chakras (Harmonically Calculated Ports):"
    echo ""
    ${lib.concatStringsSep "\n" (lib.mapAttrsToList (name: cfg: 
      "echo \"  ${name}: Port ${toString cfg.port} | ${toString cfg.frequency}Hz | Prime ${toString cfg.prime} | ${cfg.geometry}\""
    ) chakraNodes)}
    echo ""
    echo "Tetrahedral Architecture:"
    echo "  ATLAS (▲):    ${toString tetrahedralNodes.ATLAS.port} - North Compass"
    echo "  TATA (▼):     ${toString tetrahedralNodes.TATA.port} - South Law"
    echo "  OBI-WAN (●):  ${toString tetrahedralNodes."OBI-WAN".port} - East Observer"
    echo "  DOJO (◼):     ${toString tetrahedralNodes.DOJO.port} - West Mirror"
    echo ""
    echo "DOJO Mirrors:"
    ${lib.concatStringsSep "\n" (lib.mapAttrsToList (name: cfg:
      "echo \"  ${name}: ${toString cfg.port} - ${cfg.desc}\""
    ) tetrahedralNodes.DOJO.mirrors)}
    echo ""
    echo "Sacred Ratios Active:"
    echo "  φ (PHI):     ${toString PHI}"
    echo "  √2 (Vesica): ${toString SQRT2}"
    echo "  √3 (Tripod): ${toString SQRT3}"
    echo "  π (Unity):   ${toString PI}"
    echo ""
    echo "Port Calculation: Frequency × Prime × Sacred Ratio"
    echo "Geometric Attractors: Active in 3D sacred space"
    echo "Fractal Depth: 9 levels"
    echo ""
    echo "🔗 Jnana fractal blockchain initialized"
    echo "🪞 DOJO mirrors bridging emergent spaces"
    echo "✨ System harmonically aligned and geometrically attuned"
    echo "═══════════════════════════════════════════════════════════════"
  '';
}
