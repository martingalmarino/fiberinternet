"""Ewii Fiber scraper"""
import requests
from bs4 import BeautifulSoup
import logging
import re

logger = logging.getLogger(__name__)

def scrape_ewii_fiber():
    plans = []
    try:
        url = "https://www.ewii.dk/privat/internet/fiber"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for plan sections
        plan_sections = soup.find_all(['div', 'section'], class_=re.compile(r'plan|package|price|card|product|offer', re.I))
        
        for section in plan_sections:
            try:
                speed = extract_speed(section.get_text())
                price = extract_price(section.get_text())
                if speed > 0 and price > 0:
                    plans.append({
                        'udbyder': 'Ewii Fiber',
                        'hastighed_mbit': speed,
                        'pris_mdr': price,
                        'bindingstid_mdr': 12,
                        'kampagne': 'Gratis installation',
                        'plan_navn': f'Ewii Fiber {speed}',
                        'beskrivelse': f'Ewii Fiber {speed} Mbit/s',
                        'features': ['Gratis installation', '24/7 support', 'Lokalt selskab'],
                        'rating': 4.3
                    })
            except Exception as e:
                logger.warning(f"Error parsing Ewii Fiber plan: {e}")
                continue
        
        # Alternative approach: look for specific Ewii patterns
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
                                    'udbyder': 'Ewii Fiber',
                                    'hastighed_mbit': speed,
                                    'pris_mdr': price,
                                    'bindingstid_mdr': 12,
                                    'kampagne': '',
                                    'plan_navn': f'Ewii Fiber {speed}',
                                    'beskrivelse': f'Ewii Fiber {speed} Mbit/s',
                                    'features': ['Gratis installation'],
                                    'rating': 4.3
                                })
                except Exception as e:
                    logger.warning(f"Error parsing Ewii Fiber plan text: {e}")
                    continue
        
        logger.info(f"Scraped {len(plans)} plans from Ewii Fiber")
        
    except Exception as e:
        logger.error(f"Error scraping Ewii Fiber: {e}")
    
    return plans

def extract_speed(text):
    if not text: return 0
    gbit_match = re.search(r'(\d+)\s*(gbit|gb)', text.lower())
    if gbit_match: return int(gbit_match.group(1)) * 1000
    mbit_match = re.search(r'(\d+)\s*(mbit|mb)', text.lower())
    if mbit_match: return int(mbit_match.group(1))
    return 0

def extract_price(text):
    if not text: return 0
    price_match = re.search(r'(\d+)', text.replace(' ', '').replace(',', '.'))
    if price_match: return int(price_match.group(1))
    return 0

def extract_contract_length(text):
    if not text: return 0
    month_match = re.search(r'(\d+)\s*(måned|mdr)', text.lower())
    if month_match: return int(month_match.group(1))
    year_match = re.search(r'(\d+)\s*år', text.lower())
    if year_match: return int(year_match.group(1)) * 12
    return 0
