AOS.init({
    duration: 800,
    once: true,
});

document.addEventListener("DOMContentLoaded", function () {

    // ── Mobile menu ──────────────────────────────────────────────
    const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
    const mobileMenu = document.getElementById('mobile-menu');
    const menuIcon = document.getElementById('menu-icon');
    let mobileMenuOpen = false;
    let closeTimer = null;

    const openMobileMenu = () => {
        // Cancel any in-progress close
        clearTimeout(closeTimer);
        mobileMenuOpen = true;

        // 1. Make the element participate in layout BEFORE measuring
        mobileMenu.classList.remove('hidden');

        // 2. Force a reflow so the browser registers the element, then animate
        requestAnimationFrame(() => {
            mobileMenu.style.maxHeight = mobileMenu.scrollHeight + 'px';
            mobileMenu.style.paddingTop = '0.5rem';
            mobileMenu.style.paddingBottom = '1rem';
            mobileMenu.style.overflowY = 'auto';
        });

        menuIcon.classList.replace('fa-bars', 'fa-times');
        mobileMenuToggle.setAttribute('aria-expanded', 'true');
    };

    const closeMobileMenu = () => {
        mobileMenuOpen = false;

        mobileMenu.style.maxHeight = '0px';
        mobileMenu.style.paddingTop = '0';
        mobileMenu.style.paddingBottom = '0';

        menuIcon.classList.replace('fa-times', 'fa-bars');
        mobileMenuToggle.setAttribute('aria-expanded', 'false');

        // Only hide after the CSS transition finishes (matches your duration-500)
        closeTimer = setTimeout(() => {
            if (!mobileMenuOpen) {
                mobileMenu.classList.add('hidden');
            }
        }, 500);
    };

    mobileMenuToggle.addEventListener('click', () => {
        mobileMenuOpen ? closeMobileMenu() : openMobileMenu();
    });

    // Close on resize to desktop
    window.addEventListener('resize', () => {
        if (window.innerWidth >= 768 && mobileMenuOpen) {
            closeMobileMenu();
        }
    });

    // ── Scroll shadow on header ──────────────────────────────────
    const header = document.querySelector('header');

    window.addEventListener('scroll', () => {
        header.style.boxShadow = window.pageYOffset > 0
            ? '0 4px 20px rgba(0,0,0,0.1)'
            : 'none';
    });

    // ── Nav hover effects ────────────────────────────────────────
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('mouseenter', () => item.style.color = '#41A67E');
        item.addEventListener('mouseleave', () => item.style.color = '');
    });

});