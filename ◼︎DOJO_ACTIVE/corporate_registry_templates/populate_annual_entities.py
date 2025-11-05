#!/usr/bin/env python3
"""
BERJAK | NEXUS | INFINITY FRE Annual Entity Population Runner
Coordinates the population of annual corporate entity data
"""

from pathlib import Path
import logging
from datetime import datetime
from src.annual_entity_population import AnnualEntityPopulator
from src.historical_data_gatherer import HistoricalDataGatherer

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler('annual_population.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger('Annual_Population')

def main():
    logger = setup_logging()
    base_dir = Path('/Users/jbear/FIELD/◼︎DOJO_ACTIVE')
    
    logger.info("Starting annual entity population process")
    start_time = datetime.now()
    
    try:
        # Initialize processors
        populator = AnnualEntityPopulator(base_dir)
        gatherer = HistoricalDataGatherer(base_dir)
        
        # Generate base annual records
        logger.info("Generating annual records")
        annual_records = populator.generate_annual_records()
        logger.info(f"Generated {len(annual_records)} annual records")
        
        # Gather historical data points
        logger.info("Gathering historical data")
        data_points = []
        for record in annual_records:
            data_point = gatherer.gather_historical_points(
                record.entity_name,
                record.year
            )
            data_points.append(data_point)
        
        # Write outputs
        logger.info("Writing annual records to CSV")
        populator.write_annual_records(annual_records)
        
        logger.info("Generating annual manifest")
        populator.generate_annual_manifest(annual_records)
        
        logger.info("Exporting historical data points")
        gatherer.export_to_json(data_points)
        
        # Log completion
        end_time = datetime.now()
        duration = end_time - start_time
        logger.info(f"Annual population completed in {duration}")
        logger.info(f"Total records processed: {len(annual_records)}")
        
    except Exception as e:
        logger.error(f"Error during annual population: {str(e)}")
        raise

if __name__ == '__main__':
    main()