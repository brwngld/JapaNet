document.addEventListener('DOMContentLoaded', function() {
    const passwordField = document.getElementById('password');
    const confirmPasswordField = document.getElementById('confirm_password');
    const strengthBadge = document.getElementById('password-strength');
    const passwordMessage = document.getElementById('password-message');
    const togglePasswordButton = document.getElementById('toggle-password');
    const toggleConfirmPasswordButton = document.getElementById('toggle-confirm-password');

    function calculatePasswordStrength(password) {
        const containsUppercase = /[A-Z]/.test(password);
        const containsSymbol = /[\W_]/.test(password);

        if (password.length < 8 || !containsUppercase || !containsSymbol) {
            return 'Weak';
        } else if (password.length < 12) {
            return 'Moderate';
        } else {
            return 'Strong';
        }
    }

    function updatePasswordStrengthIndicator() {
        const password = passwordField.value;
        const strength = calculatePasswordStrength(password);

        strengthBadge.textContent = 'Password Strength: ' + strength.toUpperCase();
        strengthBadge.className = 'text-' + (strength === 'Weak' ? 'danger' : (strength === 'Moderate' ? 'warning' : 'success'));

        if (strength === 'Weak') {
            passwordMessage.textContent = 'Password should contain at least one uppercase letter and one symbol.';
            passwordMessage.style.display = 'block';
        } else {
            passwordMessage.style.display = 'none';
        }
    }

    function togglePasswordVisibility(field, toggleButton) {
        const type = field.getAttribute('type') === 'password' ? 'text' : 'password';
        field.setAttribute('type', type);
        toggleButton.querySelector('i').className = type === 'password' ? 'fa fa-eye' : 'fa fa-eye-slash';
    }

    passwordField.addEventListener('input', updatePasswordStrengthIndicator);
    confirmPasswordField.addEventListener('input', updatePasswordStrengthIndicator);

    togglePasswordButton.addEventListener('click', function() {
        togglePasswordVisibility(passwordField, togglePasswordButton);
    });

    toggleConfirmPasswordButton.addEventListener('click', function() {
        togglePasswordVisibility(confirmPasswordField, toggleConfirmPasswordButton);
    });
});
