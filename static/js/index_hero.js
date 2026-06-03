document.addEventListener('DOMContentLoaded', function () {

    // ── Hero Slider ──────────────────────────────────────────────
    const slides      = document.querySelectorAll('.hero-slide');
    const bgSlides    = document.querySelectorAll('.background-slide');
    const dots        = document.querySelectorAll('.dot');
    let current       = 0;
    let autoplayTimer = null;

    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.style.opacity = i === index ? '1' : '0';
            slide.style.zIndex  = i === index ? '10' : '1';
        });
        bgSlides.forEach((bg, i) => {
            bg.style.opacity = i === index ? '1' : '0';
        });
        dots.forEach((dot, i) => {
            dot.classList.toggle('bg-white',    i === index);
            dot.classList.toggle('scale-125',   i === index);
            dot.classList.toggle('bg-white/60', i !== index);
        });
        current = index;
    }

    function startAutoplay() {
        stopAutoplay();
        autoplayTimer = setInterval(() => {
            showSlide((current + 1) % slides.length);
        }, 5000);
    }

    function stopAutoplay() {
        clearInterval(autoplayTimer);
    }

    // Dot clicks — reset timer so interval doesn't immediately override
    dots.forEach((dot, i) => {
        dot.addEventListener('click', () => {
            showSlide(i);
            startAutoplay();
        });
    });

    // Pause on hover, resume on leave
    const heroSection = document.querySelector('.hero-slide')?.closest('section');
    if (heroSection) {
        heroSection.addEventListener('mouseenter', stopAutoplay);
        heroSection.addEventListener('mouseleave', startAutoplay);
    }

    // Swipe support for mobile
    let touchStartX = 0;
    document.addEventListener('touchstart', e => {
        touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });
    document.addEventListener('touchend', e => {
        const diff = touchStartX - e.changedTouches[0].screenX;
        if (Math.abs(diff) > 50) {
            const direction = diff > 0 ? 1 : -1;
            showSlide((current + direction + slides.length) % slides.length);
            startAutoplay();
        }
    }, { passive: true });

    // ── Parallax (additive — doesn't break CSS animations) ───────
    document.addEventListener('mousemove', (e) => {
        const x = (e.clientX / window.innerWidth  - 0.5) * 20;
        const y = (e.clientY / window.innerHeight - 0.5) * 20;

        document.querySelectorAll('.background-slide .fas').forEach(el => {
            // Preserve existing transform by using CSS custom properties instead
            el.style.setProperty('--px', `${x}px`);
            el.style.setProperty('--py', `${y}px`);
        });
    });

    // ── Floating Labels ──────────────────────────────────────────
    function checkValue(input, label) {
        const hasValue = input.value !== '';
        const isFocused = document.activeElement === input;
        label.classList.toggle('active', hasValue || isFocused);
    }

    document.querySelectorAll('.floating-label-group').forEach(group => {
        const input = group.querySelector('input, select, textarea');
        const label = group.querySelector('.floating-label');
        if (!input || !label) return;

        checkValue(input, label); // initial state

        input.addEventListener('focus',  () => label.classList.add('active'));
        input.addEventListener('blur',   () => checkValue(input, label));
        input.addEventListener('input',  () => checkValue(input, label));
        input.addEventListener('change', () => checkValue(input, label));
    });

    // ── Init ─────────────────────────────────────────────────────
    showSlide(0);
    startAutoplay();
});