document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const inputs = form.querySelectorAll('.form-input-peer');
    
    // Real-time validation
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            validateField(this);
        });
        
        input.addEventListener('blur', function() {
            validateField(this);
        });
    });
    
    function validateField(field) {
        field.classList.remove('valid', 'invalid');
        
        if (field.value.trim() === '') return;
        
        if (field.checkValidity()) {
            field.classList.add('valid');
        } else {
            field.classList.add('invalid');
        }
    }
    
    // Form submission with loading animation
    form.addEventListener('submit', function(e) {
        const submitBtn = form.querySelector('.submit-btn');
        const spinner = form.querySelector('.loading-spinner');
        
        if (spinner) {
            submitBtn.disabled = true;
            spinner.style.display = 'inline-block';
        }
    });
    
    // Add date picker restrictions
    const dateInput = document.getElementById('preferred-date');
    if (dateInput) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.min = today;
        
        // Add max date (1 year from now)
        const maxDate = new Date();
        maxDate.setFullYear(maxDate.getFullYear() + 1);
        dateInput.max = maxDate.toISOString().split('T')[0];
    }
    
    // Add character counter for text inputs
    const textInputs = form.querySelectorAll('input[type="text"]');
    textInputs.forEach(input => {
        const counter = document.createElement('div');
        counter.className = 'text-gray-400 text-xs mt-1 text-right';
        input.parentNode.appendChild(counter);
        
        input.addEventListener('input', function() {
            const maxLength = this.maxLength || 100;
            const currentLength = this.value.length;
            counter.textContent = `${currentLength}/${maxLength}`;
            counter.style.color = currentLength > maxLength * 0.8 ? '#ef4444' : '#9ca3af';
        });
    });
});