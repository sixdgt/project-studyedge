  // Hero Slider with Background Sync
  const slides = document.querySelectorAll('.hero-slide');
  const backgroundSlides = document.querySelectorAll('.background-slide');
  const dots = document.querySelectorAll('.dot');
  let current = 0;

  function showSlide(index) {
    // Update hero slides
    slides.forEach((slide, i) => {
      slide.style.opacity = i === index ? '1' : '0';
      slide.style.zIndex = i === index ? '10' : '1';
    });
    
    // Update background slides
    backgroundSlides.forEach((bgSlide, i) => {
      bgSlide.style.opacity = i === index ? '1' : '0';
    });
    
    // Update dots
    dots.forEach((dot, i) => {
      if (i === index) {
        dot.classList.remove('bg-white/60');
        dot.classList.add('bg-white', 'scale-125');
      } else {
        dot.classList.remove('bg-white', 'scale-125');
        dot.classList.add('bg-white/60');
      }
    });
    current = index;
  }

  dots.forEach((dot, i) => {
    dot.addEventListener('click', () => showSlide(i));
  });

  // Auto slide every 5 seconds
  setInterval(() => {
    let next = (current + 1) % slides.length;
    showSlide(next);
  }, 5000);

  // Initialize
  showSlide(0);

  // Add mouse move parallax effect
  document.addEventListener('mousemove', (e) => {
    const x = (e.clientX / window.innerWidth - 0.5) * 20;
    const y = (e.clientY / window.innerHeight - 0.5) * 20;
    
    const floatElements = document.querySelectorAll('.background-slide .fas');
    floatElements.forEach(el => {
      el.style.transform = `translate(${x}px, ${y}px)`;
    });
});

// for floating fields
document.addEventListener('DOMContentLoaded', function() {
  const floatingGroups = document.querySelectorAll('.floating-label-group');
  
  floatingGroups.forEach(group => {
    const input = group.querySelector('input, select, textarea');
    const label = group.querySelector('.floating-label');
    
    if (input && label) {
      // Check on load if field has value
      checkValue();
      
      // Check on input/change
      input.addEventListener('input', checkValue);
      input.addEventListener('change', checkValue);
      input.addEventListener('focus', () => label.classList.add('active'));
      input.addEventListener('blur', checkValue);
      
      function checkValue() {
        if (input.value !== '' || document.activeElement === input) {
          label.classList.add('active');
        } else {
          label.classList.remove('active');
        }
      }
    }
  });
});