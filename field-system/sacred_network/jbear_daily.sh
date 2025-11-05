#!/bin/bash
# JBear Daily Command Suite
# One-line commands that actually solve YOUR problems

# ============================================================================
# YOUR CONTACT PROBLEM - 80% obvious duplicates
# ============================================================================

# Find all JB Rich duplicates RIGHT NOW
jb_find_duplicates() {
    echo "🐻 Finding YOUR duplicate contacts..."
    osascript -e 'tell application "Contacts" to name of every person whose (first name contains "JB" or first name contains "J.B." or last name contains "Rich")'
}

# Quick merge duplicates with same phone
jb_merge_phones() {
    python3 ~/FIELD/field-system/sacred_network/sovereign_contacts/sailing_intelligence_contacts.py --bearflow
}

# ============================================================================
# YOUR TERMINAL WORKFLOW - Common patterns
# ============================================================================

# Quick sync to git (YOUR most common pattern)
gsync() {
    git add -A && git commit -m "sync: $(date +%Y%m%d_%H%M)" && git push
}

# Jump to sacred network (YOUR workspace)
field() {
    cd ~/FIELD/field-system/sacred_network
}

# Run orchestration (YOUR tool deployment)
orchestrate() {
    cd ~/FIELD/field-system/sacred_network && python3 field_orchestration.py
}

# ============================================================================
# YOUR FILE ORGANIZATION - By weight and usage
# ============================================================================

# Find what you worked on TODAY
today() {
    echo "📝 Files you modified today:"
    find ~/FIELD -type f -mtime -1 -exec ls -la {} \; | head -20
}

# Find heaviest files (by YOUR semantic weight)
heavy() {
    echo "🏋️ Your heaviest semantic files:"
    python3 -c "
from pathlib import Path
import datetime

sacred_path = Path.home() / 'FIELD' / 'field-system' / 'sacred_network'
files = []
for f in sacred_path.rglob('*.py'):
    try:
        content = f.read_text().lower()
        weight = 1.0
        if 'sailing' in content or 'bearflow' in content: weight *= 2
        if 'contact' in content: weight *= 1.5
        age_days = (datetime.datetime.now().timestamp() - f.stat().st_mtime) / 86400
        if age_days < 1: weight *= 2
        files.append((weight, f.name))
    except: pass
for w, n in sorted(files, reverse=True)[:10]:
    print(f'{w:.1f} - {n}')
"
}

# ============================================================================
# YOUR ABLETON WORKFLOW - Find patterns
# ============================================================================

# Find your Ableton projects
ableton_projects() {
    echo "🎵 Your Ableton projects:"
    find ~/Music/Ableton -name "*.als" -type f 2>/dev/null | head -20
}

# Find unused samples (can delete)
ableton_cleanup() {
    echo "🧹 Finding unused Ableton samples..."
    # This would scan for orphaned .aif and .wav files
    find ~/Music/Ableton -name "*.aif" -o -name "*.wav" | while read file; do
        # Check if referenced in any .als project
        grep -l "$(basename "$file")" ~/Music/Ableton/**/*.als 2>/dev/null || echo "Unused: $file"
    done
}

# ============================================================================
# YOUR MORNING ROUTINE - Automated
# ============================================================================

jb_morning() {
    echo "☀️ Good morning JBear! Starting your routine..."
    echo ""
    
    echo "1️⃣ Checking for duplicate contacts..."
    jb_find_duplicates | head -5
    echo ""
    
    echo "2️⃣ Your recent work:"
    today | head -5
    echo ""
    
    echo "3️⃣ Sacred network status:"
    field && ls -la *.py | head -5
    echo ""
    
    echo "4️⃣ Git status:"
    git status --short
    echo ""
    
    echo "✅ Morning routine complete!"
}

# ============================================================================
# YOUR SAILING INTELLIGENCE - Quick access
# ============================================================================

# Run BearFlow on contacts
bearflow() {
    python3 ~/FIELD/field-system/sacred_network/sovereign_contacts/sailing_intelligence_contacts.py --bearflow --sailing
}

# Analyze contacts
contacts() {
    python3 ~/FIELD/field-system/sacred_network/sovereign_contacts/fractal_contact_wrapper.py --analyze
}

# Weight your files
weight() {
    python3 ~/FIELD/field-system/sacred_network/jbear_sailing_examples.py
}

# ============================================================================
# ACTIVATE YOUR ALIASES
# ============================================================================

echo "🐻 JBear Daily Commands Loaded!"
echo ""
echo "YOUR SHORTCUTS:"
echo "  jb_morning     - Run your morning routine"
echo "  gsync          - Quick git sync"
echo "  field          - Jump to sacred network"
echo "  today          - See what you worked on today"
echo "  heavy          - Find your most important files"
echo "  bearflow       - Run BearFlow analysis"
echo "  contacts       - Analyze contacts"
echo "  orchestrate    - Deploy field tools"
echo ""
echo "Type 'jb_morning' to start your day!"
