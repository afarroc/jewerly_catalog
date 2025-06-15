// Mobile menu toggle
document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const mainNav = document.querySelector('.main-nav');
    
    if (mobileMenuBtn && mainNav) {
        mobileMenuBtn.addEventListener('click', function() {
            mainNav.style.display = mainNav.style.display === 'flex' ? 'none' : 'flex';
        });
    }
    
    // Quantity selector functionality
    document.querySelectorAll('.qty-btn').forEach(button => {
        button.addEventListener('click', function() {
            const input = this.parentNode.querySelector('input[type=number]');
            if (this.classList.contains('minus')) {
                input.stepDown();
            } else if (this.classList.contains('plus')) {
                input.stepUp();
            }
        });
    });
    
    // Handle window resize for menu
    window.addEventListener('resize', function() {
        if (window.innerWidth > 992) {
            if (mainNav) mainNav.style.display = 'flex';
        } else {
            if (mainNav) mainNav.style.display = 'none';
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Password strength indicator
    const password1 = document.getElementById('id_new_password1');
    const passwordStrength = document.querySelector('.password-strength');
    const passwordCriteria = document.querySelector('.password-criteria');
    
    if (password1) {
        // Create password strength meter if it doesn't exist
        if (!passwordStrength) {
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
            password1.parentNode.insertBefore(strengthMeter, password1.nextSibling);
        }
        
        // Create password criteria list if it doesn't exist
        if (!passwordCriteria) {
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
            password1.parentNode.insertBefore(criteriaList, passwordStrength.nextSibling);
        }
        
        password1.addEventListener('input', updatePasswordStrength);
    }
    
    function updatePasswordStrength() {
        const password = this.value;
        const strengthBars = document.querySelectorAll('.password-strength span');
        const strengthText = document.querySelector('.strength-text');
        const criteriaItems = document.querySelectorAll('.password-criteria li');
        
        // Reset all bars
        strengthBars.forEach(bar => {
            bar.className = '';
        });
        
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
            if (i < 2) {
                strengthBars[i].className = 'weak';
            } else if (i < 4) {
                strengthBars[i].className = 'medium';
            } else {
                strengthBars[i].className = 'strong';
            }
        }
        
        // Update strength text
        if (password.length === 0) {
            strengthText.textContent = '';
        } else if (strength <= 2) {
            strengthText.textContent = 'Weak';
            strengthText.style.color = 'var(--danger-color)';
        } else if (strength <= 4) {
            strengthText.textContent = 'Medium';
            strengthText.style.color = 'var(--warning-color)';
        } else {
            strengthText.textContent = 'Strong';
            strengthText.style.color = 'var(--success-color)';
        }
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.checkout-form');
    const placeOrderBtn = document.getElementById('place-order-btn');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            if (!document.getElementById('agree-terms').checked) {
                e.preventDefault();
                alert('Debes aceptar los términos y condiciones para continuar');
                return false;
            }
            
            // Deshabilitar botón para evitar doble envío
            placeOrderBtn.disabled = true;
            placeOrderBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Procesando...';
        });
        
        // Mostrar/ocultar dirección de facturación
        const billingOptions = document.querySelectorAll('input[name="billing_option"]');
        const billingSection = document.getElementById('billing-address-section');
        
        billingOptions.forEach(option => {
            option.addEventListener('change', function() {
                billingSection.style.display = this.value === 'different' ? 'block' : 'none';
            });
        });
    }
});