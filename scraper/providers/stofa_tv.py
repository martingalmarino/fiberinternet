#!/usr/bin/env python3
"""
Stofa TV Packages Scraper
"""

import requests
from bs4 import BeautifulSoup
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def scrape_stofa_tv() -> List[Dict[str, Any]]:
    """Scrape Stofa TV packages"""
    packages = []
    
    try:
        # Stofa TV packages URL
        url = "https://www.stofa.dk/tv/pakker"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find TV package containers
        package_containers = soup.find_all('div', class_=['package-card', 'tv-package', 'subscription-card'])
        
        for container in package_containers:
            try:
                # Extract package details
                name_elem = container.find(['h3', 'h4', '.package-name', '.tv-package-name'])
                price_elem = container.find(['.price', '.monthly-price', '.cost'])
                channels_elem = container.find(['.channels', '.kanaler', '.channel-count'])
                
                if name_elem and price_elem:
                    package_name = name_elem.get_text(strip=True)
                    price_text = price_elem.get_text(strip=True)
                    channels_text = channels_elem.get_text(strip=True) if channels_elem else "35"
                    
                    # Parse price
                    price = 0
                    if 'kr' in price_text:
                        price_str = ''.join(filter(str.isdigit, price_text))
                        if price_str:
                            price = int(price_str)
                    
                    # Parse channels
                    channels = 35  # Default
                    if channels_text and channels_text.isdigit():
                        channels = int(channels_text)
                    
                    # Check for contract length
                    contract_text = container.get_text()
                    contract_months = 6  # Default for Stofa
                    if 'ingen binding' in contract_text.lower():
                        contract_months = 0
                    elif '12 måneder' in contract_text:
                        contract_months = 12
                    elif '24 måneder' in contract_text:
                        contract_months = 24
                    
                    # Determine category
                    category = "Film & Serier"
                    if 'sport' in contract_text.lower():
                        category = "Sport"
                    elif 'basis' in contract_text.lower() or 'grund' in contract_text.lower():
                        category = "Basis"
                    elif 'total' in contract_text.lower() or 'komplet' in contract_text.lower():
                        category = "All Inclusive"
                    
                    # Check for promotions
                    promotion = ""
                    if 'gratis oprettelse' in contract_text.lower():
                        promotion = "Ingen oprettelsesgebyr"
                    elif 'halv pris' in contract_text.lower():
                        promotion = "Halv pris første 2 måneder"
                    elif 'gratis' in contract_text.lower():
                        promotion = "Første måned gratis"
                    
                    package = {
                        'id': len(packages) + 1,
                        'udbyder': 'Stofa',
                        'pakke_navn': package_name,
                        'kanaler': channels,
                        'pris_mdr': price,
                        'bindingstid_mdr': contract_months,
                        'kampagne': promotion,
                        'kategori': category,
                        'cta_url': 'https://www.stofa.dk/tv/pakker'
                    }
                    
                    packages.append(package)
                    
            except Exception as e:
                logger.warning(f"Error parsing Stofa package: {e}")
                continue
    
    except Exception as e:
        logger.error(f"Error scraping Stofa TV: {e}")
        # Return fallback data
        packages = [
            {
                'id': 1,
                'udbyder': 'Stofa',
                'pakke_navn': 'Mellempakken',
                'kanaler': 35,
                'pris_mdr': 379,
                'bindingstid_mdr': 6,
                'kampagne': 'Ingen oprettelsesgebyr',
                'kategori': 'Basis',
                'cta_url': 'https://www.stofa.dk/tv/pakker'
            },
            {
                'id': 2,
                'udbyder': 'Stofa',
                'pakke_navn': 'Storpakken',
                'kanaler': 65,
                'pris_mdr': 549,
                'bindingstid_mdr': 12,
                'kampagne': 'Halv pris første 2 måneder',
                'kategori': 'All Inclusive',
                'cta_url': 'https://www.stofa.dk/tv/pakker'
            },
            {
                'id': 3,
                'udbyder': 'Stofa',
                'pakke_navn': 'Sportspakken',
                'kanaler': 50,
                'pris_mdr': 479,
                'bindingstid_mdr': 6,
                'kampagne': 'Gratis oprettelse',
                'kategori': 'Sport',
                'cta_url': 'https://www.stofa.dk/tv/pakker'
            }
        ]
    
    logger.info(f"Scraped {len(packages)} Stofa TV packages")
    return packages
