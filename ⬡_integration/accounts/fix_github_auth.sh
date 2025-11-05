#!/bin/bash
# GitHub Authentication Fixer - nexus-infinity account
# Addresses the actual keyring token issue found in scan

echo "🔧 FIXING GITHUB AUTHENTICATION FOR nexus-infinity"
echo "=================================================="

# Check current status
echo "📊 Current GitHub auth status:"
gh auth status

echo -e "\n🗑️  Clearing invalid keyring token..."
gh auth logout -h github.com -u nexus-infinity 2>/dev/null || echo "No active session to logout"

echo -e "\n🔑 Re-authenticating with GitHub..."
echo "This will open your browser for authentication..."
sleep 2

# Re-authenticate
gh auth login -h github.com -p https -w

# Verify the fix
echo -e "\n✅ Verification - New auth status:"
gh auth status

# Test API access
echo -e "\n🧪 Testing GitHub API access..."
gh api user --jq '.login'

echo -e "\n📊 Authentication repair complete!"
echo "Your GitHub CLI should now work with the nexus-infinity account."
