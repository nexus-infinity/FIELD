function toMermaid(entities, relations) {
  // Define styles for each entity type
  const classDefinitions = [
    'classDef Trust fill:#f9d6d6,stroke:#a12222',
    'classDef UnitTrust fill:#fde8d6,stroke:#b25000',
    'classDef Company fill:#d6e5f9,stroke:#225ba1',
    'classDef Person fill:#d6f9e3,stroke:#22a147',
    'classDef PropertyAsset fill:#e5d6f9,stroke:#5722a1',
    'classDef BankRelationship fill:#f9f4d6,stroke:#a19722',
    'classDef OffshoreEntity fill:#f9d6e8,stroke:#a12271',
    'classDef RegistryRecord fill:#d6f9f7,stroke:#22a1a1'
  ];
  const id = e => e.EntityID;
  
  const label = e => {
    if (e.EntityType === "Company") return `${e.LegalName}\\nACN ${e.ACN || ""}`;
    if (e.EntityType === "Trust" || e.EntityType === "UnitTrust") return `${e.LegalName}\\nABN ${e.ABN || ""}`;
    return e.LegalName || e.EntityType;
  };
  
  const lines = ["graph TD", ...classDefinitions];
  
  // Add nodes
  for (const e of entities) {
    lines.push(`${id(e)}["${label(e)}"]:::${e.EntityType}`);
  }
  
  // Add relationships
  for (const r of relations) {
    const style = (r.verification_level || 0) >= 2 ? "-->" : "-.->";
    const lbl = r.type.replaceAll("_", " ");
    lines.push(`${r.from} ${style}|${lbl}| ${r.to}`);
  }
  
  return lines.join("\n");
}