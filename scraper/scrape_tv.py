#!/usr/bin/env python3
"""
TV Packages Scraper for Denmark
Scrapes TV package plans from major Danish providers
"""

import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# Add providers directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'providers'))

# Import TV provider scrapers
from yousee_tv import scrape_yousee_tv
from waoo_tv import scrape_waoo_tv
from stofa_tv import scrape_stofa_tv
from boxer_tv import scrape_boxer_tv
from norlys_tv import scrape_norlys_tv
from telia_tv import scrape_telia_tv
from allente_tv import scrape_allente_tv
from tdc_tv import scrape_tdc_tv
from telenor_tv import scrape_telenor_tv
from altibox_tv import scrape_altibox_tv
from kviknet_tv import scrape_kviknet_tv
from cbb_tv import scrape_cbb_tv
from hiper_tv import scrape_hiper_tv
from fastspeed_tv import scrape_fastspeed_tv
from ewii_tv import scrape_ewii_tv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper_tv.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# TV provider configuration
TV_PROVIDERS = [
    {
        'name': 'YouSee',
        'scraper': scrape_yousee_tv,
        'enabled': True
    },
    {
        'name': 'Waoo',
        'scraper': scrape_waoo_tv,
        'enabled': True
    },
    {
        'name': 'Stofa',
        'scraper': scrape_stofa_tv,
        'enabled': True
    },
    {
        'name': 'Boxer',
        'scraper': scrape_boxer_tv,
        'enabled': True
    },
    {
        'name': 'Norlys',
        'scraper': scrape_norlys_tv,
        'enabled': True
    },
    {
        'name': 'Telia TV',
        'scraper': scrape_telia_tv,
        'enabled': True
    },
    {
        'name': 'Allente',
        'scraper': scrape_allente_tv,
        'enabled': True
    },
    {
        'name': 'TDC',
        'scraper': scrape_tdc_tv,
        'enabled': True
    },
    {
        'name': 'Telenor',
        'scraper': scrape_telenor_tv,
        'enabled': True
    },
    {
        'name': 'Altibox',
        'scraper': scrape_altibox_tv,
        'enabled': True
    },
    {
        'name': 'Kviknet',
        'scraper': scrape_kviknet_tv,
        'enabled': True
    },
    {
        'name': 'CBB',
        'scraper': scrape_cbb_tv,
        'enabled': True
    },
    {
        'name': 'Hiper',
        'scraper': scrape_hiper_tv,
        'enabled': True
    },
    {
        'name': 'Fastspeed',
        'scraper': scrape_fastspeed_tv,
        'enabled': True
    },
    {
        'name': 'Ewii',
        'scraper': scrape_ewii_tv,
        'enabled': True
    }
]

def load_existing_data() -> List[Dict[str, Any]]:
    """Load existing TV data from JSON file"""
    data_file = Path('../data/tv.json')
    if data_file.exists():
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load existing data: {e}")
    return []

def save_data(data: List[Dict[str, Any]]) -> None:
    """Save TV data to JSON file"""
    data_file = Path('../data/tv.json')
    data_file.parent.mkdir(exist_ok=True)
    
    try:
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved {len(data)} TV packages to {data_file}")
    except Exception as e:
        logger.error(f"Could not save data: {e}")
        raise

def scrape_tv_providers(scraper_type: str = 'full') -> List[Dict[str, Any]]:
    """Scrape TV packages from all enabled providers"""
    all_packages = []
    successful_providers = 0
    failed_providers = 0
    
    logger.info(f"Starting TV scraping (type: {scraper_type})")
    
    for provider_config in TV_PROVIDERS:
        if not provider_config['enabled']:
            logger.info(f"Skipping disabled provider: {provider_config['name']}")
            continue
            
        provider_name = provider_config['name']
        scraper_func = provider_config['scraper']
        
        try:
            logger.info(f"Scraping {provider_name}...")
            
            if scraper_type == 'light':
                # For light scraping, only check a few key providers
                if provider_name not in ['YouSee', 'Waoo', 'Stofa', 'Boxer', 'Norlys']:
                    logger.info(f"Skipping {provider_name} in light mode")
                    continue
            
            packages = scraper_func()
            
            if packages:
                # Add metadata to each package
                for package in packages:
                    package['scraped_at'] = datetime.now().isoformat()
                    package['provider'] = provider_name
                
                all_packages.extend(packages)
                successful_providers += 1
                logger.info(f"✓ {provider_name}: {len(packages)} packages found")
            else:
                logger.warning(f"⚠ {provider_name}: No packages found")
                failed_providers += 1
                
        except Exception as e:
            logger.error(f"✗ {provider_name}: Error - {e}")
            failed_providers += 1
            continue
    
    logger.info(f"Scraping completed: {successful_providers} successful, {failed_providers} failed")
    logger.info(f"Total packages collected: {len(all_packages)}")
    
    return all_packages

def detect_changes(old_data: List[Dict[str, Any]], new_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Detect changes between old and new data"""
    changes = {
        'new_packages': 0,
        'updated_packages': 0,
        'removed_packages': 0,
        'price_changes': 0,
        'promotion_changes': 0
    }
    
    # Create lookup dictionaries
    old_lookup = {f"{pkg.get('udbyder', '')}-{pkg.get('pakke_navn', '')}-{pkg.get('pris_mdr', '')}": pkg for pkg in old_data}
    new_lookup = {f"{pkg.get('udbyder', '')}-{pkg.get('pakke_navn', '')}-{pkg.get('pris_mdr', '')}": pkg for pkg in new_data}
    
    # Find new packages
    for key, package in new_lookup.items():
        if key not in old_lookup:
            changes['new_packages'] += 1
    
    # Find removed packages
    for key, package in old_lookup.items():
        if key not in new_lookup:
            changes['removed_packages'] += 1
    
    # Find updated packages
    for key, new_package in new_lookup.items():
        if key in old_lookup:
            old_package = old_lookup[key]
            
            # Check for price changes
            if old_package.get('pris_mdr') != new_package.get('pris_mdr'):
                changes['price_changes'] += 1
                changes['updated_packages'] += 1
            
            # Check for promotion changes
            if old_package.get('kampagne') != new_package.get('kampagne'):
                changes['promotion_changes'] += 1
                if changes['updated_packages'] == 0:  # Don't double count
                    changes['updated_packages'] += 1
    
    return changes

def main():
    """Main scraping function"""
    scraper_type = os.getenv('SCRAPER_TYPE', 'full')
    force_update = os.getenv('FORCE_UPDATE', 'false').lower() == 'true'
    
    logger.info(f"TV scraper started - Type: {scraper_type}, Force: {force_update}")
    
    # Load existing data
    existing_data = load_existing_data()
    logger.info(f"Loaded {len(existing_data)} existing TV packages")
    
    # Scrape new data
    new_data = scrape_tv_providers(scraper_type)
    
    if not new_data:
        logger.error("No data scraped. Exiting.")
        return
    
    # Detect changes
    changes = detect_changes(existing_data, new_data)
    logger.info(f"Changes detected: {changes}")
    
    # Save data if there are changes or force update is enabled
    if any(changes.values()) or force_update:
        save_data(new_data)
        logger.info("Data saved successfully")
        
        # Log summary
        logger.info("=== TV SCRAPING SUMMARY ===")
        logger.info(f"Total providers: {len(TV_PROVIDERS)}")
        logger.info(f"Total packages: {len(new_data)}")
        logger.info(f"New packages: {changes['new_packages']}")
        logger.info(f"Updated packages: {changes['updated_packages']}")
        logger.info(f"Removed packages: {changes['removed_packages']}")
        logger.info(f"Price changes: {changes['price_changes']}")
        logger.info(f"Promotion changes: {changes['promotion_changes']}")
    else:
        logger.info("No changes detected. Data not updated.")

if __name__ == '__main__':
    main()
