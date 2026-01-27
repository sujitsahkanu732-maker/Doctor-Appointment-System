/**
 * Doctor Appointment System - JavaScript
 * Client-side validation and interactive features
 */

// ==================== FORM VALIDATION ====================

/**
 * Validate registration form
 */
function validateRegistrationForm() {
    const username = document.getElementById('username').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm_password').value;
    const fullName = document.getElementById('full_name').value.trim();
    
    // Check if all fields are filled
    if (!username || !email || !password || !confirmPassword || !fullName) {
        showAlert('Please fill in all required fields!', 'danger');
        return false;
    }
    
    // Validate username (alphanumeric, 3-20 characters)
    const usernameRegex = /^[a-zA-Z0-9_]{3,20}$/;
    if (!usernameRegex.test(username)) {
        showAlert('Username must be 3-20 characters and contain only letters, numbers, and underscores!', 'danger');
        return false;
    }
    
    // Validate email
    if (!validateEmail(email)) {
        showAlert('Please enter a valid email address!', 'danger');
        return false;
    }
    
    // Validate password length
    if (password.length < 8) {
        showAlert('Password must be at least 8 characters long!', 'danger');
        return false;
    }
    
    // Check password strength
    if (!validatePasswordStrength(password)) {
        showAlert('Password must contain at least one uppercase letter, one lowercase letter, and one number!', 'warning');
        return false;
    }
    
    // Check if passwords match
    if (password !== confirmPassword) {
        showAlert('Passwords do not match!', 'danger');
        return false;
    }
    
    // If user type is doctor, validate doctor fields
    const userType = document.getElementById('user_type').value;
    if (userType === 'doctor') {
        const specialization = document.getElementById('specialization')?.value.trim();
        const qualification = document.getElementById('qualification')?.value.trim();
        const consultationFee = document.getElementById('consultation_fee')?.value;
        
        if (!specialization || !qualification || !consultationFee) {
            showAlert('Please fill in all doctor-specific fields!', 'danger');
            return false;
        }
        
        if (parseFloat(consultationFee) <= 0) {
            showAlert('Consultation fee must be greater than 0!', 'danger');
            return false;
        }
    }
    
    return true;
}

/**
 * Validate login form
 */
function validateLoginForm() {
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;
    
    if (!username || !password) {
        showAlert('Please enter both username and password!', 'danger');
        return false;
    }
    
    if (username.length < 3) {
        showAlert('Please enter a valid username!', 'danger');
        return false;
    }
    
    if (password.length < 8) {
        showAlert('Please enter a valid password!', 'danger');
        return false;
    }
    
    return true;
}

/**
 * Validate appointment booking form
 */
function validateAppointmentForm() {
    const appointmentDate = document.getElementById('appointment_date').value;
    const appointmentTime = document.getElementById('appointment_time').value;
    const reason = document.getElementById('reason').value.trim();
    
    if (!appointmentDate || !appointmentTime || !reason) {
        showAlert('Please fill in all fields!', 'danger');
        return false;
    }
    
    // Check if date is in the future
    const selectedDate = new Date(appointmentDate);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    if (selectedDate < today) {
        showAlert('Please select a future date!', 'danger');
        return false;
    }
    
    // Check if reason is at least 10 characters
    if (reason.length < 10) {
        showAlert('Please provide a detailed reason (at least 10 characters)!', 'warning');
        return false;
    }
    
    return true;
}

/**
 * Validate profile edit form
 */
function validateProfileForm() {
    const fullName = document.getElementById('full_name').value.trim();
    const email = document.getElementById('email').value.trim();
    const phone = document.getElementById('phone')?.value.trim();
    
    if (!fullName || !email) {
        showAlert('Full name and email are required!', 'danger');
        return false;
    }
    
    if (!validateEmail(email)) {
        showAlert('Please enter a valid email address!', 'danger');
        return false;
    }
    
    if (phone && phone.length < 10) {
        showAlert('Please enter a valid phone number!', 'danger');
        return false;
    }
    
    return true;
}

// ==================== VALIDATION HELPER FUNCTIONS ====================

/**
 * Validate email format
 */
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Validate password strength
 */
function validatePasswordStrength(password) {
    // Check for at least one uppercase, one lowercase, and one number
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    
    return hasUpperCase && hasLowerCase && hasNumber;
}

/**
 * Show password strength indicator
 */
function showPasswordStrength(password) {
    const strengthBar = document.getElementById('password-strength');
    if (!strengthBar) return;
    
    let strength = 0;
    
    if (password.length >= 8) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^a-zA-Z0-9]/.test(password)) strength++;
    
    const strengthTexts = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong'];
    const strengthColors = ['#ef4444', '#f59e0b', '#eab308', '#10b981', '#059669'];
    
    strengthBar.style.width = (strength * 20) + '%';
    strengthBar.style.backgroundColor = strengthColors[strength - 1] || '#ef4444';
    strengthBar.textContent = strengthTexts[strength - 1] || 'Very Weak';
}

// ==================== INTERACTIVE FEATURES ====================

/**
 * Show/hide doctor-specific fields based on user type selection
 */
function toggleDoctorFields() {
    const userType = document.getElementById('user_type')?.value;
    const doctorFields = document.getElementById('doctor-fields');
    
    if (doctorFields) {
        if (userType === 'doctor') {
            doctorFields.style.display = 'block';
            // Make doctor fields required
            document.getElementById('specialization').required = true;
            document.getElementById('qualification').required = true;
            document.getElementById('consultation_fee').required = true;
        } else {
            doctorFields.style.display = 'none';
            // Remove required attribute
            if (document.getElementById('specialization')) {
                document.getElementById('specialization').required = false;
                document.getElementById('qualification').required = false;
                document.getElementById('consultation_fee').required = false;
            }
        }
    }
}

/**
 * Show alert message
 */
function showAlert(message, type = 'info') {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Insert at the top of the page
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
}

/**
 * Confirm action before proceeding
 */
function confirmAction(message) {
    return confirm(message);
}

/**
 * Confirm appointment cancellation
 */
function confirmCancellation() {
    return confirm('Are you sure you want to cancel this appointment?');
}

/**
 * Set minimum date for appointment booking (today)
 */
function setMinimumDate() {
    const dateInput = document.getElementById('appointment_date');
    if (dateInput) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.setAttribute('min', today);
    }
}

/**
 * Auto-dismiss alerts after 5 seconds
 */
function autoDismissAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const closeButton = alert.querySelector('.btn-close');
            if (closeButton) {
                closeButton.click();
            }
        }, 5000);
    });
}

/**
 * Smooth scroll to top
 */
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

/**
 * Format phone number as user types
 */
function formatPhoneNumber(input) {
    let value = input.value.replace(/\D/g, '');
    if (value.length > 10) {
        value = value.slice(0, 10);
    }
    input.value = value;
}

/**
 * Update character count for textarea
 */
function updateCharacterCount(textarea, counterId) {
    const counter = document.getElementById(counterId);
    if (counter) {
        const currentLength = textarea.value.length;
        counter.textContent = `${currentLength} characters`;
    }
}

// ==================== SEARCH AND FILTER ====================

/**
 * Search/filter doctors by name or specialization
 */
function searchDoctors() {
    const searchInput = document.getElementById('doctor-search')?.value.toLowerCase();
    if (!searchInput) return;
    
    const doctorCards = document.querySelectorAll('.doctor-card');
    
    doctorCards.forEach(card => {
        const doctorName = card.querySelector('h4')?.textContent.toLowerCase() || '';
        const specialization = card.querySelector('.doctor-specialization')?.textContent.toLowerCase() || '';
        
        if (doctorName.includes(searchInput) || specialization.includes(searchInput)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

/**
 * Filter appointments by status
 */
function filterAppointments(status) {
    const appointmentRows = document.querySelectorAll('.appointment-row');
    
    appointmentRows.forEach(row => {
        const appointmentStatus = row.dataset.status?.toLowerCase();
        
        if (status === 'all' || appointmentStatus === status.toLowerCase()) {
            row.style.display = 'table-row';
        } else {
            row.style.display = 'none';
        }
    });
}

// ==================== EVENT LISTENERS ====================

document.addEventListener('DOMContentLoaded', function() {
    // Set minimum date for appointment booking
    setMinimumDate();
    
    // Auto-dismiss alerts
    autoDismissAlerts();
    
    // Toggle doctor fields on page load
    toggleDoctorFields();
    
    // Add event listener for user type selection
    const userTypeSelect = document.getElementById('user_type');
    if (userTypeSelect) {
        userTypeSelect.addEventListener('change', toggleDoctorFields);
    }
    
    // Add event listener for password strength
    const passwordInput = document.getElementById('password');
    if (passwordInput) {
        passwordInput.addEventListener('input', function() {
            showPasswordStrength(this.value);
        });
    }
    
    // Add event listener for phone number formatting
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function() {
            formatPhoneNumber(this);
        });
    });
    
    // Add event listener for doctor search
    const searchInput = document.getElementById('doctor-search');
    if (searchInput) {
        searchInput.addEventListener('input', searchDoctors);
    }
    
    // Add smooth scroll for back-to-top button
    const backToTopBtn = document.getElementById('back-to-top');
    if (backToTopBtn) {
        backToTopBtn.addEventListener('click', scrollToTop);
        
        // Show/hide back-to-top button based on scroll position
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopBtn.style.display = 'block';
            } else {
                backToTopBtn.style.display = 'none';
            }
        });
    }
});

// ==================== AJAX FUNCTIONS (Optional Enhancement) ====================

/**
 * Check username availability (could be used with AJAX)
 */
async function checkUsernameAvailability(username) {
    // This would typically make an AJAX call to the server
    // For now, it's a placeholder for future enhancement
    console.log('Checking username:', username);
}

/**
 * Load available time slots for selected doctor and date
 */
async function loadAvailableTimeSlots(doctorId, date) {
    // This would typically make an AJAX call to the server
    // For now, it's a placeholder for future enhancement
    console.log('Loading time slots for doctor:', doctorId, 'on', date);
}

// ==================== EXPORT FUNCTIONS ====================
// Make functions available globally
window.validateRegistrationForm = validateRegistrationForm;
window.validateLoginForm = validateLoginForm;
window.validateAppointmentForm = validateAppointmentForm;
window.validateProfileForm = validateProfileForm;
window.confirmCancellation = confirmCancellation;
window.confirmAction = confirmAction;
window.toggleDoctorFields = toggleDoctorFields;
window.filterAppointments = filterAppointments;