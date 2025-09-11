// Mobile menu toggle and general DOM setup
document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu elements
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const mainNav = document.querySelector('.main-nav');

    // Handle mobile menu functionality
    if (mobileMenuBtn && mainNav) {
        // Track menu state
        let isMenuOpen = false;

        // Check if current view is mobile
        const isMobileView = () => window.innerWidth <= 992;

        // Set initial menu state
        mainNav.style.display = isMobileView() ? 'none' : 'flex';

        // Toggle menu visibility
        const toggleMenu = (shouldOpen) => {
            const open = typeof shouldOpen === 'boolean' ? shouldOpen : !isMenuOpen;

            if (isMobileView()) {
                mainNav.style.display = open ? 'flex' : 'none';
                mobileMenuBtn.classList.toggle('active', open);
                mainNav.classList.toggle('active', open);
                document.body.style.overflow = open ? 'hidden' : '';
                isMenuOpen = open;
            } else {
                mainNav.style.display = 'flex';
                isMenuOpen = false;
            }
        };

        // Mobile menu button click handler
        mobileMenuBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            toggleMenu();
        });

        // Close menu when clicking outside
        const handleDocumentClick = (e) => {
            if (isMenuOpen && isMobileView() &&
                !mainNav.contains(e.target) &&
                !mobileMenuBtn.contains(e.target)) {
                toggleMenu(false);
            }
        };

        document.addEventListener('click', handleDocumentClick);

        // Close menu when clicking on nav links
        mainNav.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                if (isMobileView()) {
                    toggleMenu(false);
                }
            });
        });

        // Handle window resize
        const handleResize = () => {
            if (isMobileView()) {
                if (isMenuOpen) {
                    mainNav.style.display = 'flex';
                }
            } else {
                mainNav.style.display = 'flex';
                isMenuOpen = false;
                document.body.style.overflow = '';
            }
        };

        window.addEventListener('resize', handleResize);
    }

    // Mobile dropdown functionality
    const userMenuBtn = document.querySelector('.user-menu-btn');
    const navDropdown = document.querySelector('.nav-dropdown');

    if (userMenuBtn && navDropdown) {
        // Check if current view is mobile
        const isMobileView = () => window.innerWidth <= 992;

        // Toggle dropdown for mobile
        const toggleDropdown = (shouldOpen) => {
            const open = typeof shouldOpen === 'boolean' ? shouldOpen : !navDropdown.classList.contains('active');

            if (isMobileView()) {
                navDropdown.classList.toggle('active', open);
            }
        };

        // Handle user menu button click
        userMenuBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();

            if (isMobileView()) {
                toggleDropdown();
            }
        });

        // Close dropdown when clicking on dropdown items
        navDropdown.querySelectorAll('.dropdown-item').forEach(item => {
            item.addEventListener('click', () => {
                if (isMobileView()) {
                    toggleDropdown(false);
                }
            });
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (isMobileView() &&
                navDropdown.classList.contains('active') &&
                !navDropdown.contains(e.target)) {
                toggleDropdown(false);
            }
        });

        // Handle window resize
        window.addEventListener('resize', () => {
            if (!isMobileView()) {
                navDropdown.classList.remove('active');
            }
        });
    }
    
    // Quantity selector functionality
    document.querySelectorAll('.qty-btn').forEach(button => {
        button.addEventListener('click', function() {
            const input = this.parentNode.querySelector('input[type=number]');
            if (!input) return;
            
            if (this.classList.contains('minus')) {
                input.stepDown();
            } else if (this.classList.contains('plus')) {
                input.stepUp();
            }
            input.dispatchEvent(new Event('change'));
        });
    });

    // Password strength indicator
    const password1 = document.getElementById('id_new_password1');
    if (password1) {
        initializePasswordStrengthMeter(password1);
    }

    // Checkout form handling
    initializeCheckoutForm();
    
    // Stripe payment initialization
    initializeStripePayment();
});

// Password strength meter functions
function initializePasswordStrengthMeter(passwordField) {
    const passwordStrength = document.querySelector('.password-strength') || createPasswordStrengthMeter(passwordField);
    const passwordCriteria = document.querySelector('.password-criteria') || createPasswordCriteria(passwordField);
    
    passwordField.addEventListener('input', function() {
        updatePasswordStrength(this.value, passwordStrength, passwordCriteria);
    });
}

function createPasswordStrengthMeter(passwordField) {
    const strengthMeter = document.createElement('div');
    strengthMeter.className = 'password-strength';
    strengthMeter.innerHTML = `
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        <small class="strength-text"></small>
    `;
    passwordField.parentNode.insertBefore(strengthMeter, passwordField.nextSibling);
    return strengthMeter;
}

function createPasswordCriteria(passwordField) {
    const criteriaList = document.createElement('div');
    criteriaList.className = 'password-criteria';
    criteriaList.innerHTML = `
        <p>Your password must contain:</p>
        <ul>
            <li class="length"><i class="fas fa-circle"></i> At least 8 characters</li>
            <li class="numeric"><i class="fas fa-circle"></i> At least 1 number</li>
            <li class="special"><i class="fas fa-circle"></i> At least 1 special character</li>
        </ul>
    `;
    passwordField.parentNode.insertBefore(criteriaList, passwordField.nextSibling.nextSibling);
    return criteriaList;
}

function updatePasswordStrength(password, strengthMeter, criteriaList) {
    const strengthBars = strengthMeter.querySelectorAll('span');
    const strengthText = strengthMeter.querySelector('.strength-text');
    const criteriaItems = criteriaList.querySelectorAll('li');
    
    // Reset all bars
    strengthBars.forEach(bar => bar.className = '');
    
    // Check password criteria
    const hasMinLength = password.length >= 8;
    const hasNumber = /\d/.test(password);
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);
    
    // Update criteria indicators
    criteriaItems[0].className = hasMinLength ? 'valid' : 'invalid';
    criteriaItems[1].className = hasNumber ? 'valid' : 'invalid';
    criteriaItems[2].className = hasSpecialChar ? 'valid' : 'invalid';
    
    // Calculate strength
    let strength = 0;
    if (password.length > 0) strength += 1;
    if (password.length >= 8) strength += 1;
    if (hasNumber) strength += 1;
    if (hasSpecialChar) strength += 1;
    if (password.length >= 12) strength += 1;
    
    // Update strength meter
    for (let i = 0; i < strength; i++) {
        if (i < 2) strengthBars[i].className = 'weak';
        else if (i < 4) strengthBars[i].className = 'medium';
        else strengthBars[i].className = 'strong';
    }
    
    // Update strength text
    if (!password.length) {
        strengthText.textContent = '';
    } else {
        strengthText.textContent = 
            strength <= 2 ? 'Weak' : 
            strength <= 4 ? 'Medium' : 'Strong';
        strengthText.style.color = 
            strength <= 2 ? 'var(--danger-color)' : 
            strength <= 4 ? 'var(--warning-color)' : 'var(--success-color)';
    }
}

// Checkout form handling
function initializeCheckoutForm() {
    const form = document.querySelector('.checkout-form');
    if (!form) return;

    const placeOrderBtn = document.getElementById('place-order-btn');
    if (!placeOrderBtn) return;

    // Terms agreement validation
    form.addEventListener('submit', function(e) {
        if (!document.getElementById('agree-terms').checked) {
            e.preventDefault();
            showAlert('You must accept the terms and conditions to continue', 'error');
            return false;
        }
        
        placeOrderBtn.disabled = true;
        placeOrderBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
    });
    
    // Billing address toggle
    const billingOptions = document.querySelectorAll('input[name="billing_option"]');
    const billingSection = document.getElementById('billing-address-section');
    
    if (billingOptions.length && billingSection) {
        billingOptions.forEach(option => {
            option.addEventListener('change', function() {
                billingSection.style.display = this.value === 'different' ? 'block' : 'none';
            });
        });
    }
}

// Stripe payment initialization
function initializeStripePayment() {
    const stripeForm = document.getElementById('payment-form');
    if (!stripeForm || !window.Stripe) return;

    const stripePublicKey = stripeForm.dataset.stripeKey || document.querySelector('meta[name="stripe-public-key"]').content;
    if (!stripePublicKey) return;

    const stripe = Stripe(stripePublicKey);
    const elements = stripe.elements();
    const paymentElement = elements.create('payment');
    paymentElement.mount('#payment-element');

    stripeForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const submitBtn = document.getElementById('place-order-btn');
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';

        try {
            // First create the order
            const formData = new FormData(stripeForm);
            const response = await fetch(stripeForm.action || window.location.href, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCSRFToken()
                }
            });

            if (response.redirected) {
                window.location.href = response.url;
                return;
            }

            const result = await response.json();
            
            if (!result.success) {
                throw new Error(result.error || 'Order creation failed');
            }

            // Then process Stripe payment
            const { error } = await stripe.confirmPayment({
                elements,
                clientSecret: result.client_secret,
                confirmParams: {
                    return_url: `${window.location.origin}${result.confirmation_url || '/order-confirmation/'}`,
                },
            });

            if (error) {
                throw new Error(error.message);
            }
            
        } catch (error) {
            showAlert(error.message, 'error');
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="fas fa-lock"></i> Complete Purchase';
        }
    });
}

// Helper functions
function getCSRFToken() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    return csrfToken ? csrfToken.value : '';
}

function showAlert(message, type = 'info') {
    // Implement your alert/show notification function here
    console.log(`${type.toUpperCase()}: ${message}`);
    // Example: You could use Toastify, SweetAlert, or a custom alert component
    // alert(`${type.toUpperCase()}: ${message}`);
}