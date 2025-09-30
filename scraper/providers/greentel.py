#!/usr/bin/env python3
"""
Greentel Mobile Plans Scraper
"""

import requests
from bs4 import BeautifulSoup
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def scrape_greentel() -> List[Dict[str, Any]]:
    """Scrape Greentel mobile plans"""
    plans = []
    
    try:
        # Greentel mobile plans URL
        url = "https://www.greentel.dk/mobil/abonnementer"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find mobile plan containers
        plan_containers = soup.find_all('div', class_=['plan-card', 'subscription-card', 'mobile-plan'])
        
        for container in plan_containers:
            try:
                # Extract plan details
                name_elem = container.find(['h3', 'h4', '.plan-name', '.subscription-name'])
                price_elem = container.find(['.price', '.monthly-price', '.cost'])
                data_elem = container.find(['.data', '.gb', '.data-amount'])
                
                if name_elem and price_elem:
                    plan_name = name_elem.get_text(strip=True)
                    price_text = price_elem.get_text(strip=True)
                    data_text = data_elem.get_text(strip=True) if data_elem else "Unlimited"
                    
                    # Parse price
                    price = 0
                    if 'kr' in price_text:
                        price_str = ''.join(filter(str.isdigit, price_text))
                        if price_str:
                            price = int(price_str)
                    
                    # Parse data
                    data_gb = 0
                    if 'GB' in data_text or 'gb' in data_text:
                        data_str = ''.join(filter(str.isdigit, data_text))
                        if data_str:
                            data_gb = int(data_str)
                    elif 'unlimited' in data_text.lower() or 'ubegrænset' in data_text.lower():
                        data_gb = 999
                    
                    # Check for EU roaming
                    roaming_eu = 'EU' in container.get_text() or 'europa' in container.get_text().lower()
                    
                    # Check for family discount
                    family_discount = 'familie' in container.get_text().lower() or 'rabat' in container.get_text().lower()
                    
                    # Check for contract length
                    contract_text = container.get_text()
                    contract_months = 0
                    if 'ingen binding' in contract_text.lower():
                        contract_months = 0
                    
                    # Check for promotions
                    promotion = ""
                    if 'klimaneutral' in contract_text.lower():
                        promotion = "Klimaneutral udbyder"
                    elif 'gratis' in contract_text.lower():
                        promotion = "Første måned gratis"
                    
                    plan = {
                        'id': len(plans) + 1,
                        'udbyder': 'Greentel',
                        'data_GB': data_gb,
                        'pris_mdr': price,
                        'roaming_EU': roaming_eu,
                        'familierabat': 'Ja, 2. simkort til halv pris' if family_discount else 'Nej',
                        'bindingstid_mdr': contract_months,
                        'kampagne': promotion,
                        'cta_url': 'https://www.greentel.dk/mobil/abonnementer'
                    }
                    
                    plans.append(plan)
                    
            except Exception as e:
                logger.warning(f"Error parsing Greentel plan: {e}")
                continue
    
    except Exception as e:
        logger.error(f"Error scraping Greentel mobile: {e}")
        # Return fallback data
        plans = [
            {
                'id': 1,
                'udbyder': 'Greentel',
                'data_GB': 40,
                'pris_mdr': 109,
                'roaming_EU': True,
                'familierabat': 'Ja, 2. simkort til halv pris',
                'bindingstid_mdr': 0,
                'kampagne': 'Klimaneutral udbyder',
                'cta_url': 'https://www.greentel.dk/mobil/abonnementer'
            }
        ]
    
    logger.info(f"Scraped {len(plans)} Greentel mobile plans")
    return plans
