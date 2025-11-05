#!/usr/bin/env python3
"""
BERJAK | NEXUS | INFINITY FRE Entity Population Runner
Coordinates the scanning, extraction, and population of corporate entity data
"""

import logging
from pathlib import Path
from datetime import datetime
from src.entity_timeline_extractor import EntityTimelineExtractor
from src.document_processor import DocumentProcessor
from src.annual_entity_population import AnnualEntityPopulator

def setup_logging():
    """Configure logging for the population process"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler('entity_population.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger('Entity_Population')

def main():
    logger = setup_logging()
    base_dir = Path('/Users/jbear/FIELD/◼︎DOJO_ACTIVE')
    start_time = datetime.now()
    
    try:
        # Initialize processors
        logger.info("Initializing processors...")
        doc_processor = DocumentProcessor()
        timeline_extractor = EntityTimelineExtractor(base_dir)
        entity_populator = AnnualEntityPopulator(base_dir)
        
        # Step 1: Process and extract content from all relevant files
        logger.info("Processing documents...")
        for file_path in base_dir.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in ['.pdf', '.doc', '.docx', '.txt', '.csv', '.xlsx']:
                result = doc_processor.process_file(file_path)
                if result:
                    logger.info(f"Processed {file_path}")
        
        processing_report = doc_processor.generate_processing_report()
        logger.info(f"Document processing complete. Processed {processing_report['total_files']} files")
        
        # Step 2: Generate entity timelines
        logger.info("Generating entity timelines...")
        timeline_extractor.scan_files()
        timeline_extractor.generate_entity_timelines()
        timeline_extractor.export_timelines()
        
        # Step 3: Generate annual records
        logger.info("Generating annual entity records...")
        annual_records = entity_populator.generate_annual_records()
        entity_populator.write_annual_records(annual_records)
        entity_populator.generate_annual_manifest(annual_records)
        
        # Log completion
        end_time = datetime.now()
        duration = end_time - start_time
        logger.info(f"Entity population completed in {duration}")
        logger.info("Generation Summary:")
        logger.info(f"- Documents Processed: {processing_report['total_files']}")
        logger.info(f"- Entity Timelines Generated: {len(timeline_extractor.timelines)}")
        logger.info(f"- Annual Records Created: {len(annual_records)}")
        
    except Exception as e:
        logger.error(f"Error during entity population: {str(e)}")
        raise

if __name__ == '__main__':
    main()