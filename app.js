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
        if (!tbody) return;

        // Clear existing rows
        tbody.innerHTML = '';

        // Render each provider row
        this.filteredData.forEach(provider => {
            const row = this.createTableRow(provider);
            tbody.appendChild(row);
        });

        // Update results count
        this.updateResultsCount();
    }

    createTableRow(provider) {
        const row = document.createElement('tr');
        
        row.innerHTML = `
            <td class="provider-cell">
                <div class="provider-logo">${provider.provider.charAt(0)}</div>
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
                <button class="action-btn" onclick="handleProviderClick(${provider.id})">
                    Vælg Tilbud
                </button>
            </td>
        `;

        return row;
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

function handleProviderClick(providerId) {
    // Placeholder for provider selection functionality
    const provider = app.filteredData.find(p => p.id === providerId);
    if (provider) {
        alert(`Vælger ${provider.provider} - ${provider.plan} til ${provider.price} kr./md.`);
    }
}

// Initialize the application when DOM is loaded
let app;

document.addEventListener('DOMContentLoaded', () => {
    app = new TelecomComparison();
});

// Make app globally available for debugging
window.app = app;
