const fs = require('fs');
const path = require('path');

// Read the files
const entities = JSON.parse(fs.readFileSync('entities.json', 'utf8'));
const relations = JSON.parse(fs.readFileSync('relations.json', 'utf8'));

// Import the toMermaid function
const toMermaidStr = fs.readFileSync('toMermaid.js', 'utf8');
eval(toMermaidStr); // This makes the toMermaid function available

// Generate the Mermaid diagram
const mermaidContent = toMermaid(entities, relations);

// Write to org.mmd
fs.writeFileSync('org.mmd', mermaidContent);

console.log('Generated org.mmd with Mermaid diagram content');
console.log('To generate SVG, install @mermaid-js/mermaid-cli and run:');
console.log('mmdc -i org.mmd -o org.svg');