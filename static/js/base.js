AOS.init({
    duration: 800,
    once: true,
});

document.addEventListener("DOMContentLoaded", function() {
    const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
    const mobileMenu = document.getElementById('mobile-menu');
    const menuIcon = document.getElementById('menu-icon');

    // Mobile Menu Toggle with animation
    mobileMenuToggle.addEventListener('click', () => {
        if (mobileMenu.style.maxHeight && mobileMenu.style.maxHeight !== "0px") {
            mobileMenu.style.maxHeight = "0px";
            mobileMenu.style.paddingTop = "0";
            mobileMenu.style.paddingBottom = "0";
            menuIcon.classList.replace('fa-times', 'fa-bars');
        } else {
            mobileMenu.style.maxHeight = mobileMenu.scrollHeight + "px";
            mobileMenu.style.paddingTop = "1rem";
            mobileMenu.style.paddingBottom = "1rem";
            menuIcon.classList.replace('fa-bars', 'fa-times');
            mobileMenu.classList.add('mobile-menu-enter');
        }
    });

    // Add scroll effect to header
    let lastScroll = 0;
    const header = document.querySelector('header');
    
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll <= 0) {
            header.style.boxShadow = 'none';
        } else {
            header.style.boxShadow = '0 4px 20px rgba(0,0,0,0.1)';
        }
        
        lastScroll = currentScroll;
    });

    // Add hover effects to navigation items
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.color = '#41A67E';
        });
        item.addEventListener('mouseleave', function() {
            this.style.color = '';
        });
    });
});