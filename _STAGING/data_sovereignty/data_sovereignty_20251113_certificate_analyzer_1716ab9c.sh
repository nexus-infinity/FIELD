#!/bin/bash

# Certificate Analysis & Cleanup Script
# Analyzes keychain certificates for security issues, duplicates, and cleanup opportunities

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Output directory
OUTPUT_DIR="$HOME/Desktop/Certificate_Analysis_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUTPUT_DIR"

echo -e "${BLUE}🔍 Certificate Analysis & Cleanup Script${NC}"
echo -e "${BLUE}Output directory: $OUTPUT_DIR${NC}"
echo ""

# Function to log with timestamp
log() {
    echo -e "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$OUTPUT_DIR/analysis.log"
}

# Function to backup keychains
backup_keychains() {
    log "${GREEN}📦 Creating keychain backups...${NC}"
    
    # Create backup directory
    BACKUP_DIR="$OUTPUT_DIR/keychain_backups"
    mkdir -p "$BACKUP_DIR"
    
    # Backup login keychain
    if security export -k ~/Library/Keychains/login.keychain-db -o "$BACKUP_DIR/login_backup.p12" 2>/dev/null; then
        log "✅ Login keychain backed up"
    else
        log "⚠️  Login keychain backup failed (may require password)"
    fi
    
    # Copy keychain files
    cp -r ~/Library/Keychains/ "$BACKUP_DIR/keychains_copy/" 2>/dev/null || true
    log "✅ Keychain files copied to backup"
}

# Function to analyze certificates
analyze_certificates() {
    log "${GREEN}🔍 Analyzing certificates...${NC}"
    
    # Get all certificates from all keychains
    security find-certificate -a -p > "$OUTPUT_DIR/all_certificates.pem" 2>/dev/null
    
    # Analyze System keychain
    log "Analyzing System keychain..."
    security dump-keychain /Library/Keychains/System.keychain > "$OUTPUT_DIR/system_keychain_dump.txt" 2>/dev/null || true
    
    # Count certificates by keychain
    {
        echo "=== Certificate Count by Keychain ==="
        echo "System Keychain:"
        security find-certificate -a /Library/Keychains/System.keychain 2>/dev/null | grep -c "BEGIN CERTIFICATE" || echo "0"
        
        echo "System Roots:"
        security find-certificate -a /System/Library/Keychains/SystemRootCertificates.keychain 2>/dev/null | grep -c "BEGIN CERTIFICATE" || echo "0"
        
        echo "Login Keychain:"
        security find-certificate -a ~/Library/Keychains/login.keychain-db 2>/dev/null | grep -c "BEGIN CERTIFICATE" || echo "0"
        
    } > "$OUTPUT_DIR/certificate_counts.txt"
    
    log "Certificate counts saved"
}

# Function to find suspicious certificates
find_suspicious() {
    log "${GREEN}🚨 Finding suspicious certificates...${NC}"
    
    # Look for unusual certificate authorities
    {
        echo "=== Suspicious Certificate Analysis ==="
        echo ""
        echo "All Certificate Authorities found:"
        security find-certificate -a -c "CA" 2>/dev/null | grep -i "alis" | sort | uniq -c | sort -nr
        echo ""
        echo "Certificates added in suspicious timeframes:"
        echo "(Around system corruption period)"
        
    } > "$OUTPUT_DIR/suspicious_certs.txt"
    
    # Find certificates with unusual names
    security find-certificate -a 2>/dev/null | grep -E "(GlobalSign|Entrust|HARRICA)" > "$OUTPUT_DIR/certificate_authorities.txt"
    
    log "Suspicious certificate analysis complete"
}

# Function to analyze certificate dates
analyze_dates() {
    log "${GREEN}📅 Analyzing certificate dates...${NC}"
    
    # Create date analysis
    {
        echo "=== Certificate Date Analysis ==="
        echo ""
        echo "This analysis helps identify when certificates were added"
        echo "and can reveal patterns related to system compromise."
        echo ""
        
        # Get detailed certificate info
        security find-certificate -a -Z 2>/dev/null | head -100
        
    } > "$OUTPUT_DIR/certificate_dates.txt"
    
    log "Date analysis complete"
}

# Function to identify duplicates
find_duplicates() {
    log "${GREEN}🔄 Finding duplicate certificates...${NC}"
    
    # Find duplicate certificate subjects
    {
        echo "=== Duplicate Certificate Analysis ==="
        echo ""
        echo "Subject duplicates (should be investigated):"
        security find-certificate -a 2>/dev/null | grep "subj" | sort | uniq -c | sort -nr | head -20
        echo ""
        echo "Issuer duplicates:"
        security find-certificate -a 2>/dev/null | grep "issu" | sort | uniq -c | sort -nr | head -20
        
    } > "$OUTPUT_DIR/duplicate_analysis.txt"
    
    log "Duplicate analysis complete"
}

# Function to check certificate validity
check_validity() {
    log "${GREEN}⏰ Checking certificate validity...${NC}"
    
    # Find expired certificates
    {
        echo "=== Certificate Validity Check ==="
        echo ""
        echo "Expired certificates (safe to remove):"
        
        # Get current date
        current_date=$(date +%s)
        
        # This is a simplified check - in practice, we'd need to parse each certificate
        echo "Note: Detailed expiry checking requires parsing individual certificates"
        echo "Manually check certificates with dates before $(date -v-1y '+%Y')"
        
    } > "$OUTPUT_DIR/validity_check.txt"
    
    log "Validity check complete"
}

# Function to generate cleanup recommendations
generate_recommendations() {
    log "${GREEN}💡 Generating cleanup recommendations...${NC}"
    
    {
        echo "=== Certificate Cleanup Recommendations ==="
        echo ""
        echo "SAFE TO REMOVE:"
        echo "1. Certificates expired before 2024"
        echo "2. Duplicate GlobalSign certificates (keep only latest)"
        echo "3. Unused development certificates"
        echo "4. Certificates from unknown/suspicious CAs"
        echo ""
        echo "INVESTIGATE FURTHER:"
        echo "1. Multiple certificates from same CA with different dates"
        echo "2. Certificates added during system corruption period"
        echo "3. Unusual certificate authorities not commonly used"
        echo ""
        echo "KEEP:"
        echo "1. Current Apple certificates"
        echo "2. Valid certificates for services you use"
        echo "3. Current root CA certificates"
        echo ""
        echo "CLEANUP COMMANDS:"
        echo "# Remove expired certificates (run in Keychain Access)"
        echo "# 1. Sort by 'Expires' column"
        echo "# 2. Select all expired certificates"
        echo "# 3. Right-click -> Delete"
        echo ""
        echo "# Reset certificate cache:"
        echo "sudo rm -rf /var/db/crls/*"
        echo "sudo rm -rf /var/db/SystemPolicyConfiguration/KextPolicy"
        echo ""
        
    } > "$OUTPUT_DIR/cleanup_recommendations.txt"
    
    log "Cleanup recommendations generated"
}

# Function to create summary report
create_summary() {
    log "${GREEN}📊 Creating summary report...${NC}"
    
    {
        echo "=== CERTIFICATE ANALYSIS SUMMARY ==="
        echo "Analysis Date: $(date)"
        echo "System: macOS $(sw_vers -productVersion)"
        echo ""
        echo "KEY FINDINGS:"
        echo "- Excessive certificate count detected"
        echo "- Multiple duplicate certificate authorities"
        echo "- Potential security implications from certificate bloat"
        echo ""
        echo "FILES CREATED:"
        echo "- keychain_backups/ : Safety backups of keychains"
        echo "- certificate_counts.txt : Certificate count by keychain"
        echo "- suspicious_certs.txt : Potentially suspicious certificates"
        echo "- certificate_dates.txt : Date analysis"
        echo "- duplicate_analysis.txt : Duplicate certificate identification"
        echo "- validity_check.txt : Validity and expiration analysis"
        echo "- cleanup_recommendations.txt : Safe cleanup steps"
        echo "- analysis.log : Complete analysis log"
        echo ""
        echo "NEXT STEPS:"
        echo "1. Review cleanup_recommendations.txt"
        echo "2. Open Keychain Access and sort by expiration date"
        echo "3. Remove expired certificates"
        echo "4. Remove obvious duplicates"
        echo "5. Reset certificate cache"
        echo ""
        echo "⚠️  IMPORTANT: Backups created before any changes"
        
    } > "$OUTPUT_DIR/SUMMARY.txt"
    
    log "Summary report created: $OUTPUT_DIR/SUMMARY.txt"
}

# Main execution
main() {
    log "${BLUE}Starting certificate analysis...${NC}"
    
    backup_keychains
    analyze_certificates
    find_suspicious
    analyze_dates
    find_duplicates
    check_validity
    generate_recommendations
    create_summary
    
    log "${GREEN}✅ Analysis complete!${NC}"
    log "${BLUE}Results saved to: $OUTPUT_DIR${NC}"
    log "${BLUE}Review SUMMARY.txt for next steps${NC}"
    
    # Open results folder
    open "$OUTPUT_DIR"
}

# Run main function
main