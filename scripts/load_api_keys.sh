#!/bin/bash
# FIELD System API Key Loader
# This script safely loads API keys from a secure credentials vault
# Usage: source load_api_keys.sh

# Sacred Coordinates: -37.8136, 144.963 (Melbourne, Australia)
# Temporal Anchor: $(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "🔐 Loading FIELD System API Keys..."

# Define the secure credentials vault path
FIELD_ROOT="$(dirname "$(dirname "$(realpath "${BASH_SOURCE[0]}")")")"
CREDENTIALS_VAULT="$FIELD_ROOT/.credentials_vault"
FIELD_ENV_FILE="$CREDENTIALS_VAULT/field_api_keys.env"

# Ensure credentials vault exists
if [ ! -d "$CREDENTIALS_VAULT" ]; then
    echo "📁 Creating secure credentials vault at $CREDENTIALS_VAULT"
    mkdir -p "$CREDENTIALS_VAULT"
    chmod 700 "$CREDENTIALS_VAULT"
fi

# Create secure API keys file if it doesn't exist
if [ ! -f "$FIELD_ENV_FILE" ]; then
    echo "📄 Creating secure API keys template at $FIELD_ENV_FILE"
    cat > "$FIELD_ENV_FILE" << 'EOF'
# FIELD System API Keys - Secure Vault
# This file should contain your actual API keys
# NEVER commit this file to version control!

# AI Service API Keys
export OPENAI_API_KEY="your_openai_api_key_here"
export ANTHROPIC_API_KEY="your_anthropic_api_key_here"
export GEMINI_API_KEY="your_gemini_api_key_here"
export HUGGINGFACE_TOKEN="your_huggingface_token_here"

# Third-Party Service API Keys  
export NOTION_TOKEN="your_notion_integration_token_here"
export GITHUB_TOKEN="your_github_token_here"
export VERCEL_API_KEY="your_vercel_api_key_here"
export PINECONE_API_KEY="your_pinecone_api_key_here"
export CLOUDFLARE_API_TOKEN="your_cloudflare_api_token_here"
export KEYMATE_API_KEY="your_keymate_api_key_here"
export LANGCHAIN_API_KEY="your_langchain_api_key_here"

# JWT Configuration
export JWT_ISSUER="your_jwt_issuer_here"
export JWT_SECRET="your_jwt_secret_here"
EOF
    chmod 600 "$FIELD_ENV_FILE"
    echo "⚠️  Please edit $FIELD_ENV_FILE and add your actual API keys"
fi

# Source the API keys if the file exists and is readable
if [ -f "$FIELD_ENV_FILE" ] && [ -r "$FIELD_ENV_FILE" ]; then
    source "$FIELD_ENV_FILE"
    echo "✅ API keys loaded from secure vault"
    
    # Validate that required keys are set
    REQUIRED_KEYS=("OPENAI_API_KEY" "NOTION_TOKEN")
    MISSING_KEYS=()
    
    for key in "${REQUIRED_KEYS[@]}"; do
        if [ -z "${!key}" ] || [ "${!key}" = "your_${key,,}_here" ]; then
            MISSING_KEYS+=("$key")
        fi
    done
    
    if [ ${#MISSING_KEYS[@]} -gt 0 ]; then
        echo "⚠️  Missing or template values for: ${MISSING_KEYS[*]}"
        echo "   Please update $FIELD_ENV_FILE with your actual API keys"
    fi
else
    echo "❌ Cannot read API keys file: $FIELD_ENV_FILE"
    return 1
fi

# Export the Notion API key for consistency (some apps expect this variable name)
export NOTION_API_KEY="$NOTION_TOKEN"

echo "🌟 FIELD System credentials loaded successfully"
