.PHONY: help setup scan run-agent harmonic-ports test-harmonic clean

help:
	@echo "FIELD System Resource Walker & Optimizer"
	@echo ""
	@echo "Usage:"
	@echo "  make setup         # Set up development environment"
	@echo "  make scan         # Run initial system scan"
	@echo "  make run-agent    # Start FIELD agent"
	@echo "  make test         # Run all tests"
	@echo "  make clean        # Clean build artifacts"
	@echo ""
	@echo "Sacred Geometry:"
	@echo "  make harmonic-ports     # Generate & validate harmonic port assignments"
	@echo "  make test-harmonic      # Run harmonic port tests"

setup:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

scan:
	python3 walker/scan.py

run-agent:
	python3 agent/run.py

test:
	. .venv/bin/activate && python3 -m pytest tests/

clean:
	rm -rf .venv
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

# Sacred Geometry Targets

harmonic-ports:
	@echo "🔮 Generating harmonic port assignments..."
	@python3 policy/harmonic_ports.py --emit json nix env \
		--out-json ops/out/chakra_ports.json \
		--out-nix ops/out/chakra_ports.nix \
		--out-env ops/out/chakra_ports.env \
		--print
	@echo "\n✨ Running validation tests..."
	@python3 tests/test_harmonic_ports.py
	@echo "\n📝 To apply changes to NixOS config:"
	@echo "make harmonic-ports-apply"

harmonic-ports-apply:
	@echo "🔄 Applying harmonic port assignments to NixOS config..."
	@python3 policy/harmonic_ports.py --apply-nix sacred-nixos-config.nix
	@echo "\n🚀 Next steps:"
	@echo "1. Review changes in sacred-nixos-config.nix"
	@echo "2. Commit changes to version control"
	@echo "3. On NixOS node: sudo nixos-rebuild switch"

test-harmonic:
	@echo "🧪 Running harmonic port tests..."
	@python3 tests/test_harmonic_ports.py
