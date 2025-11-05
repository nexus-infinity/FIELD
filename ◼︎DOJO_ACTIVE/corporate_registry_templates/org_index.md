# Rich Group Corporate Structure - Modular Analysis

## Layer Files
- `org_core.mmd` - Core corporate structure
- `org_debt.mmd` - Debt movements and financing
- `org_abn.mmd` - ABN/ACN switching patterns
- `org_addresses.mmd` - Address changes and timing
- `org_shadow.mmd` - Control and concealment patterns
- `org_verification.mmd` - Verification status overlays

## Notion Database Links
- [Debt Movements Database](https://www.notion.so/debt-movements)
- [Entity Relations](https://www.notion.so/entity-relations)
- [Address History](https://www.notion.so/address-history)
- [Verification Status](https://www.notion.so/verification-status)

## Interactive Views
Use these commands to generate different views:

### Full View
```bash
mmdc -i org_combined.mmd -o org_full.svg
```

### Layer-Specific Views
```bash
mmdc -i org_debt.mmd -o org_debt.svg
mmdc -i org_abn.mmd -o org_abn.svg
# etc
```

### Custom Combined Views
```bash
# Example: Debt + ABN switches
cat org_core.mmd org_debt.mmd org_abn.mmd > org_custom.mmd
mmdc -i org_custom.mmd -o org_custom.svg
```