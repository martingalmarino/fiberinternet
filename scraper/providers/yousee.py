"""
YouSee.dk scraper
"""

import requests
from bs4 import BeautifulSoup
import logging
import time
import re

logger = logging.getLogger(__name__)

def scrape_yousee():
    """Scrape fiber internet plans from YouSee.dk"""
    plans = []
    
    try:
        # YouSee fiber internet page
        url = "https://www.yousee.dk/privat/internet/fiber"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for plan cards or pricing sections
        plan_sections = soup.find_all(['div', 'section'], class_=re.compile(r'plan|package|price|card|product', re.I))
        
        for section in plan_sections:
            try:
                # Extract plan name
                plan_name = ""
                name_elem = section.find(['h2', 'h3', 'h4', 'span'], class_=re.compile(r'title|name|plan', re.I))
                if name_elem:
                    plan_name = name_elem.get_text(strip=True)
                
                # Extract speed
                speed = 0
                speed_elem = section.find(text=re.compile(r'\d+\s*(mbit|mb|gb|gbit)', re.I))
                if speed_elem:
                    speed_text = speed_elem.strip()
                    speed = extract_speed(speed_text)
                
                # Extract price
                price = 0
                price_elem = section.find(text=re.compile(r'\d+\s*(kr|dkk)', re.I))
                if price_elem:
                    price_text = price_elem.strip()
                    price = extract_price(price_text)
                
                # Extract contract length
                contract = 12  # Default for YouSee
                contract_elem = section.find(text=re.compile(r'\d+\s*(måned|mdr|år)', re.I))
                if contract_elem:
                    contract_text = contract_elem.strip()
                    contract = extract_contract_length(contract_text)
                
                # Extract promotion
                promotion = ""
                promo_elem = section.find(text=re.compile(r'(gratis|rabat|tilbud|kampagne)', re.I))
                if promo_elem:
                    promotion = promo_elem.strip()
                
                if speed > 0 and price > 0:
                    plans.append({
                        'udbyder': 'YouSee',
                        'hastighed_mbit': speed,
                        'pris_mdr': price,
                        'bindingstid_mdr': contract,
                        'kampagne': promotion,
                        'plan_navn': plan_name or f'YouSee Fiber {speed}',
                        'beskrivelse': f'YouSee Fiber {speed} Mbit/s',
                        'features': ['Gratis installation', 'YouSee TV tilgængelig'],
                        'rating': 4.2
                    })
                    
            except Exception as e:
                logger.warning(f"Error parsing YouSee plan section: {e}")
                continue
        
        # Alternative approach: look for specific YouSee plan patterns
        if not plans:
            # Try to find fiber plans by looking for specific text patterns
            fiber_plans = soup.find_all(text=re.compile(r'fiber.*\d+\s*(mbit|mb)', re.I))
            for plan_text in fiber_plans:
                try:
                    parent = plan_text.parent
                    if parent:
                        # Look for price in the same container
                        price_elem = parent.find(text=re.compile(r'\d+\s*(kr|dkk)', re.I))
                        if price_elem:
                            speed = extract_speed(plan_text)
                            price = extract_price(price_elem.strip())
                            
                            if speed > 0 and price > 0:
                                plans.append({
                                    'udbyder': 'YouSee',
                                    'hastighed_mbit': speed,
                                    'pris_mdr': price,
                                    'bindingstid_mdr': 12,
                                    'kampagne': '',
                                    'plan_navn': f'YouSee Fiber {speed}',
                                    'beskrivelse': f'YouSee Fiber {speed} Mbit/s',
                                    'features': ['Gratis installation'],
                                    'rating': 4.2
                                })
                except Exception as e:
                    logger.warning(f"Error parsing YouSee plan text: {e}")
                    continue
        
        logger.info(f"Scraped {len(plans)} plans from YouSee")
        
    except Exception as e:
        logger.error(f"Error scraping YouSee: {e}")
    
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
