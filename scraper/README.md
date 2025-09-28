# Fiber Internet Scraper for Denmark

A comprehensive web scraper that collects fiber internet plans from major Danish providers to keep the comparison website data fresh and up-to-date.

## 🚀 Features

- **Multi-provider support**: Scrapes from 13+ major Danish fiber internet providers
- **Robust error handling**: Gracefully handles provider failures and missing data
- **Data normalization**: Standardizes speed, price, and contract length formats
- **Comprehensive logging**: Detailed logs for debugging and monitoring
- **Scheduled execution**: Ready for automated weekly/monthly runs
- **JSON output**: Clean, structured data for frontend consumption

## 📦 Installation

### Prerequisites
- Python 3.10+
- pip package manager

### Setup
```bash
# Clone the repository
cd scraper

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers (for dynamic content)
playwright install
```

## 🔧 Usage

### Manual Execution
```bash
# Run the scraper
python scrape_fiber.py

# Check logs
tail -f scraper.log
```

### Scheduled Execution

#### Using Cron (Linux/macOS)
```bash
# Edit crontab
crontab -e

# Add weekly execution (every Monday at 4 AM)
0 4 * * 1 cd /path/to/scraper && python scrape_fiber.py
```

#### Using GitHub Actions
Create `.github/workflows/scraper.yml`:
```yaml
name: Fiber Internet Scraper
on:
  schedule:
    - cron: '0 4 * * 1'  # Every Monday at 4 AM
  workflow_dispatch:  # Manual trigger

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          cd scraper
          pip install -r requirements.txt
          playwright install
      - name: Run scraper
        run: |
          cd scraper
          python scrape_fiber.py
      - name: Commit changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add data/fiber.json
          git commit -m "Update fiber data" || exit 0
          git push
```

## 📊 Data Structure

The scraper outputs a JSON file with the following structure:

```json
{
  "last_updated": "2024-01-15T10:30:00",
  "total_plans": 45,
  "providers": ["Hiper", "YouSee", "Telia", "Stofa", "Telenor"],
  "plans": [
    {
      "udbyder": "Hiper",
      "hastighed_mbit": 1000,
      "pris_mdr": 299,
      "bindingstid_mdr": 6,
      "kampagne": "3 mdr til 199 DKK",
      "plan_navn": "Hiper Fiber 1000",
      "beskrivelse": "Hiper Fiber 1000 Mbit/s",
      "features": ["Gratis installation", "24/7 support"],
      "rating": 4.0
    }
  ]
}
```

## 🏢 Supported Providers

| Provider | Status | URL |
|----------|--------|-----|
| Hiper | ✅ Active | https://www.hiper.dk |
| YouSee | ✅ Active | https://www.yousee.dk |
| Telia | ✅ Active | https://www.telia.dk |
| Stofa | ✅ Active | https://www.stofa.dk |
| Telenor | ✅ Active | https://www.telenor.dk |
| Waoo | ✅ Active | https://www.waoo.dk |
| Kviknet | ✅ Active | https://www.kviknet.dk |
| CBB | ✅ Active | https://www.cbb.dk |
| Altibox | ⚠️ Disabled | https://www.altibox.dk |
| Fibia | ⚠️ Disabled | https://www.fibia.dk |
| Norlys | ✅ Active | https://www.norlys.dk |
| Energi Fyn | ✅ Active | https://www.energi-fyn.dk |
| SEAS-NVE | ✅ Active | https://www.seas-nve.dk |

## 🔧 Configuration

### Enabling/Disabling Providers
Edit `scrape_fiber.py` and modify the `PROVIDERS` list:

```python
PROVIDERS = [
    {
        'name': 'Provider Name',
        'scraper': scrape_provider,
        'enabled': True  # Set to False to disable
    }
]
```

### Adding New Providers
1. Create a new file in `providers/provider_name.py`
2. Implement the scraper function following the pattern:
   ```python
   def scrape_provider_name():
       plans = []
       # Scraping logic here
       return plans
   ```
3. Add the provider to the `PROVIDERS` list in `scrape_fiber.py`

## 📝 Logging

The scraper creates detailed logs in `scraper.log`:
- Provider scraping progress
- Data extraction details
- Error messages and warnings
- Summary statistics

## 🚨 Error Handling

The scraper includes comprehensive error handling:
- **Network errors**: Retries and graceful failures
- **Parsing errors**: Logs warnings and continues
- **Data validation**: Ensures required fields are present
- **Provider failures**: Skips failed providers and continues

## 📈 Monitoring

### Key Metrics
- Total plans scraped
- Provider success rate
- Data freshness (last_updated timestamp)
- Error frequency

### Health Checks
```bash
# Check if scraper ran recently
ls -la scraper/data/fiber.json

# Check for errors in logs
grep "ERROR" scraper/scraper.log | tail -10

# Validate JSON output
python -c "import json; json.load(open('scraper/data/fiber.json'))"
```

## 🔄 Integration

The scraper integrates seamlessly with the frontend:
1. Updates `data/fiber.json` in the main project
2. Frontend automatically loads fresh data
3. No downtime during updates
4. Maintains data consistency

## 🛠️ Troubleshooting

### Common Issues

**Provider returns no data**
- Check if the provider's website structure changed
- Verify the URL is still valid
- Check for anti-bot measures

**Parsing errors**
- Review the provider's HTML structure
- Update CSS selectors in the provider module
- Test with a sample HTML snippet

**Network timeouts**
- Increase timeout values in provider modules
- Check network connectivity
- Consider using proxy servers

### Debug Mode
Enable detailed logging:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 📞 Support

For issues or questions:
1. Check the logs in `scraper.log`
2. Review provider-specific error messages
3. Test individual provider modules
4. Verify network connectivity

## 📄 License

This scraper is part of the Telecom & Home Digital DK project and follows the same license terms.
