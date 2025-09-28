"""Energi Fyn scraper"""
import requests
from bs4 import BeautifulSoup
import logging
import re

logger = logging.getLogger(__name__)

def scrape_energi_fyn():
    plans = []
    try:
        url = "https://www.energi-fyn.dk/internet/fiber"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        plan_sections = soup.find_all(['div', 'section'], class_=re.compile(r'plan|package|price|card', re.I))
        for section in plan_sections:
            try:
                speed = extract_speed(section.get_text())
                price = extract_price(section.get_text())
                if speed > 0 and price > 0:
                    plans.append({
                        'udbyder': 'Energi Fyn',
                        'hastighed_mbit': speed,
                        'pris_mdr': price,
                        'bindingstid_mdr': 12,
                        'kampagne': 'Gratis installation',
                        'plan_navn': f'Energi Fyn Fiber {speed}',
                        'beskrivelse': f'Energi Fyn Fiber {speed} Mbit/s',
                        'features': ['Gratis installation', 'Lokalt selskab'],
                        'rating': 4.1
                    })
            except Exception as e:
                logger.warning(f"Error parsing Energi Fyn plan: {e}")
                continue
        
        logger.info(f"Scraped {len(plans)} plans from Energi Fyn")
    except Exception as e:
        logger.error(f"Error scraping Energi Fyn: {e}")
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
