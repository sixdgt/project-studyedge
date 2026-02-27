document.addEventListener('DOMContentLoaded', function () {
  const slider = document.getElementById('testimonial-slider');
  const prevBtn = document.getElementById('prev-testimonial');
  const nextBtn = document.getElementById('next-testimonial');

  const cards = Array.from(slider.children);
  const totalCards = cards.length;

  // 🔥 Clone cards for infinite effect
  cards.forEach(card => {
    const clone = card.cloneNode(true);
    slider.appendChild(clone);
  });

  cards.forEach(card => {
    const clone = card.cloneNode(true);
    slider.insertBefore(clone, slider.firstChild);
  });

  let currentIndex = totalCards; // Start from middle
  const cardWidth = slider.children[0].offsetWidth + 32; // 32 = gap-8
  let isTransitioning = false;

  function updateSlider(smooth = true) {
    if (!smooth) slider.style.transition = 'none';

    slider.style.transform = `translateX(-${currentIndex * cardWidth}px)`;

    if (!smooth) {
      setTimeout(() => {
        slider.style.transition =
          'transform 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
      }, 50);
    }
  }

  function handleTransitionEnd() {
    isTransitioning = false;

    if (currentIndex >= totalCards * 2) {
      currentIndex = totalCards;
      updateSlider(false);
    } else if (currentIndex < totalCards) {
      currentIndex = totalCards * 2 - 1;
      updateSlider(false);
    }
  }

  nextBtn.addEventListener('click', () => {
    if (isTransitioning) return;
    isTransitioning = true;
    currentIndex++;
    updateSlider();
  });

  prevBtn.addEventListener('click', () => {
    if (isTransitioning) return;
    isTransitioning = true;
    currentIndex--;
    updateSlider();
  });

  slider.addEventListener('transitionend', handleTransitionEnd);

  // Auto-scroll
  let autoScroll = setInterval(() => {
    if (!isTransitioning) {
      isTransitioning = true;
      currentIndex++;
      updateSlider();
    }
  }, 4000);

  slider.parentElement.addEventListener('mouseenter', () => {
    clearInterval(autoScroll);
  });

  slider.parentElement.addEventListener('mouseleave', () => {
    autoScroll = setInterval(() => {
      if (!isTransitioning) {
        isTransitioning = true;
        currentIndex++;
        updateSlider();
      }
    }, 4000);
  });

  updateSlider(false);
});