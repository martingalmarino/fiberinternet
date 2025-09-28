// Telecom & Home Digital DK - Main Application JavaScript
// Handles data loading, table rendering, sorting, and filtering functionality

class TelecomComparison {
    constructor() {
        this.data = [];
        this.filteredData = [];
        this.sortColumn = 'price';
        this.sortDirection = 'asc';
        this.currentFilter = 'all';
        
        this.init();
    }

    async init() {
        // Initialize the application
        this.setupEventListeners();
        this.setupFAQ();
        this.setupMobileScrollEnhancements();
        await this.loadComparisonData();
    }

    setupEventListeners() {
        // Sort button event listeners
        document.querySelectorAll('.sort-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.handleSort(e.target.dataset.sort);
            });
        });

        // Table header sort event listeners
        document.querySelectorAll('.sortable').forEach(header => {
            header.addEventListener('click', () => {
                this.handleSort(header.dataset.sort);
            });
        });

        // Speed filter event listener
        const speedFilter = document.getElementById('speed-filter');
        if (speedFilter) {
            speedFilter.addEventListener('change', (e) => {
                this.handleFilter(e.target.value);
            });
        }

        // Keyboard navigation for accessibility
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                const focused = document.activeElement;
                if (focused.classList.contains('sort-btn') || focused.classList.contains('sortable')) {
                    e.preventDefault();
                    focused.click();
                }
            }
        });
    }

    setupFAQ() {
        // FAQ functionality
        document.querySelectorAll('.faq-question').forEach(question => {
            question.addEventListener('click', () => {
                this.toggleFAQ(question);
            });
            
            // Keyboard support
            question.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.toggleFAQ(question);
                }
            });
        });
    }

    toggleFAQ(question) {
        const answer = question.nextElementSibling;
        const isExpanded = question.getAttribute('aria-expanded') === 'true';
        
        // Close all other FAQ items
        document.querySelectorAll('.faq-question').forEach(q => {
            if (q !== question) {
                q.setAttribute('aria-expanded', 'false');
                q.nextElementSibling.classList.remove('active');
            }
        });
        
        // Toggle current FAQ item
        if (isExpanded) {
            question.setAttribute('aria-expanded', 'false');
            answer.classList.remove('active');
        } else {
            question.setAttribute('aria-expanded', 'true');
            answer.classList.add('active');
        }
    }

    async loadComparisonData() {
        const loading = document.getElementById('loading');
        const comparisonContainer = document.getElementById('comparison-container');
        const errorState = document.getElementById('error-state');

        try {
            // Show loading state
            if (loading) loading.style.display = 'block';
            if (comparisonContainer) comparisonContainer.style.display = 'none';
            if (errorState) errorState.style.display = 'none';

            // Fetch data from JSON file
            const response = await fetch('./data/fiber.json');
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const rawData = await response.json();
            
            // Handle both array format and object format with metadata
            if (Array.isArray(rawData)) {
                this.data = rawData;
            } else if (rawData.plans) {
                this.data = rawData.plans;
                this.updateLastUpdatedDisplay(rawData.last_updated);
            } else {
                this.data = rawData;
            }
            
            this.filteredData = [...this.data];

            // Render the table
            this.renderTable();
            this.updateSortButtons();

            // Hide loading and show table
            if (loading) loading.style.display = 'none';
            if (comparisonContainer) comparisonContainer.style.display = 'block';

        } catch (error) {
            console.error('Error loading comparison data:', error);
            
            // Show error state
            if (loading) loading.style.display = 'none';
            if (comparisonContainer) comparisonContainer.style.display = 'none';
            if (errorState) errorState.style.display = 'block';
        }
    }

    handleSort(column) {
        // Update sort column and direction
        if (this.sortColumn === column) {
            this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
            this.sortColumn = column;
            this.sortDirection = 'asc';
        }

        // Apply sorting
        this.applySorting();
        this.renderTable();
        this.updateSortButtons();
        this.updateTableHeaders();
    }

    applySorting() {
        this.filteredData.sort((a, b) => {
            let aValue, bValue;

            switch (this.sortColumn) {
                case 'provider':
                    aValue = a.provider.toLowerCase();
                    bValue = b.provider.toLowerCase();
                    break;
                case 'speed':
                    aValue = parseInt(a.speed);
                    bValue = parseInt(b.speed);
                    break;
                case 'price':
                    aValue = parseInt(a.price);
                    bValue = parseInt(b.price);
                    break;
                case 'contract':
                    aValue = parseInt(a.contractLength);
                    bValue = parseInt(b.contractLength);
                    break;
                default:
                    return 0;
            }

            if (aValue < bValue) {
                return this.sortDirection === 'asc' ? -1 : 1;
            }
            if (aValue > bValue) {
                return this.sortDirection === 'asc' ? 1 : -1;
            }
            return 0;
        });
    }

    handleFilter(minSpeed) {
        this.currentFilter = minSpeed;
        
        if (minSpeed === 'all') {
            this.filteredData = [...this.data];
        } else {
            const speedThreshold = parseInt(minSpeed);
            this.filteredData = this.data.filter(item => item.speed >= speedThreshold);
        }

        // Reapply current sorting
        this.applySorting();
        this.renderTable();
    }

    renderTable() {
        const tbody = document.getElementById('table-body');
        const mobileCardsContainer = document.getElementById('mobile-cards-container');
        
        if (!tbody || !mobileCardsContainer) {
            console.error('Missing elements:', { tbody, mobileCardsContainer });
            return;
        }

        // Clear existing rows and cards
        tbody.innerHTML = '';
        mobileCardsContainer.innerHTML = '';

        // Render each provider row and card
        this.filteredData.forEach(provider => {
            const row = this.createTableRow(provider);
            tbody.appendChild(row);
            
            const card = this.createMobileCard(provider);
            mobileCardsContainer.appendChild(card);
        });

        // Update results count
        this.updateResultsCount();
        
        // Initialize calculator after data is loaded
        this.initializeCalculator();
    }

    initializeCalculator() {
        // Initialize calculator dropdowns with loaded data
        this.populateCalculatorDropdowns();
    }

    populateCalculatorDropdowns() {
        console.log('populateCalculatorDropdowns called');
        console.log('Data length:', this.data ? this.data.length : 'No data');
        
        const providerSelect = document.getElementById('calculator-provider');
        const speedSelect = document.getElementById('calculator-speed');
        const contractSelect = document.getElementById('calculator-contract');
        
        console.log('Elements found:', { providerSelect, speedSelect, contractSelect });
        
        if (!providerSelect || !speedSelect || !contractSelect) {
            console.error('Calculator elements not found');
            return;
        }
        
        if (!this.data || this.data.length === 0) {
            console.error('No data available for calculator');
            return;
        }
        
        // Get unique providers
        const providers = [...new Set(this.data.map(item => item.provider))].sort();
        console.log('Unique providers:', providers);
        
        // Clear and populate provider dropdown
        providerSelect.innerHTML = '<option value="">Vælg en udbyder</option>';
        providers.forEach(provider => {
            const option = document.createElement('option');
            option.value = provider;
            option.textContent = provider;
            providerSelect.appendChild(option);
        });
        
        console.log('Provider dropdown populated with', providers.length, 'options');
    }

    createTableRow(provider) {
        const row = document.createElement('tr');
        
        row.innerHTML = `
            <td class="provider-cell">
                <div class="provider-logo">
                    <img src="${this.getProviderLogo(provider.provider)}" 
                         alt="${provider.provider} logo" 
                         class="provider-logo-img"
                         onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                    <div class="provider-logo-fallback" style="display: none;">${provider.provider.charAt(0)}</div>
                </div>
                <div class="provider-info">
                    <h4>${provider.provider}</h4>
                    <p>${this.getCleanPlanName(provider.plan, provider.provider)}</p>
                </div>
            </td>
            <td class="speed-cell">${provider.speed} Mbit/s</td>
            <td class="price-cell">${provider.price} kr./md.</td>
            <td class="contract-cell">${provider.contractLength} måneder</td>
            <td class="promotion-cell">
                ${provider.promotion ? `<span class="promotion-badge" title="${provider.promotion}">${provider.promotion}</span>` : '-'}
            </td>
            <td class="action-cell">
                <button class="action-btn" onclick="handleProviderClick(${provider.id}, '${provider.provider}', '${provider.plan}', ${provider.price})" data-provider="${provider.provider}" data-plan="${provider.plan}" data-price="${provider.price}">
                    Vælg Tilbud
                </button>
            </td>
        `;

        return row;
    }

    createMobileCard(provider) {
        const card = document.createElement('div');
        card.className = 'mobile-card';
        
        card.innerHTML = `
            <div class="mobile-card-header">
                <div class="mobile-card-logo">
                    <img src="${this.getProviderLogo(provider.provider)}" 
                         alt="${provider.provider} logo" 
                         class="mobile-card-logo-img"
                         onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                    <div class="mobile-card-logo-fallback" style="display: none;">${provider.provider.charAt(0)}</div>
                </div>
                <div class="mobile-card-info">
                    <h3>${provider.provider}</h3>
                    <p>${this.getCleanPlanName(provider.plan, provider.provider)}</p>
                </div>
                <div class="mobile-card-price">
                    <p class="price">${provider.price} kr.</p>
                    <p class="period">per måned</p>
                </div>
            </div>
            <div class="mobile-card-body">
                <div class="mobile-card-details">
                    <div class="mobile-card-detail">
                        <span class="mobile-card-detail-label">Hastighed</span>
                        <span class="mobile-card-detail-value">${provider.speed} Mbit/s</span>
                    </div>
                    <div class="mobile-card-detail">
                        <span class="mobile-card-detail-label">Kontrakt</span>
                        <span class="mobile-card-detail-value">${provider.contractLength} måneder</span>
                    </div>
                </div>
                ${provider.promotion ? `
                    <div class="mobile-card-promotion">
                        <p class="promotion-text">🎁 ${provider.promotion}</p>
                    </div>
                ` : ''}
                <button class="mobile-card-action" onclick="handleProviderClick(${provider.id}, '${provider.provider}', '${provider.plan}', ${provider.price})">
                    Vælg Tilbud
                </button>
            </div>
        `;
        
        return card;
    }

    updateSortButtons() {
        // Remove active class from all sort buttons
        document.querySelectorAll('.sort-btn').forEach(btn => {
            btn.classList.remove('active');
        });

        // Add active class to current sort button
        const activeBtn = document.querySelector(`[data-sort="${this.sortColumn}"]`);
        if (activeBtn) {
            activeBtn.classList.add('active');
        }
    }

    updateTableHeaders() {
        // Remove sort indicators from all headers
        document.querySelectorAll('.sortable').forEach(header => {
            header.classList.remove('sort-asc', 'sort-desc');
        });

        // Add sort indicator to current column header
        const activeHeader = document.querySelector(`[data-sort="${this.sortColumn}"]`);
        if (activeHeader) {
            activeHeader.classList.add(`sort-${this.sortDirection}`);
        }
    }

    updateResultsCount() {
        // Update any results count display if needed
        const count = this.filteredData.length;
        console.log(`Showing ${count} results`);
    }

    getCleanPlanName(plan, provider) {
        // Remove redundant provider name from plan name
        let cleanPlan = plan;
        
        // Remove provider name if it appears at the beginning of the plan
        if (plan.toLowerCase().startsWith(provider.toLowerCase())) {
            cleanPlan = plan.substring(provider.length).trim();
        }
        
        // Remove common redundant terms
        cleanPlan = cleanPlan.replace(/^Fiber\s*/i, '');
        
        // If the plan is now empty or very short, use a default
        if (!cleanPlan || cleanPlan.length < 3) {
            cleanPlan = 'Fiber Internet';
        }
        
        return cleanPlan;
    }
    
    getProviderLogo(providerName) {
        // Map of provider names to logo file paths or SVG data URLs
        const logoMap = {
            'TDC': this.createLogoSVG('TDC', '#E60012'),
            'YouSee': this.createLogoSVG('YS', '#FF6B35'),
            'Telenor': this.createLogoSVG('T', '#22B573'),
            'Telia': this.createLogoSVG('T', '#490094'),
            'Stofa': this.createLogoSVG('S', '#1E3A8A'),
            'Hiper': this.createLogoSVG('H', '#00A86B'),
            'Hiper Pro': this.createLogoSVG('H', '#00A86B'),
            'Waoo': this.createLogoSVG('W', '#FF4081'),
            'Kviknet': this.createLogoSVG('K', '#3B82F6'),
            'CBB': this.createLogoSVG('CBB', '#8B5CF6'),
            'Fastspeed': this.createLogoSVG('F', '#F59E0B'),
            'Ewii Fiber': this.createLogoSVG('E', '#10B981'),
            'Norlys': this.createLogoSVG('N', '#EF4444'),
            'Altibox': this.createLogoSVG('A', '#6366F1'),
            'Fiberby': this.createLogoSVG('F', '#84CC16'),
            'Fullrate': this.createLogoSVG('FR', '#F97316'),
            'Energi Fyn': this.createLogoSVG('EF', '#06B6D4'),
            'SEAS-NVE': this.createLogoSVG('SN', '#8B5A2B'),
            'Fibia': this.createLogoSVG('F', '#EC4899')
        };
        
        // Return logo or fallback to initials
        return logoMap[providerName] || this.createLogoSVG(providerName.charAt(0), '#00A86B');
    }
    
    createLogoSVG(text, color) {
        // Create a simple SVG logo with the provider initial and brand color
        const svg = `
            <svg width="44" height="44" viewBox="0 0 44 44" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect width="44" height="44" rx="10" fill="${color}"/>
                <text x="22" y="28" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="white" text-anchor="middle">${text}</text>
            </svg>
        `;
        
        // Convert to data URL
        const encoded = btoa(unescape(encodeURIComponent(svg)));
        return `data:image/svg+xml;base64,${encoded}`;
    }
    
    updateLastUpdatedDisplay(lastUpdated) {
        if (!lastUpdated) return;
        
        // Find or create the last updated display element
        let lastUpdatedElement = document.getElementById('last-updated');
        if (!lastUpdatedElement) {
            lastUpdatedElement = document.createElement('div');
            lastUpdatedElement.id = 'last-updated';
            lastUpdatedElement.className = 'last-updated';
            
            // Insert after the hero section or before the comparison section
            const heroSection = document.querySelector('.hero');
            if (heroSection) {
                heroSection.insertAdjacentElement('afterend', lastUpdatedElement);
            }
        }
        
        // Format the date
        const date = new Date(lastUpdated);
        const options = { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            timeZone: 'Europe/Copenhagen'
        };
        const formattedDate = date.toLocaleDateString('da-DK', options);
        
        lastUpdatedElement.innerHTML = `
            <div class="container">
                <p><i class="fas fa-clock"></i> Data opdateret: ${formattedDate}</p>
            </div>
        `;
    }
    
    setupMobileScrollEnhancements() {
        const tableResponsive = document.querySelector('.table-responsive');
        if (!tableResponsive) return;
        
        let scrollIndicator = null;
        let isScrolling = false;
        
        // Create scroll progress indicator
        const createScrollIndicator = () => {
            if (scrollIndicator) return;
            
            scrollIndicator = document.createElement('div');
            scrollIndicator.className = 'scroll-progress';
            scrollIndicator.innerHTML = `
                <div class="scroll-progress-bar"></div>
                <span class="scroll-progress-text">Scroll to see more</span>
            `;
            
            tableResponsive.parentNode.insertBefore(scrollIndicator, tableResponsive);
        };
        
        // Update scroll progress
        const updateScrollProgress = () => {
            if (!scrollIndicator) return;
            
            const scrollLeft = tableResponsive.scrollLeft;
            const maxScroll = tableResponsive.scrollWidth - tableResponsive.clientWidth;
            const progress = Math.min(scrollLeft / maxScroll, 1);
            
            const progressBar = scrollIndicator.querySelector('.scroll-progress-bar');
            const progressText = scrollIndicator.querySelector('.scroll-progress-text');
            
            if (progressBar) {
                progressBar.style.width = `${progress * 100}%`;
            }
            
            if (progressText) {
                if (progress > 0.9) {
                    progressText.textContent = 'All options visible';
                } else if (progress > 0.5) {
                    progressText.textContent = 'Keep scrolling →';
                } else {
                    progressText.textContent = 'Scroll to see more →';
                }
            }
            
            // Hide indicator when fully scrolled
            scrollIndicator.style.opacity = progress > 0.95 ? '0.3' : '1';
        };
        
        // Hide scroll indicator after scrolling stops
        const hideScrollIndicator = () => {
            if (scrollIndicator) {
                setTimeout(() => {
                    if (scrollIndicator) {
                        scrollIndicator.style.opacity = '0';
                        setTimeout(() => {
                            if (scrollIndicator && scrollIndicator.parentNode) {
                                scrollIndicator.parentNode.removeChild(scrollIndicator);
                                scrollIndicator = null;
                            }
                        }, 300);
                    }
                }, 2000);
            }
        };
        
        // Event listeners
        tableResponsive.addEventListener('scroll', () => {
            isScrolling = true;
            createScrollIndicator();
            updateScrollProgress();
            
            clearTimeout(tableResponsive.scrollTimeout);
            tableResponsive.scrollTimeout = setTimeout(() => {
                isScrolling = false;
                hideScrollIndicator();
            }, 1500);
        });
        
        // Touch events for better mobile experience
        let startX = 0;
        let startY = 0;
        
        tableResponsive.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        });
        
        tableResponsive.addEventListener('touchmove', (e) => {
            const deltaX = Math.abs(e.touches[0].clientX - startX);
            const deltaY = Math.abs(e.touches[0].clientY - startY);
            
            // If horizontal scroll is more prominent, prevent vertical scroll
            if (deltaX > deltaY && deltaX > 10) {
                e.preventDefault();
            }
        });
        
        // Add smooth scroll behavior
        tableResponsive.style.scrollBehavior = 'smooth';
    }
}

// Global functions for HTML onclick handlers
function scrollToComparison() {
    const comparisonSection = document.querySelector('.comparison-section');
    if (comparisonSection) {
        comparisonSection.scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
    }
}

function showSpeedTest() {
    // Placeholder for speed test functionality
    alert('Hastighedstest funktionalitet kommer snart!');
}

// Calculator Functions
function initializeCalculator() {
    // This will be called after data is loaded
    if (window.app && window.app.data) {
        populateCalculatorDropdowns();
    }
}

// Global function wrapper for HTML onclick
function populateCalculatorDropdowns() {
    if (window.app) {
        window.app.populateCalculatorDropdowns();
    }
}

function updateCalculatorOptions() {
    if (!window.app || !window.app.data) return;
    
    const providerSelect = document.getElementById('calculator-provider');
    const speedSelect = document.getElementById('calculator-speed');
    const contractSelect = document.getElementById('calculator-contract');
    
    if (!providerSelect || !speedSelect || !contractSelect) return;
    
    const selectedProvider = providerSelect.value;
    
    // Clear speed and contract dropdowns
    speedSelect.innerHTML = '<option value="">Vælg først en udbyder</option>';
    contractSelect.innerHTML = '<option value="">Vælg først hastighed</option>';
    
    if (!selectedProvider) return;
    
    // Filter data for selected provider
    const providerData = window.app.data.filter(item => item.provider === selectedProvider);
    
    if (providerData.length === 0) return;
    
    // Get unique speeds for this provider
    const speeds = [...new Set(providerData.map(item => item.speed))].sort((a, b) => a - b);
    
    // Populate speed dropdown
    speedSelect.innerHTML = '<option value="">Vælg hastighed</option>';
    speeds.forEach(speed => {
        const option = document.createElement('option');
        option.value = speed;
        option.textContent = `${speed} Mbit/s`;
        speedSelect.appendChild(option);
    });
    
    // Remove existing event listeners and add new one
    speedSelect.removeEventListener('change', speedSelect._changeHandler);
    speedSelect._changeHandler = function() {
        updateContractOptions(selectedProvider, this.value);
    };
    speedSelect.addEventListener('change', speedSelect._changeHandler);
}

function updateContractOptions(provider, speed) {
    if (!window.app || !window.app.data) return;
    
    const contractSelect = document.getElementById('calculator-contract');
    if (!contractSelect) return;
    
    // Clear contract dropdown
    contractSelect.innerHTML = '<option value="">Vælg først hastighed</option>';
    
    if (!provider || !speed) return;
    
    // Filter data for selected provider and speed
    const filteredData = window.app.data.filter(item => 
        item.provider === provider && item.speed === parseInt(speed)
    );
    
    if (filteredData.length === 0) return;
    
    // Get unique contract lengths for this provider and speed
    const contracts = [...new Set(filteredData.map(item => item.contractLength))].sort((a, b) => a - b);
    
    // Populate contract dropdown
    contractSelect.innerHTML = '<option value="">Vælg kontraktlængde</option>';
    contracts.forEach(contract => {
        const option = document.createElement('option');
        option.value = contract;
        option.textContent = `${contract} måneder`;
        contractSelect.appendChild(option);
    });
}

function calculateFiberPrice() {
    if (!window.app || !window.app.data) return;
    
    const providerSelect = document.getElementById('calculator-provider');
    const speedSelect = document.getElementById('calculator-speed');
    const contractSelect = document.getElementById('calculator-contract');
    const promotionsCheckbox = document.getElementById('calculator-promotions');
    const resultsDiv = document.getElementById('calculator-results');
    
    if (!providerSelect || !speedSelect || !contractSelect || !promotionsCheckbox || !resultsDiv) return;
    
    const selectedProvider = providerSelect.value;
    const selectedSpeed = parseInt(speedSelect.value);
    const selectedContract = parseInt(contractSelect.value);
    const includePromotions = promotionsCheckbox.checked;
    
    // Validate inputs
    if (!selectedProvider || !selectedSpeed || !selectedContract) {
        alert('Vælg venligst alle felter for at beregne prisen.');
        return;
    }
    
    // Find matching plan
    const matchingPlan = window.app.data.find(item => 
        item.provider === selectedProvider &&
        item.speed === selectedSpeed &&
        item.contractLength === selectedContract
    );
    
    if (!matchingPlan) {
        alert('Ingen data for dette valg. Prøv at vælge en anden kombination.');
        return;
    }
    
    // Calculate prices
    const monthlyPrice = matchingPlan.price;
    const totalMonths = selectedContract;
    let totalCost = monthlyPrice * totalMonths;
    let savings = 0;
    let promotionText = '';
    
    // Apply promotions if enabled
    if (includePromotions && matchingPlan.promotion) {
        const promotion = matchingPlan.promotion.toLowerCase();
        
        if (promotion.includes('første måned gratis') || promotion.includes('first month free')) {
            // First month free
            savings = monthlyPrice;
            totalCost -= savings;
            promotionText = matchingPlan.promotion;
        } else if (promotion.includes('kr. rabat første') || promotion.includes('kr. discount first')) {
            // Extract discount amount and months from promotion text
            const discountMatch = promotion.match(/(\d+)\s*kr\.?\s*rabat\s*første\s*(\d+)\s*måneder?/i);
            if (discountMatch) {
                const discountAmount = parseInt(discountMatch[1]);
                const discountMonths = parseInt(discountMatch[2]);
                savings = Math.min(discountAmount * discountMonths, totalCost);
                totalCost -= savings;
                promotionText = matchingPlan.promotion;
            }
        } else if (promotion.includes('gratis') || promotion.includes('free')) {
            // Generic free promotion
            promotionText = matchingPlan.promotion;
        }
    }
    
    // Display results
    document.getElementById('result-monthly').textContent = `${monthlyPrice} kr./md.`;
    document.getElementById('result-total').textContent = `${totalCost} kr.`;
    
    // Show/hide promotion info
    const promotionItem = document.getElementById('result-promotion');
    const savingsItem = document.getElementById('result-savings');
    
    if (promotionText) {
        document.getElementById('result-promotion-text').textContent = promotionText;
        promotionItem.style.display = 'flex';
    } else {
        promotionItem.style.display = 'none';
    }
    
    if (savings > 0) {
        document.getElementById('result-savings-text').textContent = `${savings} kr.`;
        savingsItem.style.display = 'flex';
    } else {
        savingsItem.style.display = 'none';
    }
    
    // Show results
    resultsDiv.style.display = 'block';
    resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function handleProviderClick(providerId, providerName, planName, price) {
    // Enhanced provider selection with tracking and confirmation
    const provider = app.filteredData.find(p => p.id === providerId);
    if (!provider) {
        console.error('Provider not found:', providerId);
        return;
    }

    // Track the click for analytics
    trackProviderClick(providerId, providerName, planName, price);
    
    // Show confirmation modal before redirect
    showProviderConfirmation(provider);
}

function trackProviderClick(providerId, providerName, planName, price) {
    // Analytics tracking
    const clickData = {
        provider_id: providerId,
        provider_name: providerName,
        plan_name: planName,
        price: price,
        timestamp: new Date().toISOString(),
        user_agent: navigator.userAgent,
        screen_resolution: `${screen.width}x${screen.height}`,
        referrer: document.referrer
    };
    
    // Log for analytics (in production, send to your analytics service)
    console.log('Provider click tracked:', clickData);
    
    // Send to analytics service (Google Analytics, Mixpanel, etc.)
    if (typeof gtag !== 'undefined') {
        gtag('event', 'provider_click', {
            'provider_name': providerName,
            'plan_name': planName,
            'price': price,
            'provider_id': providerId
        });
    }
    
    // Store in localStorage for conversion tracking
    try {
        const existingClicks = JSON.parse(localStorage.getItem('provider_clicks') || '[]');
        existingClicks.push(clickData);
        localStorage.setItem('provider_clicks', JSON.stringify(existingClicks.slice(-50))); // Keep last 50 clicks
    } catch (e) {
        console.warn('Could not store click data:', e);
    }
}

function showProviderConfirmation(provider) {
    // Create confirmation modal
    const modal = document.createElement('div');
    modal.className = 'provider-modal';
    modal.innerHTML = `
        <div class="modal-overlay"></div>
        <div class="modal-content">
            <div class="modal-header">
                <h3>Bekræft valg af ${provider.provider}</h3>
                <button class="modal-close" onclick="closeProviderModal()">&times;</button>
            </div>
            <div class="modal-body">
                <div class="provider-summary">
                    <div class="provider-logo-large">${provider.provider.charAt(0)}</div>
                    <div class="provider-details">
                        <h4>${provider.provider}</h4>
                        <p class="plan-name">${provider.plan}</p>
                        <p class="price-highlight">${provider.price} kr./md.</p>
                        <p class="contract-info">Bindingstid: ${provider.contractLength} måneder</p>
                        ${provider.promotion ? `<p class="promotion-info">${provider.promotion}</p>` : ''}
                    </div>
                </div>
                <div class="modal-actions">
                    <button class="btn-secondary" onclick="closeProviderModal()">Annuller</button>
                    <button class="btn-primary" onclick="redirectToProvider('${provider.provider}', ${provider.id})">
                        Fortsæt til ${provider.provider}
                    </button>
                </div>
                <div class="modal-footer">
                    <p><small>Du vil blive omdirigeret til ${provider.provider}'s officielle hjemmeside</small></p>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    document.body.style.overflow = 'hidden';
    
    // Close modal on overlay click
    modal.querySelector('.modal-overlay').addEventListener('click', closeProviderModal);
    
    // Close modal on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeProviderModal();
        }
    });
}

function closeProviderModal() {
    const modal = document.querySelector('.provider-modal');
    if (modal) {
        modal.remove();
        document.body.style.overflow = '';
    }
}

function redirectToProvider(providerName, providerId) {
    // Map of provider URLs - all pointing to main company pages to avoid 404s
    const providerUrls = {
        'TDC': 'https://www.yousee.dk',
        'YouSee': 'https://www.yousee.dk',
        'Telenor': 'https://www.telenor.dk',
        'Telia': 'https://www.telia.dk',
        'Stofa': 'https://www.stofa.dk',
        'Hiper': 'https://www.hiper.dk',
        'Waoo': 'https://www.waoo.dk',
        'Kviknet': 'https://www.kviknet.dk',
        'CBB': 'https://www.cbb.dk',
        'Fastspeed': 'https://www.fastspeed.dk',
        'Ewii Fiber': 'https://www.ewii.dk',
        'Hiper Pro': 'https://www.hiper.dk',
        'Norlys': 'https://www.norlys.dk',
        'Altibox': 'https://www.altibox.dk',
        'Fiberby': 'https://www.fiberby.dk',
        'Fullrate': 'https://www.fullrate.dk',
        'Energi Fyn': 'https://www.energifyn.dk',
        'SEAS-NVE': 'https://www.seas-nve.dk',
        'Fibia': 'https://www.fibia.dk'
    };
    
    // Get URL or create fallback
    let url = providerUrls[providerName];
    
    if (!url) {
        // Create fallback URL by cleaning provider name
        const cleanName = providerName.toLowerCase()
            .replace(/\s+/g, '')
            .replace(/[^a-z0-9]/g, '');
        url = `https://www.${cleanName}.dk`;
    }
    
    // Track redirect
    const isFallbackUrl = !providerUrls[providerName];
    trackProviderRedirect(providerId, providerName, url, isFallbackUrl);
    
    // Close modal and redirect
    closeProviderModal();
    
    // Open in new tab to keep user on comparison site
    window.open(url, '_blank', 'noopener,noreferrer');
}

function trackProviderRedirect(providerId, providerName, url, isFallbackUrl = false) {
    console.log('Redirecting to:', providerName, url, isFallbackUrl ? '(fallback URL)' : '(direct URL)');
    
    // Track redirect event
    if (typeof gtag !== 'undefined') {
        gtag('event', 'provider_redirect', {
            'provider_name': providerName,
            'provider_id': providerId,
            'redirect_url': url,
            'is_fallback_url': isFallbackUrl
        });
    }
}

// Initialize the application when DOM is loaded
let app;

document.addEventListener('DOMContentLoaded', () => {
    app = new TelecomComparison();
});

// Make app globally available for debugging
window.app = app;
