(function () {
    const toggleBtn = document.getElementById('admin-theme-toggle');
    const themeIcon = document.getElementById('admin-theme-icon');
    const html = document.documentElement;

    const savedTheme = localStorage.getItem('vitalyx_admin_theme') || 'dark';
    html.setAttribute('data-theme', savedTheme);
    updateIcon(savedTheme);

    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            const currentTheme = html.getAttribute('data-theme') || 'dark';
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('vitalyx_admin_theme', newTheme);
            updateIcon(newTheme);
        });
    }

    function updateIcon(theme) {
        if (!themeIcon) return;
        themeIcon.className = theme === 'dark' ? 'bx bx-sun' : 'bx bx-moon';
    }
})();