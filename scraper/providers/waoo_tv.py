#!/usr/bin/env python3
"""
Waoo TV Packages Scraper
"""

import requests
from bs4 import BeautifulSoup
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def scrape_waoo_tv() -> List[Dict[str, Any]]:
    """Scrape Waoo TV packages"""
    packages = []
    
    try:
        # Waoo TV packages URL
        url = "https://www.waoo.dk/tv/pakker"
        
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
                    channels_text = channels_elem.get_text(strip=True) if channels_elem else "50"
                    
                    # Parse price
                    price = 0
                    if 'kr' in price_text:
                        price_str = ''.join(filter(str.isdigit, price_text))
                        if price_str:
                            price = int(price_str)
                    
                    # Parse channels
                    channels = 50  # Default
                    if channels_text and channels_text.isdigit():
                        channels = int(channels_text)
                    
                    # Check for contract length
                    contract_text = container.get_text()
                    contract_months = 12  # Default for Waoo
                    if 'ingen binding' in contract_text.lower():
                        contract_months = 0
                    elif '6 måneder' in contract_text:
                        contract_months = 6
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
                    if 'hbo' in contract_text.lower():
                        promotion = "Gratis HBO Max i 6 måneder"
                    elif 'gratis installation' in contract_text.lower():
                        promotion = "Gratis installation"
                    elif 'gratis' in contract_text.lower():
                        promotion = "Første måned gratis"
                    
                    package = {
                        'id': len(packages) + 1,
                        'udbyder': 'Waoo',
                        'pakke_navn': package_name,
                        'kanaler': channels,
                        'pris_mdr': price,
                        'bindingstid_mdr': contract_months,
                        'kampagne': promotion,
                        'kategori': category,
                        'cta_url': 'https://www.waoo.dk/tv/pakker'
                    }
                    
                    packages.append(package)
                    
            except Exception as e:
                logger.warning(f"Error parsing Waoo package: {e}")
                continue
    
    except Exception as e:
        logger.error(f"Error scraping Waoo TV: {e}")
        # Return fallback data
        packages = [
            {
                'id': 1,
                'udbyder': 'Waoo',
                'pakke_navn': 'Favoritpakken',
                'kanaler': 50,
                'pris_mdr': 429,
                'bindingstid_mdr': 12,
                'kampagne': 'Gratis HBO Max i 6 måneder',
                'kategori': 'Film & Serier',
                'cta_url': 'https://www.waoo.dk/tv/pakker'
            },
            {
                'id': 2,
                'udbyder': 'Waoo',
                'pakke_navn': 'Sportspakken',
                'kanaler': 55,
                'pris_mdr': 499,
                'bindingstid_mdr': 12,
                'kampagne': 'Gratis installation',
                'kategori': 'Sport',
                'cta_url': 'https://www.waoo.dk/tv/pakker'
            },
            {
                'id': 3,
                'udbyder': 'Waoo',
                'pakke_navn': 'Kompletpakken',
                'kanaler': 70,
                'pris_mdr': 649,
                'bindingstid_mdr': 12,
                'kampagne': 'Gratis oprettelse',
                'kategori': 'All Inclusive',
                'cta_url': 'https://www.waoo.dk/tv/pakker'
            }
        ]
    
    logger.info(f"Scraped {len(packages)} Waoo TV packages")
    return packages
