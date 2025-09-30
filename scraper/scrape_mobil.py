#!/usr/bin/env python3
"""
Mobile Plans Scraper for Denmark
Scrapes mobile subscription plans from major Danish providers
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

# Import mobile provider scrapers
from telia_mobil import scrape_telia_mobil
from telenor_mobil import scrape_telenor_mobil
from yousee_mobil import scrape_yousee_mobil
from oister import scrape_oister
from lebara import scrape_lebara
from greentel import scrape_greentel
from hallo_mobil import scrape_hallo_mobil
from cbb_mobil import scrape_cbb_mobil
from stofa_mobil import scrape_stofa_mobil
from waoo_mobil import scrape_waoo_mobil
from norlys_mobil import scrape_norlys_mobil
from boxer_mobil import scrape_boxer_mobil
from callme import scrape_callme
from lycamobile import scrape_lycamobile
from gomore import scrape_gomore

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper_mobil.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Mobile provider configuration
MOBILE_PROVIDERS = [
    {
        'name': 'Telia',
        'scraper': scrape_telia_mobil,
        'enabled': True
    },
    {
        'name': 'Telenor',
        'scraper': scrape_telenor_mobil,
        'enabled': True
    },
    {
        'name': 'YouSee',
        'scraper': scrape_yousee_mobil,
        'enabled': True
    },
    {
        'name': 'Oister',
        'scraper': scrape_oister,
        'enabled': True
    },
    {
        'name': 'Lebara',
        'scraper': scrape_lebara,
        'enabled': True
    },
    {
        'name': 'Greentel',
        'scraper': scrape_greentel,
        'enabled': True
    },
    {
        'name': 'Hallo Mobil',
        'scraper': scrape_hallo_mobil,
        'enabled': True
    },
    {
        'name': 'CBB',
        'scraper': scrape_cbb_mobil,
        'enabled': True
    },
    {
        'name': 'Stofa',
        'scraper': scrape_stofa_mobil,
        'enabled': True
    },
    {
        'name': 'Waoo',
        'scraper': scrape_waoo_mobil,
        'enabled': True
    },
    {
        'name': 'Norlys',
        'scraper': scrape_norlys_mobil,
        'enabled': True
    },
    {
        'name': 'Boxer',
        'scraper': scrape_boxer_mobil,
        'enabled': True
    },
    {
        'name': 'Callme',
        'scraper': scrape_callme,
        'enabled': True
    },
    {
        'name': 'Lycamobile',
        'scraper': scrape_lycamobile,
        'enabled': True
    },
    {
        'name': 'Gomore',
        'scraper': scrape_gomore,
        'enabled': True
    }
]

def load_existing_data() -> List[Dict[str, Any]]:
    """Load existing mobile data from JSON file"""
    data_file = Path('../data/mobil.json')
    if data_file.exists():
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load existing data: {e}")
    return []

def save_data(data: List[Dict[str, Any]]) -> None:
    """Save mobile data to JSON file"""
    data_file = Path('../data/mobil.json')
    data_file.parent.mkdir(exist_ok=True)
    
    try:
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved {len(data)} mobile plans to {data_file}")
    except Exception as e:
        logger.error(f"Could not save data: {e}")
        raise

def scrape_mobile_providers(scraper_type: str = 'full') -> List[Dict[str, Any]]:
    """Scrape mobile plans from all enabled providers"""
    all_plans = []
    successful_providers = 0
    failed_providers = 0
    
    logger.info(f"Starting mobile scraping (type: {scraper_type})")
    
    for provider_config in MOBILE_PROVIDERS:
        if not provider_config['enabled']:
            logger.info(f"Skipping disabled provider: {provider_config['name']}")
            continue
            
        provider_name = provider_config['name']
        scraper_func = provider_config['scraper']
        
        try:
            logger.info(f"Scraping {provider_name}...")
            
            if scraper_type == 'light':
                # For light scraping, only check a few key providers
                if provider_name not in ['Telia', 'Telenor', 'YouSee', 'Oister', 'Lebara']:
                    logger.info(f"Skipping {provider_name} in light mode")
                    continue
            
            plans = scraper_func()
            
            if plans:
                # Add metadata to each plan
                for plan in plans:
                    plan['scraped_at'] = datetime.now().isoformat()
                    plan['provider'] = provider_name
                
                all_plans.extend(plans)
                successful_providers += 1
                logger.info(f"✓ {provider_name}: {len(plans)} plans found")
            else:
                logger.warning(f"⚠ {provider_name}: No plans found")
                failed_providers += 1
                
        except Exception as e:
            logger.error(f"✗ {provider_name}: Error - {e}")
            failed_providers += 1
            continue
    
    logger.info(f"Scraping completed: {successful_providers} successful, {failed_providers} failed")
    logger.info(f"Total plans collected: {len(all_plans)}")
    
    return all_plans

def detect_changes(old_data: List[Dict[str, Any]], new_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Detect changes between old and new data"""
    changes = {
        'new_plans': 0,
        'updated_plans': 0,
        'removed_plans': 0,
        'price_changes': 0,
        'promotion_changes': 0
    }
    
    # Create lookup dictionaries
    old_lookup = {f"{plan.get('udbyder', '')}-{plan.get('data_GB', '')}-{plan.get('pris_mdr', '')}": plan for plan in old_data}
    new_lookup = {f"{plan.get('udbyder', '')}-{plan.get('data_GB', '')}-{plan.get('pris_mdr', '')}": plan for plan in new_data}
    
    # Find new plans
    for key, plan in new_lookup.items():
        if key not in old_lookup:
            changes['new_plans'] += 1
    
    # Find removed plans
    for key, plan in old_lookup.items():
        if key not in new_lookup:
            changes['removed_plans'] += 1
    
    # Find updated plans
    for key, new_plan in new_lookup.items():
        if key in old_lookup:
            old_plan = old_lookup[key]
            
            # Check for price changes
            if old_plan.get('pris_mdr') != new_plan.get('pris_mdr'):
                changes['price_changes'] += 1
                changes['updated_plans'] += 1
            
            # Check for promotion changes
            if old_plan.get('kampagne') != new_plan.get('kampagne'):
                changes['promotion_changes'] += 1
                if changes['updated_plans'] == 0:  # Don't double count
                    changes['updated_plans'] += 1
    
    return changes

def main():
    """Main scraping function"""
    scraper_type = os.getenv('SCRAPER_TYPE', 'full')
    force_update = os.getenv('FORCE_UPDATE', 'false').lower() == 'true'
    
    logger.info(f"Mobile scraper started - Type: {scraper_type}, Force: {force_update}")
    
    # Load existing data
    existing_data = load_existing_data()
    logger.info(f"Loaded {len(existing_data)} existing mobile plans")
    
    # Scrape new data
    new_data = scrape_mobile_providers(scraper_type)
    
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
        logger.info("=== SCRAPING SUMMARY ===")
        logger.info(f"Total providers: {len(MOBILE_PROVIDERS)}")
        logger.info(f"Total plans: {len(new_data)}")
        logger.info(f"New plans: {changes['new_plans']}")
        logger.info(f"Updated plans: {changes['updated_plans']}")
        logger.info(f"Removed plans: {changes['removed_plans']}")
        logger.info(f"Price changes: {changes['price_changes']}")
        logger.info(f"Promotion changes: {changes['promotion_changes']}")
    else:
        logger.info("No changes detected. Data not updated.")

if __name__ == '__main__':
    main()
