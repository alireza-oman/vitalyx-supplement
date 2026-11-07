document.addEventListener('DOMContentLoaded', () => {
    // 1. Password Visibility Toggle
    const toggleButtons = document.querySelectorAll('.toggle-password');

    toggleButtons.forEach(button => {
        button.addEventListener('click', () => {
            const wrapper = button.closest('.input-wrapper');
            const passwordInput = wrapper.querySelector('.form-input');
            const icon = button.querySelector('i');

            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                icon.className = 'bx bx-show';
            } else {
                passwordInput.type = 'password';
                icon.className = 'bx bx-hide';
            }
        });
    });

    // 2. Prevent Multiple Form Submissions & Show Loading State
    const authForm = document.querySelector('.auth-form');
    if (authForm) {
        authForm.addEventListener('submit', function () {
            const submitBtn = this.querySelector('.auth-submit-btn');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.style.opacity = '0.7';
                submitBtn.style.cursor = 'not-allowed';
                submitBtn.value = 'Please wait...';
            }
        });
    }
});