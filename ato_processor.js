function processAtoRows(grid, ix, ctx) {
  const atoRows = [];
  const docs = [];
  const prov = [];
  
  for (let i = 1; i < grid.length; i++) {
    const r = grid[i];
    if (!r || r.every(cell => !cell)) continue;
    const accType = tidyType(val(r[ix.type]));
    if (!accType) continue;
    const entityName = val(r[ix.name]);
    atoRows.push({
      "ATO Account": `${accType} — ${val(r[ix.abn]) || ""}`.trim(),
      "Type": accType,
      "ABN": val(r[ix.abn]),
      "TFN": val(r[ix.tfn]),
      "Status": "Unknown",
      "ATO Reference": val(r[ix.ref]),
      "Primary Entity": entityName,
      "Notes": `[draft] imported from ${ctx.name}`
    });
    pushDoc(docs, `${ctx.name} — ${val(r[ix.date]) || "undated"}`, "ATO Lodgement", val(r[ix.date]), "Australia", entityName, "", "", driveUrl(ctx.id), "[draft]");
    prov.push(provLine("ato_accounts.csv", ctx, i, r.join(", ")));
  }
  return {ato: atoRows, docs, prov};
}

function tidyType(s) {
  s = (s || "").toUpperCase();
  if (/BAS|GST/.test(s)) return "BAS/GST";
  if (/PAYG/.test(s)) return "PAYG Withholding";
  if (/FBT/.test(s)) return "Fringe Benefits";
  if (/SUPER/.test(s)) return "Superannuation";
  if (/INCOME|TAX/.test(s)) return "Income Tax";
  return s ? "Other" : "";
}

// ------------- Utils -------------
function pick(h, keys) {
  for (const k of keys) {
    const i = h.indexOf(k);
    if (i >= 0) return i;
  }
  return -1;
}

function val(v) {
  return (v == null) ? "" : String(v).trim();
}

function driveUrl(id) {
  return `https://drive.google.com/open?id=${id}`;
}

function inferJurisdiction(name) {
  return /BEKB|Rothschild|CHF|Switz/i.test(name || "") ? "Switzerland" : "Australia";
}

function pushDoc(docs, title, type, date, jur, ent, ba, aa, url, notes) {
  docs.push({
    "Document Title": title,
    "Type": type,
    "Date": date,
    "Jurisdiction": jur,
    "Entities": ent,
    "Bank Accounts": ba,
    "ATO Accounts": aa,
    "Intercompany Loans": "",
    "Source URL": url,
    "Notes": notes
  });
}

function toCsv(rows) {
  if (!rows.length) return "";
  const heads = Object.keys(rows[0]);
  const esc = v => `"${String(v ?? "").replace(/"/g, '""')}"`;
  return [heads.join(",")].concat(rows.map(r => heads.map(h => esc(r[h])).join(","))).join("\n");
}

function getOrCreateFolder(name) {
  const folders = DriveApp.getFoldersByName(name);
  return folders.hasNext() ? folders.next() : DriveApp.createFolder(name);
}

function writeCsv(name, csv, folder) {
  if (csv) folder.createFile(Utilities.newBlob(csv, "text/csv", name));
}

function writeJsonl(name, text, folder) {
  if (text) folder.createFile(Utilities.newBlob(text, "application/json", name));
}

function provLine(csv, ctx, row, snippet) {
  return {
    csv,
    file_path: ctx.name,
    sheet: ctx.sheet,
    row,
    source: driveUrl(ctx.id),
    snippet: String(snippet || "").slice(0, 200)
  };
}