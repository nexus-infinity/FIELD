# Sovereign Timeline Integration

This is an Obsidian-based timeline interface integrated with the Sovereign Drive system.

## Setup Instructions

1. Open this folder as an Obsidian vault
2. Install the required community plugins:
   - Timeline
   - Dataview
   - Templater

## Usage

### Creating Timeline Entries
1. Use the template in `templates/timeline_entry.md` for new entries
2. Store all timeline entries in the `timeline_data` directory
3. Make sure to fill out all metadata fields in the frontmatter

### Viewing the Timeline
1. Open `Timeline.md` for the main timeline view
2. Use the dataview tables and timeline visualization to explore entries
3. All entries are automatically sorted by date and time

### Sovereign Data Integration
- All timeline entries maintain links to sovereign data
- Use the "Sovereign Data Links" section to reference related files
- Timeline data is stored in the sovereign drive structure

## Directory Structure
- `.obsidian/` - Obsidian configuration
- `templates/` - Timeline entry templates
- `timeline_data/` - Timeline entries and attachments
- `Timeline.md` - Main timeline view

