#!/usr/bin/env python3
"""
Test script for the fiber internet scraper
"""

import sys
import os
import json
from datetime import datetime

# Add providers directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'providers'))

def test_provider_scrapers():
    """Test individual provider scrapers"""
    providers = [
        ('hiper', 'Hiper'),
        ('yousee', 'YouSee'),
        ('telia', 'Telia'),
        ('stofa', 'Stofa'),
        ('telenor', 'Telenor'),
        ('waoo', 'Waoo'),
        ('kviknet', 'Kviknet'),
        ('cbb', 'CBB'),
        ('altibox', 'Altibox'),
        ('fibia', 'Fibia'),
        ('norlys', 'Norlys'),
        ('energi_fyn', 'Energi Fyn'),
        ('seas_nve', 'SEAS-NVE'),
        ('fastspeed', 'Fastspeed'),
        ('ewii_fiber', 'Ewii Fiber'),
        ('hiper_pro', 'Hiper Pro')
    ]
    
    results = {}
    
    for module_name, provider_name in providers:
        try:
            module = __import__(module_name)
            scraper_func = getattr(module, f'scrape_{module_name}')
            
            print(f"Testing {provider_name}...")
            plans = scraper_func()
            
            results[provider_name] = {
                'status': 'success',
                'plans_count': len(plans),
                'plans': plans[:2] if plans else []  # Show first 2 plans as sample
            }
            
            print(f"  ✅ {provider_name}: {len(plans)} plans found")
            
        except Exception as e:
            results[provider_name] = {
                'status': 'error',
                'error': str(e),
                'plans_count': 0
            }
            print(f"  ❌ {provider_name}: {str(e)}")
    
    return results

def test_data_validation():
    """Test data validation and normalization"""
    print("\n🔍 Testing data validation...")
    
    # Test speed normalization
    from scrape_fiber import TelecomComparison
    scraper = TelecomComparison()
    
    test_cases = [
        ("100 Mbit/s", 100),
        ("1 Gbit/s", 1000),
        ("500 mb", 500),
        ("2 GB", 2000),
        ("invalid", 0)
    ]
    
    for input_text, expected in test_cases:
        result = scraper.normalize_speed(input_text)
        status = "✅" if result == expected else "❌"
        print(f"  {status} Speed: '{input_text}' -> {result} (expected {expected})")
    
    # Test price normalization
    price_cases = [
        ("299 kr", 299),
        ("399 DKK", 399),
        ("199,50", 199),
        ("invalid", 0)
    ]
    
    for input_text, expected in price_cases:
        result = scraper.normalize_price(input_text)
        status = "✅" if result == expected else "❌"
        print(f"  {status} Price: '{input_text}' -> {result} (expected {expected})")
    
    # Test contract length normalization
    contract_cases = [
        ("12 måneder", 12),
        ("2 år", 24),
        ("6 mdr", 6),
        ("invalid", 0)
    ]
    
    for input_text, expected in contract_cases:
        result = scraper.normalize_contract_length(input_text)
        status = "✅" if result == expected else "❌"
        print(f"  {status} Contract: '{input_text}' -> {result} (expected {expected})")

def test_json_output():
    """Test JSON output format"""
    print("\n📄 Testing JSON output...")
    
    try:
        # Run the main scraper
        from scrape_fiber import main
        main()
        
        # Check if output file exists
        output_file = 'data/fiber.json'
        if os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Validate structure
            required_fields = ['last_updated', 'total_plans', 'providers', 'plans']
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                print(f"  ❌ Missing fields: {missing_fields}")
            else:
                print(f"  ✅ JSON structure valid")
                print(f"  📊 Total plans: {data['total_plans']}")
                print(f"  🏢 Providers: {len(data['providers'])}")
                print(f"  📅 Last updated: {data['last_updated']}")
                
                # Validate plan structure
                if data['plans']:
                    plan = data['plans'][0]
                    plan_fields = ['udbyder', 'hastighed_mbit', 'pris_mdr', 'bindingstid_mdr', 'kampagne']
                    missing_plan_fields = [field for field in plan_fields if field not in plan]
                    
                    if missing_plan_fields:
                        print(f"  ❌ Missing plan fields: {missing_plan_fields}")
                    else:
                        print(f"  ✅ Plan structure valid")
        else:
            print(f"  ❌ Output file not found: {output_file}")
            
    except Exception as e:
        print(f"  ❌ JSON output test failed: {e}")

def main():
    """Run all tests"""
    print("🧪 Fiber Internet Scraper Test Suite")
    print("=" * 50)
    
    # Test individual providers
    print("\n🔍 Testing Provider Scrapers...")
    provider_results = test_provider_scrapers()
    
    # Test data validation
    test_data_validation()
    
    # Test JSON output
    test_json_output()
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 30)
    
    successful_providers = [name for name, result in provider_results.items() if result['status'] == 'success']
    failed_providers = [name for name, result in provider_results.items() if result['status'] == 'error']
    
    print(f"✅ Successful providers: {len(successful_providers)}")
    for provider in successful_providers:
        count = provider_results[provider]['plans_count']
        print(f"   - {provider}: {count} plans")
    
    print(f"❌ Failed providers: {len(failed_providers)}")
    for provider in failed_providers:
        error = provider_results[provider]['error']
        print(f"   - {provider}: {error}")
    
    print(f"\n🎯 Total plans found: {sum(result['plans_count'] for result in provider_results.values())}")
    
    # Save test results
    test_results = {
        'timestamp': datetime.now().isoformat(),
        'provider_results': provider_results,
        'summary': {
            'successful_providers': len(successful_providers),
            'failed_providers': len(failed_providers),
            'total_plans': sum(result['plans_count'] for result in provider_results.values())
        }
    }
    
    with open('test_results.json', 'w', encoding='utf-8') as f:
        json.dump(test_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Test results saved to: test_results.json")

if __name__ == "__main__":
    main()
