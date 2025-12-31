const testimonials = [
  {
    name: "Pasang Lama",
    image: "static/images/stories/one.jpeg",
    quote: "I got my visa approved for Australia thanks to the consultancy's amazing support and guidance!",
    university: "University of East London, UK",
    course: "MSc in Data Science",
    intake: "January Intake 2026",
    borderColor: "border-blue-500",
    textColor: "text-blue-700 dark:text-blue-300"
  },
  {
    name: "Renjina Pariyar",
    image: "static/images/stories/two.jpeg",
    quote: "My dream of studying in Canada came true — very professional guidance throughout the process!",
    university: "BPP University",
    course: "BSc in Social Health Care",
    intake: "September Intake 2025",
    borderColor: "border-green-500",
    textColor: "text-green-700 dark:text-green-300"
  },
  {
    name: "Abdul Hamid",
    image: "static/images/stories/three.jpeg",
    quote: "The IELTS classes and document help made my UK process incredibly smooth and stress-free.",
    university: "University of East London, UK",
    course: "BSc in Computer Science",
    intake: "September Intake 2025",
    borderColor: "border-red-500",
    textColor: "text-red-700 dark:text-red-300"
  },
  {
    name: "Pratima Maharjan",
    image: "static/images/stories/four.jpeg",
    quote: "I got my visa approved for Australia thanks to the consultancy's amazing support and guidance!",
    university: "Charles Darwin University",
    course: "Master by Research in Business",
    intake: "August Intake 2025",
    borderColor: "border-indigo-500",
    textColor: "text-indigo-700 dark:text-indigo-300"
  },
  {
    name: "Sushmita Rokaya",
    image: "static/images/stories/five.jpeg",
    quote: "I got my visa approved for Australia thanks to the consultancy's amazing support and guidance!",
    university: "La Trobe University",
    course: "Masters in Health Administration",
    intake: "July Intake 2025",
    borderColor: "border-teal-500",
    textColor: "text-teal-700 dark:text-teal-300"
  }
];

document.addEventListener('DOMContentLoaded', function() {
    const slider = document.getElementById('testimonial-slider');
  const prevBtn = document.getElementById('prev-testimonial');
  const nextBtn = document.getElementById('next-testimonial');
  
  // Triple the testimonials for infinite scroll
  const allTestimonials = [...testimonials, ...testimonials, ...testimonials];
  let currentIndex = testimonials.length; // Start at the middle set
  const cardWidth = window.innerWidth < 768 ? 352 : 412; // 320/380 + gap
  let isTransitioning = false;
  
  // Generate testimonial cards
  function generateCards() {
    slider.innerHTML = allTestimonials.map(t => `
      <div class="testimonial-card min-w-[320px] md:min-w-[380px] bg-white dark:bg-gray-800 p-8 rounded-3xl shadow-xl border border-gray-100 dark:border-gray-700">
        <div class="relative mb-6">
          <div class="profile-img-wrapper w-24 h-24 mx-auto rounded-full overflow-hidden border-4 ${t.borderColor} shadow-lg">
            <img src="${t.image}" alt="${t.name}" class="w-full h-full object-cover">
          </div>
          <div class="absolute -bottom-2 right-1/2 transform translate-x-1/2 bg-green-500 text-white rounded-full p-2 shadow-lg">
            <i class="fas fa-check text-sm"></i>
          </div>
        </div>
        <div class="flex justify-center text-yellow-400 mb-4">
          <i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i>
        </div>
        <p class="text-gray-800 dark:text-gray-200 italic mb-6 leading-relaxed text-center min-h-[80px]">
          "${t.quote}"
        </p>
        <div class="mt-auto">
          <h3 class="font-bold text-xl text-gray-900 dark:text-white mb-2">${t.name}</h3>
          <div class="space-y-1">
            <span class="block text-sm font-semibold ${t.textColor}">${t.university}</span>
            <span class="block text-sm ${t.textColor.replace('700', '600').replace('300', '400')}">${t.course}</span>
            <span class="block text-sm ${t.textColor.replace('700', '600').replace('300', '400')}">${t.intake}</span>
          </div>
        </div>
      </div>
    `).join('');
  }
  
  function updateSlider(smooth = true) {
    if (!smooth) {
      slider.style.transition = 'none';
    }
    const offset = -currentIndex * cardWidth;
    slider.style.transform = `translateX(${offset}px)`;
    
    if (!smooth) {
      setTimeout(() => {
        slider.style.transition = 'transform 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
      }, 50);
    }
  }
  
  function handleTransitionEnd() {
    isTransitioning = false;
    
    // Reset to middle set for infinite loop
    if (currentIndex >= testimonials.length * 2) {
      currentIndex = testimonials.length;
      updateSlider(false);
    } else if (currentIndex < testimonials.length) {
      currentIndex = testimonials.length * 2 - 1;
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
  
  // Pause on hover
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
  
  // Initialize
  generateCards();
  updateSlider(false);
});