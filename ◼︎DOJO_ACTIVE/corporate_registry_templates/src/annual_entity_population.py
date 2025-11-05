#!/usr/bin/env python3
"""
BERJAK | NEXUS | INFINITY FRE Annual Entity Population
Comprehensive population of annual corporate entity data
"""

import csv
import json
from pathlib import Path
from datetime import datetime, date
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class CorporateYear:
    year: int
    entity_name: str
    abn: str
    acn: str
    status: str
    jurisdiction: str
    registered_address: str
    directors: List[str]
    principal_place_business: str
    annual_review_date: date
    last_modified: date
    document_references: List[str]

class AnnualEntityPopulator:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.entities_data = {}
        self.years_range = range(2012, 2026)  # Adjust range as needed
        self.load_existing_data()

    def load_existing_data(self):
        """Load existing entity data from CSV"""
        entities_file = self.base_dir / 'corporate_registry_templates/templates/entities.csv'
        if entities_file.exists():
            with open(entities_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['Entity Name']:
                        self.entities_data[row['Entity Name']] = row

    def determine_active_years(self, entity_data: Dict) -> List[int]:
        """Determine years when entity was active based on creation/cessation dates"""
        creation_date = entity_data.get('Date of creation')
        cessation_date = entity_data.get('Date of cessation')
        
        start_year = int(creation_date.split('-')[0]) if creation_date else min(self.years_range)
        end_year = int(cessation_date.split('-')[0]) if cessation_date else max(self.years_range)
        
        return list(range(start_year, end_year + 1))

    def generate_annual_records(self):
        """Generate annual records for each entity"""
        annual_records = []
        
        for entity_name, entity_data in self.entities_data.items():
            active_years = self.determine_active_years(entity_data)
            
            for year in active_years:
                record = CorporateYear(
                    year=year,
                    entity_name=entity_name,
                    abn=entity_data.get('ABN', ''),
                    acn=entity_data.get('ACN', ''),
                    status=entity_data.get('Status', 'Active'),
                    jurisdiction=entity_data.get('Jurisdiction', ''),
                    registered_address=entity_data.get('Registered Office', ''),
                    directors=entity_data.get('Directors / Controllers', '').split(';'),
                    principal_place_business=entity_data.get('Registered Office', ''),
                    annual_review_date=date(year, 7, 1),  # Default to July 1st
                    last_modified=datetime.now().date(),
                    document_references=[]
                )
                annual_records.append(record)
        
        return annual_records

    def write_annual_records(self, records: List[CorporateYear]):
        """Write annual records to CSV file"""
        output_file = self.base_dir / 'corporate_registry_templates/output/annual_entity_records.csv'
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        fieldnames = [
            'Year', 'Entity Name', 'ABN', 'ACN', 'Status', 'Jurisdiction',
            'Registered Address', 'Directors', 'Principal Place of Business',
            'Annual Review Date', 'Last Modified', 'Document References'
        ]
        
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for record in records:
                writer.writerow({
                    'Year': record.year,
                    'Entity Name': record.entity_name,
                    'ABN': record.abn,
                    'ACN': record.acn,
                    'Status': record.status,
                    'Jurisdiction': record.jurisdiction,
                    'Registered Address': record.registered_address,
                    'Directors': ';'.join(record.directors),
                    'Principal Place of Business': record.principal_place_business,
                    'Annual Review Date': record.annual_review_date.isoformat(),
                    'Last Modified': record.last_modified.isoformat(),
                    'Document References': ';'.join(record.document_references)
                })

    def generate_annual_manifest(self, records: List[CorporateYear]):
        """Generate a manifest of the annual population"""
        manifest = {
            'generation_date': datetime.now().isoformat(),
            'total_records': len(records),
            'years_covered': sorted(list(set(r.year for r in records))),
            'entities_covered': sorted(list(set(r.entity_name for r in records))),
            'records_per_year': {},
            'entities_per_year': {}
        }
        
        for year in self.years_range:
            year_records = [r for r in records if r.year == year]
            manifest['records_per_year'][year] = len(year_records)
            manifest['entities_per_year'][year] = len(set(r.entity_name for r in year_records))
        
        manifest_file = self.base_dir / 'corporate_registry_templates/output/annual_population_manifest.json'
        with open(manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)

def main():
    base_dir = Path('/Users/jbear/FIELD/◼︎DOJO_ACTIVE')
    populator = AnnualEntityPopulator(base_dir)
    
    # Generate annual records
    annual_records = populator.generate_annual_records()
    
    # Write records to CSV
    populator.write_annual_records(annual_records)
    
    # Generate manifest
    populator.generate_annual_manifest(annual_records)

if __name__ == '__main__':
    main()