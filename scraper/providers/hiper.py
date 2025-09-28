"""
Hiper.dk scraper
"""

import requests
from bs4 import BeautifulSoup
import logging
import time
import re

logger = logging.getLogger(__name__)

def scrape_hiper():
    """Scrape fiber internet plans from Hiper.dk"""
    plans = []
    
    try:
        # Hiper fiber internet page
        url = "https://www.hiper.dk/internet/fiber-internet"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for plan cards or pricing tables
        plan_cards = soup.find_all(['div', 'section'], class_=re.compile(r'plan|package|price|card', re.I))
        
        for card in plan_cards:
            try:
                # Extract plan name
                plan_name = ""
                name_elem = card.find(['h2', 'h3', 'h4', 'span'], class_=re.compile(r'title|name|plan', re.I))
                if name_elem:
                    plan_name = name_elem.get_text(strip=True)
                
                # Extract speed
                speed = 0
                speed_elem = card.find(text=re.compile(r'\d+\s*(mbit|mb|gb|gbit)', re.I))
                if speed_elem:
                    speed_text = speed_elem.strip()
                    speed = extract_speed(speed_text)
                
                # Extract price
                price = 0
                price_elem = card.find(text=re.compile(r'\d+\s*(kr|dkk)', re.I))
                if price_elem:
                    price_text = price_elem.strip()
                    price = extract_price(price_text)
                
                # Extract contract length
                contract = 0
                contract_elem = card.find(text=re.compile(r'\d+\s*(måned|mdr|år)', re.I))
                if contract_elem:
                    contract_text = contract_elem.strip()
                    contract = extract_contract_length(contract_text)
                
                # Extract promotion
                promotion = ""
                promo_elem = card.find(text=re.compile(r'(gratis|rabat|tilbud|kampagne)', re.I))
                if promo_elem:
                    promotion = promo_elem.strip()
                
                if speed > 0 and price > 0:
                    plans.append({
                        'udbyder': 'Hiper',
                        'hastighed_mbit': speed,
                        'pris_mdr': price,
                        'bindingstid_mdr': contract,
                        'kampagne': promotion,
                        'plan_navn': plan_name,
                        'beskrivelse': f'Hiper Fiber {speed} Mbit/s',
                        'features': ['Gratis installation', '24/7 support'],
                        'rating': 4.0
                    })
                    
            except Exception as e:
                logger.warning(f"Error parsing Hiper plan card: {e}")
                continue
        
        # If no plans found with the above method, try alternative selectors
        if not plans:
            # Try to find pricing tables
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')[1:]  # Skip header
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 3:
                        try:
                            # Assume first cell is speed, second is price, third is contract
                            speed_text = cells[0].get_text(strip=True)
                            price_text = cells[1].get_text(strip=True)
                            contract_text = cells[2].get_text(strip=True) if len(cells) > 2 else ""
                            
                            speed = extract_speed(speed_text)
                            price = extract_price(price_text)
                            contract = extract_contract_length(contract_text)
                            
                            if speed > 0 and price > 0:
                                plans.append({
                                    'udbyder': 'Hiper',
                                    'hastighed_mbit': speed,
                                    'pris_mdr': price,
                                    'bindingstid_mdr': contract,
                                    'kampagne': '',
                                    'plan_navn': f'Hiper Fiber {speed}',
                                    'beskrivelse': f'Hiper Fiber {speed} Mbit/s',
                                    'features': ['Gratis installation'],
                                    'rating': 4.0
                                })
                        except Exception as e:
                            logger.warning(f"Error parsing Hiper table row: {e}")
                            continue
        
        logger.info(f"Scraped {len(plans)} plans from Hiper")
        
    except Exception as e:
        logger.error(f"Error scraping Hiper: {e}")
    
    return plans

def extract_speed(text):
    """Extract speed from text"""
    if not text:
        return 0
    
    # Look for Gbit/s
    gbit_match = re.search(r'(\d+)\s*(gbit|gb)', text.lower())
    if gbit_match:
        return int(gbit_match.group(1)) * 1000
    
    # Look for Mbit/s
    mbit_match = re.search(r'(\d+)\s*(mbit|mb)', text.lower())
    if mbit_match:
        return int(mbit_match.group(1))
    
    return 0

def extract_price(text):
    """Extract price from text"""
    if not text:
        return 0
    
    price_match = re.search(r'(\d+)', text.replace(' ', '').replace(',', '.'))
    if price_match:
        return int(price_match.group(1))
    
    return 0

def extract_contract_length(text):
    """Extract contract length from text"""
    if not text:
        return 0
    
    # Look for months
    month_match = re.search(r'(\d+)\s*(måned|mdr)', text.lower())
    if month_match:
        return int(month_match.group(1))
    
    # Look for years
    year_match = re.search(r'(\d+)\s*år', text.lower())
    if year_match:
        return int(year_match.group(1)) * 12
    
    return 0
