#!/usr/bin/env python3
"""
Fiber Internet Scraper for Denmark
Scrapes fiber internet plans from major Danish providers
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

# Import provider scrapers
from hiper import scrape_hiper
from yousee import scrape_yousee
from telia import scrape_telia
from stofa import scrape_stofa
from telenor import scrape_telenor
from waoo import scrape_waoo
from kviknet import scrape_kviknet
from cbb import scrape_cbb
from altibox import scrape_altibox
from fibia import scrape_fibia
from norlys import scrape_norlys
from energi_fyn import scrape_energi_fyn
from seas_nve import scrape_seas_nve

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper/scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Provider configuration
PROVIDERS = [
    {
        'name': 'Hiper',
        'scraper': scrape_hiper,
        'enabled': True
    },
    {
        'name': 'YouSee',
        'scraper': scrape_yousee,
        'enabled': True
    },
    {
        'name': 'Telia',
        'scraper': scrape_telia,
        'enabled': True
    },
    {
        'name': 'Stofa',
        'scraper': scrape_stofa,
        'enabled': True
    },
    {
        'name': 'Telenor',
        'scraper': scrape_telenor,
        'enabled': True
    },
    {
        'name': 'Waoo',
        'scraper': scrape_waoo,
        'enabled': True
    },
    {
        'name': 'Kviknet',
        'scraper': scrape_kviknet,
        'enabled': True
    },
    {
        'name': 'CBB',
        'scraper': scrape_cbb,
        'enabled': True
    },
    {
        'name': 'Altibox',
        'scraper': scrape_altibox,
        'enabled': False  # Disable if not available
    },
    {
        'name': 'Fibia',
        'scraper': scrape_fibia,
        'enabled': False  # Disable if not available
    },
    {
        'name': 'Norlys',
        'scraper': scrape_norlys,
        'enabled': True
    },
    {
        'name': 'Energi Fyn',
        'scraper': scrape_energi_fyn,
        'enabled': True
    },
    {
        'name': 'SEAS-NVE',
        'scraper': scrape_seas_nve,
        'enabled': True
    }
]

def normalize_speed(speed_str: str) -> int:
    """Normalize speed values to Mbit/s"""
    if not speed_str:
        return 0
    
    speed_str = str(speed_str).lower().replace(' ', '')
    
    # Handle Gbit/s
    if 'gbit' in speed_str or 'gb' in speed_str:
        try:
            value = float(speed_str.replace('gbit', '').replace('gb', '').replace('/s', ''))
            return int(value * 1000)
        except:
            pass
    
    # Handle Mbit/s
    if 'mbit' in speed_str or 'mb' in speed_str:
        try:
            value = float(speed_str.replace('mbit', '').replace('mb', '').replace('/s', ''))
            return int(value)
        except:
            pass
    
    # Try to extract number
    try:
        import re
        numbers = re.findall(r'\d+', speed_str)
        if numbers:
            return int(numbers[0])
    except:
        pass
    
    return 0

def normalize_price(price_str: str) -> int:
    """Normalize price values to DKK"""
    if not price_str:
        return 0
    
    price_str = str(price_str).replace(' ', '').replace('kr', '').replace('dkk', '').replace(',', '.')
    
    try:
        import re
        numbers = re.findall(r'\d+\.?\d*', price_str)
        if numbers:
            return int(float(numbers[0]))
    except:
        pass
    
    return 0

def normalize_contract_length(contract_str: str) -> int:
    """Normalize contract length to months"""
    if not contract_str:
        return 0
    
    contract_str = str(contract_str).lower().replace(' ', '')
    
    # Handle months
    if 'måned' in contract_str or 'mdr' in contract_str:
        try:
            import re
            numbers = re.findall(r'\d+', contract_str)
            if numbers:
                return int(numbers[0])
        except:
            pass
    
    # Handle years
    if 'år' in contract_str or 'year' in contract_str:
        try:
            import re
            numbers = re.findall(r'\d+', contract_str)
            if numbers:
                return int(numbers[0]) * 12
        except:
            pass
    
    # Try to extract number
    try:
        import re
        numbers = re.findall(r'\d+', contract_str)
        if numbers:
            return int(numbers[0])
    except:
        pass
    
    return 0

def scrape_all_providers() -> List[Dict[str, Any]]:
    """Scrape all enabled providers"""
    all_plans = []
    
    for provider in PROVIDERS:
        if not provider['enabled']:
            logger.info(f"Skipping {provider['name']} (disabled)")
            continue
        
        logger.info(f"Scraping {provider['name']}...")
        
        try:
            plans = provider['scraper']()
            
            # Normalize and validate data
            normalized_plans = []
            for plan in plans:
                normalized_plan = {
                    'udbyder': plan.get('udbyder', provider['name']),
                    'hastighed_mbit': normalize_speed(plan.get('hastighed_mbit', '')),
                    'pris_mdr': normalize_price(plan.get('pris_mdr', '')),
                    'bindingstid_mdr': normalize_contract_length(plan.get('bindingstid_mdr', '')),
                    'kampagne': plan.get('kampagne', ''),
                    'plan_navn': plan.get('plan_navn', ''),
                    'beskrivelse': plan.get('beskrivelse', ''),
                    'features': plan.get('features', []),
                    'rating': plan.get('rating', 0)
                }
                
                # Validate required fields
                if normalized_plan['hastighed_mbit'] > 0 and normalized_plan['pris_mdr'] > 0:
                    normalized_plans.append(normalized_plan)
                else:
                    logger.warning(f"Invalid plan data for {provider['name']}: {plan}")
            
            all_plans.extend(normalized_plans)
            logger.info(f"Scraped {len(normalized_plans)} plans from {provider['name']}")
            
        except Exception as e:
            logger.error(f"Error scraping {provider['name']}: {str(e)}")
            continue
    
    return all_plans

def save_to_json(data: List[Dict[str, Any]], output_path: str):
    """Save data to JSON file with metadata"""
    output_data = {
        'last_updated': datetime.now().isoformat(),
        'total_plans': len(data),
        'providers': list(set([plan['udbyder'] for plan in data])),
        'plans': data
    }
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    logger.info(f"Saved {len(data)} plans to {output_path}")

def main():
    """Main scraping function"""
    logger.info("Starting fiber internet scraper...")
    
    # Scrape all providers
    all_plans = scrape_all_providers()
    
    # Save to JSON
    output_path = 'data/fiber.json'
    save_to_json(all_plans, output_path)
    
    # Also save to scraper data directory
    scraper_output_path = 'scraper/data/fiber.json'
    save_to_json(all_plans, scraper_output_path)
    
    logger.info(f"Scraping completed. Total plans: {len(all_plans)}")
    
    # Print summary
    provider_counts = {}
    for plan in all_plans:
        provider = plan['udbyder']
        provider_counts[provider] = provider_counts.get(provider, 0) + 1
    
    logger.info("Provider summary:")
    for provider, count in provider_counts.items():
        logger.info(f"  {provider}: {count} plans")

if __name__ == "__main__":
    main()
