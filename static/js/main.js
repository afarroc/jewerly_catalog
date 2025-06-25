// Mobile menu toggle and general DOM setup
document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const mainNav = document.querySelector('.main-nav');
    
    if (mobileMenuBtn && mainNav) {
        mobileMenuBtn.addEventListener('click', function() {
            mainNav.style.display = mainNav.style.display === 'flex' ? 'none' : 'flex';
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!mainNav.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
                mainNav.style.display = 'none';
            }
        });
    }
    
    // Responsive menu handling
    window.addEventListener('resize', function() {
        if (window.innerWidth > 992) {
            if (mainNav) mainNav.style.display = 'flex';
        } else {
            if (mainNav) mainNav.style.display = 'none';
        }
    });

    // Quantity selector functionality
    document.querySelectorAll('.qty-btn').forEach(button => {
        button.addEventListener('click', function() {
            const input = this.parentNode.querySelector('input[type=number]');
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

// Password strength meter initialization
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

// Checkout form initialization
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
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}