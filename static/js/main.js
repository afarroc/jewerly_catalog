// Main JavaScript for Jewelry Ecommerce

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components with enhanced functionality
    initBannerCarousel();
    initNavbar(); // Enhanced navbar system
    initSmoothScroll();
    initProductHoverEffects();
    initProductCardActions();
    initAnnouncementBar();
});

// Banner Carousel Functionality
function initBannerCarousel() {
    const banners = document.querySelectorAll('.banner-container');
    if (banners.length <= 1) return;

    let currentBanner = 0;
    const totalBanners = banners.length;

    // Create navigation dots
    const bannersSection = document.querySelector('.banners-section');
    if (bannersSection) {
        const dotsContainer = document.createElement('div');
        dotsContainer.className = 'carousel-dots';
        dotsContainer.style.cssText = `
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 10px;
            z-index: 10;
        `;

        for (let i = 0; i < totalBanners; i++) {
            const dot = document.createElement('button');
            dot.className = `carousel-dot ${i === 0 ? 'active' : ''}`;
            dot.style.cssText = `
                width: 12px;
                height: 12px;
                border-radius: 50%;
                border: none;
                background-color: rgba(255, 255, 255, 0.5);
                cursor: pointer;
                transition: all 0.3s ease;
            `;
            dot.addEventListener('click', () => goToBanner(i));
            dotsContainer.appendChild(dot);
        }

        bannersSection.appendChild(dotsContainer);
    }

    // Show first banner
    showBanner(currentBanner);

    // Auto-play carousel
    setInterval(() => {
        currentBanner = (currentBanner + 1) % totalBanners;
        showBanner(currentBanner);
    }, 5000);

    function showBanner(index) {
        banners.forEach((banner, i) => {
            banner.style.display = i === index ? 'flex' : 'none';
        });

        // Update dots
        const dots = document.querySelectorAll('.carousel-dot');
        dots.forEach((dot, i) => {
            dot.classList.toggle('active', i === index);
            dot.style.backgroundColor = i === index ? '#D4AF37' : 'rgba(255, 255, 255, 0.5)';
        });
    }

    function goToBanner(index) {
        currentBanner = index;
        showBanner(currentBanner);
    }
}

// Mobile Menu Functionality
function initMobileMenu() {
    const header = document.querySelector('header');
    const nav = document.querySelector('.nav');

    if (!nav) return;

    // Create mobile menu button
    const mobileMenuBtn = document.createElement('button');
    mobileMenuBtn.className = 'mobile-menu-btn';
    mobileMenuBtn.innerHTML = '☰';
    mobileMenuBtn.style.cssText = `
        display: none;
        background: none;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
        color: var(--secondary-color);
        padding: 0.5rem;
    `;

    // Insert button before nav
    nav.parentNode.insertBefore(mobileMenuBtn, nav);

    // Mobile menu styles
    const mobileMenuStyles = document.createElement('style');
    mobileMenuStyles.textContent = `
        @media (max-width: 768px) {
            .mobile-menu-btn {
                display: block !important;
            }
            .nav {
                position: fixed;
                top: 100%;
                left: 0;
                right: 0;
                background-color: var(--white);
                flex-direction: column;
                padding: 1rem;
                box-shadow: var(--shadow);
                transform: translateY(-100%);
                opacity: 0;
                visibility: hidden;
                transition: all 0.3s ease;
                z-index: 999;
            }
            .nav.open {
                transform: translateY(0);
                opacity: 1;
                visibility: visible;
            }
            .nav-item {
                margin: 0.5rem 0;
                width: 100%;
            }
            .nav-link {
                display: block;
                padding: 1rem;
                border-radius: var(--border-radius);
            }
        }
    `;
    document.head.appendChild(mobileMenuStyles);

    // Toggle mobile menu
    mobileMenuBtn.addEventListener('click', function() {
        nav.classList.toggle('open');
        mobileMenuBtn.innerHTML = nav.classList.contains('open') ? '✕' : '☰';
    });

    // Close menu when clicking outside
    document.addEventListener('click', function(e) {
        if (!header.contains(e.target)) {
            nav.classList.remove('open');
            mobileMenuBtn.innerHTML = '☰';
        }
    });
}

// Smooth Scroll for Anchor Links
function initSmoothScroll() {
    const anchorLinks = document.querySelectorAll('a[href^="#"]');

    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Product Hover Effects
function initProductHoverEffects() {
    const productCards = document.querySelectorAll('.product-card');

    productCards.forEach(card => {
        const image = card.querySelector('.product-image');

        if (image) {
            card.addEventListener('mouseenter', function() {
                image.style.transform = 'scale(1.05)';
            });

            card.addEventListener('mouseleave', function() {
                image.style.transform = 'scale(1)';
            });
        }
    });
}

// Utility Functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Add loading states for buttons
function addLoadingState(button) {
    const originalText = button.textContent;
    button.disabled = true;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Cargando...';

    return function removeLoading() {
        button.disabled = false;
        button.innerHTML = originalText;
    };
}

// Lazy load images
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');

    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                observer.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
}

// Initialize lazy loading
initLazyLoading();

// Add to cart functionality (placeholder)
function addToCart(productId) {
    // This would typically make an AJAX request
    console.log('Adding product to cart:', productId);

    // Show success message
    showNotification('Producto agregado al carrito', 'success');
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: var(--border-radius);
        color: var(--white);
        background-color: ${type === 'success' ? 'var(--success)' : 'var(--primary-color)'};
        box-shadow: var(--shadow);
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add notification animations
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(notificationStyles);

// Product Card Actions
function initProductCardActions() {
    // Quick view buttons
    document.addEventListener('click', function(e) {
        if (e.target.closest('.quick-view-btn')) {
            e.preventDefault();
            const button = e.target.closest('.quick-view-btn');
            const url = button.getAttribute('data-url');
            if (url) {
                window.open(url, '_blank');
            }
        }
    });

    // Add to cart buttons
    document.addEventListener('click', function(e) {
        if (e.target.closest('.add-to-cart-btn')) {
            e.preventDefault();
            const button = e.target.closest('.add-to-cart-btn');
            const productId = button.getAttribute('data-product-id');
            if (productId) {
                addToCart(productId);
            }
        }
    });
}

// Product Detail Page Functionality
function initProductDetailPage() {
    initQuantitySelector();
    initImageGallery();
    initDescriptionTabs();
    initImageModal();
    initProductActions();
}

// Quantity Selector
function initQuantitySelector() {
    const minusBtn = document.getElementById('qty-minus');
    const plusBtn = document.getElementById('qty-plus');
    const quantityInput = document.getElementById('quantity');

    if (!minusBtn || !plusBtn || !quantityInput) return;

    const maxStock = parseInt(quantityInput.getAttribute('max')) || 1;
    const minStock = parseInt(quantityInput.getAttribute('min')) || 1;

    minusBtn.addEventListener('click', () => {
        const currentValue = parseInt(quantityInput.value);
        if (currentValue > minStock) {
            quantityInput.value = currentValue - 1;
        }
    });

    plusBtn.addEventListener('click', () => {
        const currentValue = parseInt(quantityInput.value);
        if (currentValue < maxStock) {
            quantityInput.value = currentValue + 1;
        }
    });

    // Prevent manual input outside bounds
    quantityInput.addEventListener('change', () => {
        let value = parseInt(quantityInput.value);
        if (isNaN(value) || value < minStock) {
            value = minStock;
        } else if (value > maxStock) {
            value = maxStock;
        }
        quantityInput.value = value;
    });
}

// Image Gallery
function initImageGallery() {
    const thumbnails = document.querySelectorAll('.thumbnail-item');
    const mainImage = document.getElementById('main-product-image');

    if (!thumbnails.length || !mainImage) return;

    thumbnails.forEach(thumbnail => {
        thumbnail.addEventListener('click', () => {
            // Remove active class from all thumbnails
            thumbnails.forEach(t => t.classList.remove('active'));
            // Add active class to clicked thumbnail
            thumbnail.classList.add('active');

            // Update main image
            const imageSrc = thumbnail.getAttribute('data-image');
            if (imageSrc) {
                mainImage.src = imageSrc;
            }
        });
    });
}

// Description Tabs
function initDescriptionTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    if (!tabButtons.length) return;

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');

            // Remove active class from all buttons and panes
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabPanes.forEach(pane => pane.classList.remove('active'));

            // Add active class to clicked button and corresponding pane
            button.classList.add('active');
            const targetPane = document.getElementById(targetTab);
            if (targetPane) {
                targetPane.classList.add('active');
            }
        });
    });
}

// Image Modal
function initImageModal() {
    // Modal functionality is handled by global functions
}

function openImageModal(imageSrc) {
    const modal = document.getElementById('image-modal');
    const modalImg = document.getElementById('modal-image');

    if (modal && modalImg && imageSrc) {
        modalImg.src = imageSrc;
        modal.style.display = 'flex';
        modal.style.alignItems = 'center';
        modal.style.justifyContent = 'center';
        document.body.style.overflow = 'hidden';
    }
}

function closeImageModal() {
    const modal = document.getElementById('image-modal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

// Close modal when clicking outside
document.addEventListener('click', (e) => {
    const modal = document.getElementById('image-modal');
    if (modal && e.target === modal) {
        closeImageModal();
    }
});

// Close modal with ESC key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeImageModal();
        closeQuickView();
    }
});

// FAQ Accordion
function toggleFaq(button) {
    const faqItem = button.parentElement;
    const isActive = faqItem.classList.contains('active');

    // Close all FAQ items
    document.querySelectorAll('.faq-item').forEach(item => {
        item.classList.remove('active');
    });

    // Open clicked item if it wasn't active
    if (!isActive) {
        faqItem.classList.add('active');
    }
}

// Enhanced Image Modal Navigation
let currentImageIndex = 0;
let galleryImages = [];

function navigateImage(direction) {
    if (galleryImages.length === 0) return;

    currentImageIndex = (currentImageIndex + direction + galleryImages.length) % galleryImages.length;
    const modalImg = document.getElementById('modal-image');
    if (modalImg && galleryImages[currentImageIndex]) {
        modalImg.src = galleryImages[currentImageIndex];
    }
}

// Update openImageModal to handle gallery
function openImageModal(imageSrc) {
    const modal = document.getElementById('image-modal');
    const modalImg = document.getElementById('modal-image');

    if (modal && modalImg && imageSrc) {
        // Get all thumbnail images for gallery navigation
        galleryImages = Array.from(document.querySelectorAll('.thumbnail-item img')).map(img => img.src);
        currentImageIndex = galleryImages.indexOf(imageSrc);

        if (currentImageIndex === -1) {
            galleryImages = [imageSrc];
            currentImageIndex = 0;
        }

        modalImg.src = imageSrc;
        modal.style.display = 'flex';
        modal.style.alignItems = 'center';
        modal.style.justifyContent = 'center';
        document.body.style.overflow = 'hidden';
    }
}

// Quick View Modal
function openQuickView(productCard) {
    const modal = document.getElementById('quick-view-modal');
    const modalImg = document.getElementById('quick-view-image');
    const modalTitle = document.getElementById('quick-view-title');
    const modalPrice = document.getElementById('quick-view-price');
    const modalLink = document.getElementById('quick-view-link');

    if (modal && productCard) {
        const img = productCard.querySelector('.product-image');
        const title = productCard.querySelector('.product-title');
        const price = productCard.querySelector('.product-price');
        const link = productCard.querySelector('.product-link');

        if (img) modalImg.src = img.src;
        if (title) modalTitle.textContent = title.textContent;
        if (price) modalPrice.textContent = price.textContent;
        if (link) modalLink.href = link.href;

        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
}

function closeQuickView() {
    const modal = document.getElementById('quick-view-modal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

function addToCartFromQuickView() {
    // This would typically get the product ID from the modal and add to cart
    showNotification('Product added to cart!', 'success');
    closeQuickView();
}

// Social Sharing Functions
function shareOnFacebook() {
    const url = encodeURIComponent(window.location.href);
    const title = encodeURIComponent(document.title);
    window.open(`https://www.facebook.com/sharer/sharer.php?u=${url}&quote=${title}`, '_blank');
}

function shareOnTwitter() {
    const url = encodeURIComponent(window.location.href);
    const text = encodeURIComponent(`Check out this amazing product: ${document.title}`);
    window.open(`https://twitter.com/intent/tweet?url=${url}&text=${text}`, '_blank');
}

function shareOnPinterest() {
    const url = encodeURIComponent(window.location.href);
    const description = encodeURIComponent(document.title);
    const image = encodeURIComponent(document.querySelector('.main-image')?.src || '');
    window.open(`https://pinterest.com/pin/create/button/?url=${url}&description=${description}&media=${image}`, '_blank');
}

function shareOnWhatsApp() {
    const url = encodeURIComponent(window.location.href);
    const text = encodeURIComponent(`Check out this product: ${document.title} ${url}`);
    window.open(`https://wa.me/?text=${text}`, '_blank');
}

function shareByEmail() {
    const subject = encodeURIComponent(`Check out this product: ${document.title}`);
    const body = encodeURIComponent(`I thought you might be interested in this product:\n\n${document.title}\n${window.location.href}`);
    window.location.href = `mailto:?subject=${subject}&body=${body}`;
}

// Enhanced Product Actions
function initEnhancedProductActions() {
    // Quick view from product cards
    document.addEventListener('click', (e) => {
        if (e.target.closest('.quick-view-btn')) {
            e.preventDefault();
            const button = e.target.closest('.quick-view-btn');
            const productCard = button.closest('.product-card');
            if (productCard) {
                openQuickView(productCard);
            }
        }
    });

    // Close quick view when clicking outside
    document.addEventListener('click', (e) => {
        const modal = document.getElementById('quick-view-modal');
        if (modal && e.target === modal) {
            closeQuickView();
        }
    });

    // Keyboard navigation for image modal
    document.addEventListener('keydown', (e) => {
        const modal = document.getElementById('image-modal');
        if (modal && modal.style.display === 'flex') {
            if (e.key === 'ArrowLeft') {
                navigateImage(-1);
            } else if (e.key === 'ArrowRight') {
                navigateImage(1);
            }
        }
    });
}

// Initialize enhanced functionality
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on a product detail page
    if (document.querySelector('.product-detail-container')) {
        initProductDetailPage();
        initEnhancedProductActions();
    }
});

// Product Actions
function initProductActions() {
    // Quick add to cart from image overlay
    document.addEventListener('click', (e) => {
        if (e.target.closest('.quick-add-btn')) {
            e.preventDefault();
            const button = e.target.closest('.quick-add-btn');
            const productId = button.getAttribute('data-product-id');
            if (productId) {
                addToCart(productId);
            }
        }
    });

    // Wishlist functionality
    document.addEventListener('click', (e) => {
        if (e.target.closest('.wishlist-btn')) {
            e.preventDefault();
            const button = e.target.closest('.wishlist-btn');
            const productId = button.getAttribute('data-product-id');
            if (productId) {
                toggleWishlist(productId, button);
            }
        }
    });

    // Notify me functionality
    document.addEventListener('click', (e) => {
        if (e.target.closest('.notify-btn')) {
            e.preventDefault();
            const button = e.target.closest('.notify-btn');
            const productId = button.getAttribute('data-product-id');
            if (productId) {
                notifyWhenAvailable(productId, button);
            }
        }
    });
}

// Wishlist functionality
function toggleWishlist(productId, button) {
    // This would typically make an AJAX request
    const icon = button.querySelector('i');
    const text = button.querySelector('span');

    if (icon.classList.contains('fas')) {
        // Remove from wishlist
        icon.classList.remove('fas');
        icon.classList.add('far');
        text.textContent = 'Add to Wishlist';
        showNotification('Removed from wishlist', 'info');
    } else {
        // Add to wishlist
        icon.classList.remove('far');
        icon.classList.add('fas');
        text.textContent = 'Remove from Wishlist';
        showNotification('Added to wishlist', 'success');
    }

    console.log('Toggle wishlist for product:', productId);
}

// Notify when available
function notifyWhenAvailable(productId, button) {
    // This would typically make an AJAX request
    const removeLoading = addLoadingState(button);
    button.disabled = true;

    setTimeout(() => {
        removeLoading();
        button.innerHTML = '<i class="fas fa-check"></i> We\'ll notify you!';
        button.classList.add('notified');
        showNotification('We\'ll notify you when this product is back in stock!', 'success');
    }, 1000);

    console.log('Notify when available for product:', productId);
}

// Share product
function shareProduct() {
    if (navigator.share) {
        navigator.share({
            title: document.title,
            url: window.location.href
        });
    } else {
        // Fallback: copy to clipboard
        navigator.clipboard.writeText(window.location.href).then(() => {
            showNotification('Product link copied to clipboard!', 'success');
        });
    }
}

// Print product
function printProduct() {
    window.print();
}

// Report product
function reportProduct() {
    const reason = prompt('Please provide a reason for reporting this product:');
    if (reason) {
        // This would typically make an AJAX request
        showNotification('Thank you for your report. We\'ll review it shortly.', 'info');
        console.log('Report product:', reason);
    }
}

// Initialize product detail functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on a product detail page
    if (document.querySelector('.product-detail-container')) {
        initProductDetailPage();
    }
});

// Enhanced Robust Navbar functionality
function initNavbar() {
    // Initialize desktop navbar
    initDesktopNavbar();

    // Initialize mobile sidebar
    initMobileSidebar();

    // Initialize enhanced search
    initEnhancedSearch();

    // Initialize accessibility features
    initNavbarAccessibility();

    // Update cart count
    updateCartCount();

    // Handle window resize
    handleNavbarResize();
}

// Enhanced Desktop Navbar Functionality
function initDesktopNavbar() {
    // Enhanced dropdown functionality
    initEnhancedDropdowns();

    // Handle navbar scroll effects
    initNavbarScrollEffects();

    // Handle window resize
    handleNavbarResize();
}

// Enhanced dropdown functionality with better accessibility
function initEnhancedDropdowns() {
    const dropdowns = document.querySelectorAll('.dropdown');

    dropdowns.forEach(dropdown => {
        const toggle = dropdown.querySelector('.dropdown-toggle, .nav-link[aria-haspopup]');
        const menu = dropdown.querySelector('.dropdown-menu');

        if (toggle && menu) {
            let isOpen = false;
            let timeoutId;

            // Mouse enter/leave for desktop
            dropdown.addEventListener('mouseenter', function() {
                if (window.innerWidth > 768) {
                    clearTimeout(timeoutId);
                    openDropdown(toggle, menu);
                }
            });

            dropdown.addEventListener('mouseleave', function() {
                if (window.innerWidth > 768) {
                    timeoutId = setTimeout(() => {
                        closeDropdown(toggle, menu);
                    }, 150);
                }
            });

            // Click for mobile
            toggle.addEventListener('click', function(e) {
                if (window.innerWidth <= 768) {
                    e.preventDefault();
                    if (isOpen) {
                        closeDropdown(toggle, menu);
                    } else {
                        // Close other dropdowns first
                        closeAllDropdowns();
                        openDropdown(toggle, menu);
                    }
                    isOpen = !isOpen;
                }
            });

            // Keyboard navigation
            toggle.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    if (isOpen) {
                        closeDropdown(toggle, menu);
                    } else {
                        closeAllDropdowns();
                        openDropdown(toggle, menu);
                    }
                    isOpen = !isOpen;
                } else if (e.key === 'Escape') {
                    closeDropdown(toggle, menu);
                    isOpen = false;
                    toggle.focus();
                } else if (e.key === 'ArrowDown' && isOpen) {
                    e.preventDefault();
                    const firstItem = menu.querySelector('.dropdown-item');
                    if (firstItem) firstItem.focus();
                }
            });

            // Handle focus within dropdown
            menu.addEventListener('keydown', function(e) {
                const items = menu.querySelectorAll('.dropdown-item');
                const currentIndex = Array.from(items).indexOf(document.activeElement);

                if (e.key === 'ArrowDown') {
                    e.preventDefault();
                    const nextIndex = (currentIndex + 1) % items.length;
                    items[nextIndex].focus();
                } else if (e.key === 'ArrowUp') {
                    e.preventDefault();
                    const prevIndex = currentIndex <= 0 ? items.length - 1 : currentIndex - 1;
                    items[prevIndex].focus();
                } else if (e.key === 'Escape') {
                    closeDropdown(toggle, menu);
                    isOpen = false;
                    toggle.focus();
                }
            });
        }
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.dropdown')) {
            closeAllDropdowns();
        }
    });

    function openDropdown(toggle, menu) {
        menu.setAttribute('aria-hidden', 'false');
        toggle.setAttribute('aria-expanded', 'true');
        menu.style.opacity = '1';
        menu.style.visibility = 'visible';
        menu.style.transform = 'translateX(-50%) translateY(10px)';
    }

    function closeDropdown(toggle, menu) {
        menu.setAttribute('aria-hidden', 'true');
        toggle.setAttribute('aria-expanded', 'false');
        menu.style.opacity = '0';
        menu.style.visibility = 'hidden';
        menu.style.transform = 'translateX(-50%) translateY(-10px)';
    }

    function closeAllDropdowns() {
        document.querySelectorAll('.dropdown-menu').forEach(menu => {
            menu.setAttribute('aria-hidden', 'true');
        });
        document.querySelectorAll('.dropdown-toggle, [aria-haspopup]').forEach(toggle => {
            toggle.setAttribute('aria-expanded', 'false');
        });
    }
}

// Navbar scroll effects
function initNavbarScrollEffects() {
    const navbar = document.querySelector('.enhanced-navbar');
    let lastScrollTop = 0;
    let isScrollingDown = false;

    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

        // Add background blur on scroll
        if (scrollTop > 50) {
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
            navbar.style.backdropFilter = 'blur(20px)';
            navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.backdropFilter = 'blur(20px)';
            navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.08)';
        }

        // Hide/show navbar on scroll (optional - can be enabled if desired)
        /*
        isScrollingDown = scrollTop > lastScrollTop;
        lastScrollTop = scrollTop;

        if (isScrollingDown && scrollTop > 200) {
            navbar.style.transform = 'translateY(-100%)';
        } else {
            navbar.style.transform = 'translateY(0)';
        }
        */
    });
}

// Handle navbar responsive behavior
function handleNavbarResize() {
    const mobileToggle = document.getElementById('mobile-menu-toggle');
    const mobileOverlay = document.getElementById('mobile-nav-overlay');

    window.addEventListener('resize', debounce(function() {
        if (window.innerWidth >= 768) {
            // Desktop mode
            if (mobileOverlay) {
                mobileOverlay.classList.remove('active');
                mobileOverlay.setAttribute('aria-hidden', 'true');
            }
            if (mobileToggle) {
                mobileToggle.classList.remove('active');
                mobileToggle.setAttribute('aria-expanded', 'false');
            }
            document.body.style.overflow = 'auto';
        }
    }, 250));
}

// Enhanced Mobile Sidebar Functionality
function initMobileSidebar() {
    const mobileToggle = document.getElementById('mobile-menu-toggle');
    const mobileOverlay = document.getElementById('mobile-nav-overlay');
    const sidebarClose = document.getElementById('mobile-nav-close');

    if (mobileToggle && mobileOverlay) {
        // Toggle sidebar
        mobileToggle.addEventListener('click', function(e) {
            e.preventDefault();
            toggleMobileSidebar();
        });

        // Close sidebar
        if (sidebarClose) {
            sidebarClose.addEventListener('click', function(e) {
                e.preventDefault();
                closeMobileSidebar();
            });
        }

        // Close sidebar when clicking overlay
        mobileOverlay.addEventListener('click', function(e) {
            if (e.target === mobileOverlay) {
                closeMobileSidebar();
            }
        });

        // Handle swipe gestures for mobile
        initSwipeGestures();
    }

    // Handle escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && mobileOverlay.classList.contains('active')) {
            closeMobileSidebar();
        }
    });

    // Close sidebar on navigation (for single-page navigation)
    const mobileLinks = mobileOverlay.querySelectorAll('.mobile-nav-link');
    mobileLinks.forEach(link => {
        link.addEventListener('click', function() {
            // Only close if it's not an external link or modal trigger
            if (!this.hasAttribute('data-modal') && !this.hasAttribute('target')) {
                closeMobileSidebar();
            }
        });
    });

    function toggleMobileSidebar() {
        const isActive = mobileOverlay.classList.contains('active');

        if (isActive) {
            closeMobileSidebar();
        } else {
            openMobileSidebar();
        }
    }

    function openMobileSidebar() {
        mobileOverlay.classList.add('active');
        mobileOverlay.setAttribute('aria-hidden', 'false');
        mobileToggle.classList.add('active');
        mobileToggle.setAttribute('aria-expanded', 'true');
        document.body.style.overflow = 'hidden';

        // Focus management
        const firstFocusable = mobileOverlay.querySelector('.mobile-nav-link');
        if (firstFocusable) {
            setTimeout(() => firstFocusable.focus(), 100);
        }

        // Announce to screen readers
        announceToScreenReader('Menú de navegación abierto');
    }

    function closeMobileSidebar() {
        mobileOverlay.classList.remove('active');
        mobileOverlay.setAttribute('aria-hidden', 'true');
        mobileToggle.classList.remove('active');
        mobileToggle.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = 'auto';

        // Return focus to toggle button
        mobileToggle.focus();

        // Announce to screen readers
        announceToScreenReader('Menú de navegación cerrado');
    }

    // Swipe gesture support for mobile
    function initSwipeGestures() {
        let startX = 0;
        let startY = 0;
        let isTracking = false;

        mobileOverlay.addEventListener('touchstart', function(e) {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
            isTracking = true;
        });

        mobileOverlay.addEventListener('touchmove', function(e) {
            if (!isTracking) return;

            const currentX = e.touches[0].clientX;
            const currentY = e.touches[0].clientY;
            const diffX = startX - currentX;
            const diffY = startY - currentY;

            // Only handle horizontal swipes
            if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
                if (diffX > 0) {
                    // Swipe left - close sidebar
                    closeMobileSidebar();
                }
                isTracking = false;
            }
        });

        mobileOverlay.addEventListener('touchend', function() {
            isTracking = false;
        });
    }

    // Screen reader announcements
    function announceToScreenReader(message) {
        const announcement = document.createElement('div');
        announcement.setAttribute('aria-live', 'polite');
        announcement.setAttribute('aria-atomic', 'true');
        announcement.style.position = 'absolute';
        announcement.style.left = '-10000px';
        announcement.style.width = '1px';
        announcement.style.height = '1px';
        announcement.style.overflow = 'hidden';

        announcement.textContent = message;
        document.body.appendChild(announcement);

        setTimeout(() => {
            document.body.removeChild(announcement);
        }, 1000);
    }
}

// Dropdown functionality for desktop
function initDropdowns() {
    const dropdowns = document.querySelectorAll('.dropdown');

    dropdowns.forEach(dropdown => {
        const toggle = dropdown.querySelector('.dropdown-toggle');
        const menu = dropdown.querySelector('.dropdown-menu');

        if (toggle && menu) {
            // Mouse enter/leave for desktop
            dropdown.addEventListener('mouseenter', function() {
                if (window.innerWidth > 768) {
                    menu.setAttribute('aria-hidden', 'false');
                    toggle.setAttribute('aria-expanded', 'true');
                }
            });

            dropdown.addEventListener('mouseleave', function() {
                if (window.innerWidth > 768) {
                    menu.setAttribute('aria-hidden', 'true');
                    toggle.setAttribute('aria-expanded', 'false');
                }
            });

            // Click for mobile
            toggle.addEventListener('click', function(e) {
                if (window.innerWidth <= 768) {
                    e.preventDefault();
                    const isExpanded = toggle.getAttribute('aria-expanded') === 'true';
                    toggle.setAttribute('aria-expanded', !isExpanded);
                    menu.setAttribute('aria-hidden', isExpanded);
                }
            });
        }
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.dropdown')) {
            document.querySelectorAll('.dropdown-menu').forEach(menu => {
                menu.setAttribute('aria-hidden', 'true');
            });
            document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
                toggle.setAttribute('aria-expanded', 'false');
            });
        }
    });
}

// Keyboard navigation for accessibility
function initKeyboardNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const dropdownItems = document.querySelectorAll('.dropdown-item');

    // Arrow key navigation for dropdowns
    document.addEventListener('keydown', function(e) {
        const activeElement = document.activeElement;

        if (e.key === 'ArrowDown' && activeElement.closest('.dropdown')) {
            e.preventDefault();
            const dropdown = activeElement.closest('.dropdown');
            const menu = dropdown.querySelector('.dropdown-menu');
            const firstItem = menu.querySelector('.dropdown-item');

            if (firstItem && menu.getAttribute('aria-hidden') !== 'false') {
                menu.setAttribute('aria-hidden', 'false');
                activeElement.setAttribute('aria-expanded', 'true');
                firstItem.focus();
            }
        }

        if (e.key === 'Escape') {
            // Close any open dropdowns
            document.querySelectorAll('.dropdown-menu').forEach(menu => {
                menu.setAttribute('aria-hidden', 'true');
            });
            document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
                toggle.setAttribute('aria-expanded', 'false');
            });

            // Return focus to toggle
            const focusedDropdown = document.activeElement.closest('.dropdown');
            if (focusedDropdown) {
                focusedDropdown.querySelector('.dropdown-toggle').focus();
            }
        }
    });

    // Tab navigation
    navLinks.forEach(link => {
        link.addEventListener('focus', function() {
            // Close other dropdowns when focusing on a new nav item
            document.querySelectorAll('.dropdown-menu').forEach(menu => {
                if (!this.closest('.dropdown')?.contains(menu)) {
                    menu.setAttribute('aria-hidden', 'true');
                }
            });
        });
    });
}

// Update cart count in navbar
function updateCartCount() {
    const cartCountElement = document.getElementById('cart-count');
    if (cartCountElement) {
        // This would typically get the cart count from localStorage or API
        const cartCount = localStorage.getItem('cartCount') || 0;
        if (cartCount > 0) {
            cartCountElement.textContent = cartCount;
            cartCountElement.style.display = 'flex';
        } else {
            cartCountElement.style.display = 'none';
        }
    }
}

// Back to top functionality
function initBackToTop() {
    const backToTopBtn = document.getElementById('back-to-top');

    if (!backToTopBtn) return;

    // Show/hide button based on scroll position
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopBtn.classList.add('visible');
        } else {
            backToTopBtn.classList.remove('visible');
        }
    });

    // Scroll to top when clicked
    backToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Newsletter signup functionality
function initNewsletterSignup() {
    const newsletterForm = document.getElementById('newsletter-form');

    if (!newsletterForm) return;

    newsletterForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const emailInput = this.querySelector('input[type="email"]');
        const submitBtn = this.querySelector('button');

        if (!emailInput.value) {
            showNotification('Por favor ingresa tu email', 'error');
            return;
        }

        const removeLoading = addLoadingState(submitBtn);
        submitBtn.disabled = true;

        // Simulate API call
        setTimeout(() => {
            removeLoading();
            emailInput.value = '';
            showNotification('¡Gracias por suscribirte! Recibirás nuestras últimas novedades.', 'success');
        }, 1500);
    });
}

// Announcement bar functionality
function initAnnouncementBar() {
    const announcementClose = document.getElementById('announcement-close');
    const announcementBar = document.querySelector('.announcement-bar');

    if (announcementClose && announcementBar) {
        announcementClose.addEventListener('click', function() {
            announcementBar.style.display = 'none';
        });

        // Auto-hide after 10 seconds
        setTimeout(() => {
            if (announcementBar.style.display !== 'none') {
                announcementBar.style.display = 'none';
            }
        }, 10000);
    }
}

// Enhanced cart functionality
function addToCart(productId, quantity = 1) {
    // Update localStorage cart count
    let cartCount = parseInt(localStorage.getItem('cartCount') || 0);
    cartCount += quantity;
    localStorage.setItem('cartCount', cartCount);

    // Update cart count display
    updateCartCount();

    // Show notification
    showNotification('Producto agregado al carrito', 'success');

    // This would typically make an AJAX request to add to cart
    console.log('Adding to cart:', productId, 'Quantity:', quantity);
}

// Smooth scroll for anchor links
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Navbar Accessibility Features
function initNavbarAccessibility() {
    // Skip link functionality
    const skipLink = document.querySelector('.skip-link');
    if (skipLink) {
        skipLink.addEventListener('click', function(e) {
            e.preventDefault();
            const mainContent = document.getElementById('main-content');
            if (mainContent) {
                mainContent.focus();
                mainContent.scrollIntoView();
            }
        });

        // Show skip link on focus
        skipLink.addEventListener('focus', function() {
            this.style.top = '6px';
        });

        skipLink.addEventListener('blur', function() {
            this.style.top = '-40px';
        });
    }

    // Focus trap for mobile menu
    const mobileOverlay = document.getElementById('mobile-nav-overlay');
    if (mobileOverlay) {
        mobileOverlay.addEventListener('keydown', function(e) {
            if (e.key === 'Tab') {
                const focusableElements = mobileOverlay.querySelectorAll(
                    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
                );
                const firstElement = focusableElements[0];
                const lastElement = focusableElements[focusableElements.length - 1];

                if (e.shiftKey) {
                    if (document.activeElement === firstElement) {
                        lastElement.focus();
                        e.preventDefault();
                    }
                } else {
                    if (document.activeElement === lastElement) {
                        firstElement.focus();
                        e.preventDefault();
                    }
                }
            }
        });
    }

    // Announce dynamic content changes
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                const addedNode = mutation.addedNodes[0];
                if (addedNode.nodeType === Node.ELEMENT_NODE &&
                    (addedNode.classList.contains('dropdown-menu') ||
                     addedNode.classList.contains('search-suggestions'))) {
                    announceToScreenReader('Contenido dinámico cargado');
                }
            }
        });
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });

    function announceToScreenReader(message) {
        const announcement = document.createElement('div');
        announcement.setAttribute('aria-live', 'polite');
        announcement.setAttribute('aria-atomic', 'true');
        announcement.style.position = 'absolute';
        announcement.style.left = '-10000px';
        announcement.style.width = '1px';
        announcement.style.height = '1px';
        announcement.style.overflow = 'hidden';

        announcement.textContent = message;
        document.body.appendChild(announcement);

        setTimeout(() => {
            document.body.removeChild(announcement);
        }, 1000);
    }
}

// Enhanced initialization with error handling and performance optimizations
document.addEventListener('DOMContentLoaded', function() {
    try {
        // Core navbar functionality
        initNavbar();

        // Additional features
        initBackToTop();
        initNewsletterSignup();
        initAnnouncementBar();
        initSmoothScroll();

        // Page-specific functionality
        if (document.querySelector('.product-detail-container')) {
            initProductDetailPage();
            initEnhancedProductActions();
        }

        // Performance optimizations (lazy load)
        setTimeout(() => {
            initPerformanceOptimizations();
        }, 1000);

        console.log('Enhanced navbar system initialized successfully');
    } catch (error) {
        console.error('Error during enhanced navbar initialization:', error);
        // Fallback: ensure basic functionality works
        initMobileSidebar();
        initEnhancedSearch();
    }
});

// Performance optimizations
function initPerformanceOptimizations() {
    // Preload critical resources
    const criticalImages = document.querySelectorAll('img[loading="lazy"]');
    criticalImages.forEach(img => {
        if (img.getBoundingClientRect().top < window.innerHeight * 2) {
            img.loading = 'eager';
        }
    });

    // Optimize scroll performance
    let ticking = false;
    window.addEventListener('scroll', function() {
        if (!ticking) {
            requestAnimationFrame(function() {
                // Handle scroll-based optimizations
                optimizeVisibleElements();
                ticking = false;
            });
            ticking = true;
        }
    });

    function optimizeVisibleElements() {
        // Add will-change property to animating elements during scroll
        const animatingElements = document.querySelectorAll('.action-btn, .nav-link');
        animatingElements.forEach(el => {
            el.style.willChange = 'transform';
            setTimeout(() => {
                el.style.willChange = 'auto';
            }, 1000);
        });
    }
}

// Enhanced Search Functionality
function initEnhancedSearch() {
    const searchInputs = document.querySelectorAll('.search-input');
    const searchForms = document.querySelectorAll('.search-form');

    searchInputs.forEach((searchInput, index) => {
        const searchForm = searchForms[index];
        if (!searchInput || !searchForm) return;

        let searchTimeout;
        let currentSuggestions = [];
        let selectedIndex = -1;

        // Search input wrapper for better event handling
        const searchWrapper = searchInput.closest('.search-input-wrapper') || searchInput.parentElement;
        const searchBtn = searchWrapper ? searchWrapper.querySelector('.search-btn') : null;
        const searchClear = searchWrapper ? searchWrapper.querySelector('.search-clear') : null;

        // Real-time search suggestions (debounced)
        searchInput.addEventListener('input', function() {
            const query = this.value.trim();
            clearTimeout(searchTimeout);

            // Show/hide clear button
            if (searchClear) {
                searchClear.style.display = query ? 'flex' : 'none';
            }

            if (query.length >= 2) {
                searchTimeout = setTimeout(() => {
                    showEnhancedSearchSuggestions(query, searchInput);
                }, 300);
            } else {
                hideSearchSuggestions(searchInput);
            }

            selectedIndex = -1;
        });

        // Clear search
        if (searchClear) {
            searchClear.addEventListener('click', function() {
                searchInput.value = '';
                searchInput.focus();
                hideSearchSuggestions(searchInput);
                this.style.display = 'none';
            });
        }

        // Handle search form submission
        searchForm.addEventListener('submit', function(e) {
            const query = searchInput.value.trim();
            if (!query) {
                e.preventDefault();
                showNotification('Por favor ingresa un término de búsqueda', 'warning');
                searchInput.focus();
                return;
            }

            // Add loading state
            const removeLoading = addLoadingState(searchBtn);
            hideSearchSuggestions(searchInput);

            // Simulate search processing
            setTimeout(() => {
                removeLoading();
            }, 500);
        });

        // Keyboard navigation for search
        searchInput.addEventListener('keydown', function(e) {
            const suggestions = this.parentElement.querySelector('.search-suggestions');

            if (!suggestions || suggestions.style.display === 'none') {
                if (e.key === 'Escape') {
                    this.blur();
                }
                return;
            }

            const suggestionItems = suggestions.querySelectorAll('.suggestion-item');

            switch (e.key) {
                case 'ArrowDown':
                    e.preventDefault();
                    selectedIndex = (selectedIndex + 1) % suggestionItems.length;
                    updateSuggestionSelection(suggestionItems, selectedIndex);
                    break;
                case 'ArrowUp':
                    e.preventDefault();
                    selectedIndex = selectedIndex <= 0 ? suggestionItems.length - 1 : selectedIndex - 1;
                    updateSuggestionSelection(suggestionItems, selectedIndex);
                    break;
                case 'Enter':
                    if (selectedIndex >= 0 && suggestionItems[selectedIndex]) {
                        e.preventDefault();
                        suggestionItems[selectedIndex].click();
                    }
                    break;
                case 'Escape':
                    hideSearchSuggestions(searchInput);
                    selectedIndex = -1;
                    break;
            }
        });

        // Close suggestions when clicking outside
        document.addEventListener('click', function(e) {
            const navbarSearch = searchInput.closest('.navbar-search') || searchInput.parentElement;
            if (navbarSearch && !navbarSearch.contains(e.target)) {
                hideSearchSuggestions(searchInput);
                selectedIndex = -1;
            }
        });

        // Handle focus events
        searchInput.addEventListener('focus', function() {
            const query = this.value.trim();
            if (query.length >= 2) {
                showEnhancedSearchSuggestions(query, this);
            }
        });

        searchInput.addEventListener('blur', function() {
            // Delay hiding to allow clicking on suggestions
            setTimeout(() => {
                const navbarSearch = this.closest('.navbar-search') || this.parentElement;
                if (navbarSearch && !navbarSearch.contains(document.activeElement)) {
                    hideSearchSuggestions(this);
                    selectedIndex = -1;
                }
            }, 150);
        });
    });

    function showEnhancedSearchSuggestions(query, searchInput) {
        hideSearchSuggestions(searchInput);

        // Create suggestions container
        const searchWrapper = searchInput.closest('.search-input-wrapper') || searchInput.parentElement;
        if (!searchWrapper) return;

        const suggestions = document.createElement('div');
        suggestions.className = 'search-suggestions';
        suggestions.setAttribute('role', 'listbox');
        suggestions.setAttribute('aria-label', 'Sugerencias de búsqueda');

        // Mock search suggestions - replace with actual API call
        const mockSuggestions = [
            { text: `Buscar "${query}" en productos`, icon: 'fas fa-search', action: 'search' },
            { text: `Buscar "${query}" en categorías`, icon: 'fas fa-tags', action: 'category' },
            { text: `Ver productos destacados`, icon: 'fas fa-star', action: 'featured' }
        ];

        mockSuggestions.forEach((suggestion, index) => {
            const item = document.createElement('div');
            item.className = 'suggestion-item';
            item.setAttribute('role', 'option');
            item.setAttribute('tabindex', '-1');
            item.innerHTML = `
                <i class="${suggestion.icon}" aria-hidden="true"></i>
                <span>${suggestion.text}</span>
            `;

            item.addEventListener('click', function() {
                handleSuggestionClick(suggestion, query, searchInput);
            });

            item.addEventListener('mouseenter', function() {
                selectedIndex = index;
                updateSuggestionSelection(suggestions.querySelectorAll('.suggestion-item'), selectedIndex);
            });

            suggestions.appendChild(item);
        });

        searchWrapper.appendChild(suggestions);
        suggestions.style.display = 'block';

        // Position suggestions
        positionSuggestions(suggestions, searchInput);
    }

    function handleSuggestionClick(suggestion, query, searchInput) {
        searchInput.value = query;
        hideSearchSuggestions(searchInput);

        // Handle different suggestion types
        switch (suggestion.action) {
            case 'search':
                const form = searchInput.closest('form') || searchInput.parentElement;
                if (form && form.tagName === 'FORM') {
                    form.submit();
                }
                break;
            case 'category':
                // Redirect to category search
                window.location.href = `/products/?q=${encodeURIComponent(query)}&type=category`;
                break;
            case 'featured':
                // Redirect to featured products
                window.location.href = '/products/?featured=true';
                break;
        }
    }

    function updateSuggestionSelection(items, selectedIndex) {
        items.forEach((item, index) => {
            item.classList.toggle('selected', index === selectedIndex);
        });
    }

    function positionSuggestions(suggestions, searchInput) {
        const rect = searchInput.getBoundingClientRect();
        const viewportHeight = window.innerHeight;
        const suggestionsHeight = 200; // Approximate height

        // Position below input by default
        suggestions.style.top = '100%';
        suggestions.style.bottom = 'auto';

        // If not enough space below, position above
        if (rect.bottom + suggestionsHeight > viewportHeight) {
            suggestions.style.top = 'auto';
            suggestions.style.bottom = '100%';
        }
    }

    function hideSearchSuggestions(searchInput) {
        const parentElement = searchInput.parentElement;
        if (parentElement) {
            const suggestions = parentElement.querySelector('.search-suggestions');
            if (suggestions) {
                suggestions.remove();
            }
        }
    }
}

// Show search suggestions
function showSearchSuggestions(query) {
    // Remove existing suggestions
    hideSearchSuggestions();

    // Create suggestions container
    const searchWrapper = document.querySelector('.search-input-wrapper');
    const suggestions = document.createElement('div');
    suggestions.className = 'search-suggestions';
    suggestions.innerHTML = `
        <div class="suggestion-item">
            <i class="fas fa-search"></i>
            <span>Buscar "${query}" en productos</span>
        </div>
        <div class="suggestion-item">
            <i class="fas fa-star"></i>
            <span>Buscar "${query}" en destacados</span>
        </div>
    `;

    searchWrapper.appendChild(suggestions);

    // Add click handlers
    suggestions.querySelectorAll('.suggestion-item').forEach(item => {
        item.addEventListener('click', function() {
            const searchInput = document.querySelector('.search-input');
            searchInput.value = query;
            const form = searchInput.closest('form') || searchInput.parentElement;
            if (form && form.tagName === 'FORM') {
                form.submit();
            }
        });
    });
}

// Hide search suggestions
function hideSearchSuggestions() {
    const suggestions = document.querySelector('.search-suggestions');
    if (suggestions) {
        suggestions.remove();
    }
}

// Enhanced cart functionality with localStorage
function updateCartCount() {
    const cartCountElement = document.getElementById('cart-count');
    if (cartCountElement) {
        // Get cart count from localStorage or API
        let cartCount = 0;

        // Try to get from localStorage first
        const storedCart = localStorage.getItem('jewelryCart');
        if (storedCart) {
            try {
                const cart = JSON.parse(storedCart);
                cartCount = cart.reduce((total, item) => total + item.quantity, 0);
            } catch (e) {
                console.warn('Error parsing cart data:', e);
            }
        }

        if (cartCount > 0) {
            cartCountElement.textContent = cartCount > 99 ? '99+' : cartCount;
            cartCountElement.style.display = 'flex';
        } else {
            cartCountElement.style.display = 'none';
        }
    }
}

// Enhanced add to cart with localStorage
function addToCart(productId, quantity = 1) {
    // Get existing cart
    let cart = [];
    const storedCart = localStorage.getItem('jewelryCart');

    if (storedCart) {
        try {
            cart = JSON.parse(storedCart);
        } catch (e) {
            console.warn('Error parsing cart data, resetting cart');
            cart = [];
        }
    }

    // Check if product already exists
    const existingItem = cart.find(item => item.id === productId);

    if (existingItem) {
        existingItem.quantity += quantity;
    } else {
        cart.push({
            id: productId,
            quantity: quantity,
            addedAt: new Date().toISOString()
        });
    }

    // Save to localStorage
    localStorage.setItem('jewelryCart', JSON.stringify(cart));

    // Update UI
    updateCartCount();

    // Show notification
    showNotification(`Producto agregado al carrito (${quantity})`, 'success');

    console.log('Cart updated:', cart);
}

// Export functions for global use
window.JewelryEcommerce = {
    addToCart,
    showNotification,
    addLoadingState,
    openImageModal,
    closeImageModal,
    shareProduct,
    printProduct,
    reportProduct,
    updateCartCount
};