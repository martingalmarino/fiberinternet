# Telecom & Home Digital DK

A modern comparison platform for telecom services in Denmark, starting with fiber internet comparison.

## 🚀 Quick Start

### Prerequisites
- A modern web browser
- A local web server (for development)

### Installation

1. **Clone or download** the project files
2. **Start a local server** (choose one method):

#### Option 1: Python (Recommended)
```bash
# Python 3
cd "Telecom & Home Digital DK"
python -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000
```

#### Option 2: Node.js (if you have it installed)
```bash
cd "Telecom & Home Digital DK"
npx serve .
```

#### Option 3: PHP
```bash
cd "Telecom & Home Digital DK"
php -S localhost:8000
```

3. **Open your browser** and navigate to:
   - `http://localhost:8000`

## 📁 Project Structure

```
Telecom & Home Digital DK/
├── index.html          # Main HTML file with hero section and comparison table
├── style.css           # CSS styles with responsive design and Danish color scheme
├── app.js              # JavaScript for data loading, sorting, and filtering
├── data/
│   └── fiber.json      # Sample fiber internet provider data
└── README.md           # This file
```

## 🎨 Design Features

### Color Palette
- **Hero Background**: Dark blue-green gradient (`#0B3C49` → `#1E3A8A`)
- **Primary CTA**: Emerald green (`#00A86B`)
- **Background**: Light gray (`#F8FAFC`)
- **Cards/Tables**: White with soft shadows

### Responsive Design
- Mobile-first approach
- Breakpoints: 768px, 480px
- Touch-friendly buttons and interactions
- Accessible keyboard navigation

## 🔧 Features

### Current MVP Features
- ✅ Hero section with clear value proposition
- ✅ Fiber internet comparison table
- ✅ Sortable columns (Provider, Speed, Price, Contract)
- ✅ Speed filtering (100+, 200+, 500+, 1000+ Mbit/s)
- ✅ Responsive design for mobile and desktop
- ✅ Loading states and error handling
- ✅ Danish language interface

### Sample Data
The `data/fiber.json` file includes 10 sample providers:
- TDC, Telenor, Telia, Stofa, Hiper
- Waoo, Fiberby, Kviknet, Fullrate, CBB

Each provider includes:
- Provider name and plan details
- Speed, price, and contract length
- Promotional offers
- Features and ratings

## 🛠️ Development

### Adding New Providers
Edit `data/fiber.json` to add new providers:

```json
{
  "id": 11,
  "provider": "New Provider",
  "logo": "new-logo.png",
  "plan": "New Plan 100",
  "speed": 100,
  "price": 299,
  "contractLength": 12,
  "promotion": "Special offer",
  "features": ["Feature 1", "Feature 2"],
  "rating": 4.0,
  "description": "Provider description"
}
```

### Customizing Styles
Main style variables in `style.css`:
- Colors: Search for `#00A86B`, `#0B3C49`, `#1E3A8A`
- Typography: Font family and sizes in the base styles
- Layout: Container max-width, spacing, grid systems

### JavaScript Functionality
Key functions in `app.js`:
- `TelecomComparison` class handles all functionality
- `loadComparisonData()` fetches JSON data
- `handleSort()` manages table sorting
- `handleFilter()` applies speed filters
- `renderTable()` updates the display

## 📈 Future Enhancements

### Phase 2: Additional Services
- Mobile plans comparison (`mobil.json`)
- TV bundle packages (`pakker.json`)
- Combined service bundles

### Phase 3: Interactive Tools
- Speed test integration
- Family bundle calculator
- Postcode-based coverage checker

### Phase 4: Backend Integration
- Python scraper for live data
- REST API for dynamic content
- Database integration
- Automated price updates

## 🚀 Deployment

### Static Hosting Options

#### Vercel
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

#### Netlify
1. Drag and drop the project folder to [netlify.com/drop](https://netlify.com/drop)
2. Or connect your Git repository

#### GitHub Pages
1. Push to GitHub repository
2. Enable Pages in repository settings
3. Select source branch

### Custom Server
Upload all files to your web server's document root.

## 🔍 SEO & Performance

### SEO Features
- Semantic HTML structure
- Meta descriptions and keywords
- Danish language support (`lang="da"`)
- Structured data ready for implementation

### Performance
- Lightweight vanilla JavaScript
- Optimized CSS with minimal dependencies
- Fast loading static assets
- Mobile-optimized images (when added)

## 🐛 Troubleshooting

### Common Issues

**Data not loading:**
- Ensure you're using a local server (not opening file directly)
- Check browser console for CORS errors
- Verify `data/fiber.json` exists and is valid JSON

**Styling issues:**
- Clear browser cache
- Check CSS file path in HTML
- Verify responsive breakpoints

**JavaScript errors:**
- Open browser developer tools
- Check console for error messages
- Ensure all files are properly linked

### Browser Support
- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## 📞 Support

For technical issues or questions about the codebase, please check the browser console for error messages and ensure all files are properly structured.

## 📄 License

This project is proprietary software for Telecom & Home Digital DK.

---

**Built with ❤️ for the Danish market**
