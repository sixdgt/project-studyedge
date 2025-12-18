// Date restriction JavaScript for booking forms
document.addEventListener('DOMContentLoaded', function() {
    const dateInput = document.getElementById('preferred-date');
    
    if (dateInput) {
        // Set minimum date to tomorrow (block today and previous dates)
        const today = new Date();
        const tomorrow = new Date(today);
        tomorrow.setDate(tomorrow.getDate() + 1);
        
        // Format to YYYY-MM-DD
        const minDate = tomorrow.toISOString().split('T')[0];
        dateInput.min = minDate;
        
        // Set maximum date to 6 months from now (consultant availability)
        const maxDate = new Date(today);
        maxDate.setMonth(maxDate.getMonth() + 6);
        const maxDateFormatted = maxDate.toISOString().split('T')[0];
        dateInput.max = maxDateFormatted;
        
        // Block weekends (Saturday and Sunday)
        dateInput.addEventListener('input', function(e) {
            const selectedDate = new Date(this.value);
            const dayOfWeek = selectedDate.getDay(); // 0 = Sunday, 6 = Saturday
            
            if (dayOfWeek === 0 || dayOfWeek === 6) {
                alert('Bookings are not available on weekends. Please select a weekday (Monday-Friday).');
                this.value = '';
                
                // Suggest next available weekday
                const nextWeekday = new Date(selectedDate);
                if (dayOfWeek === 6) { // Saturday
                    nextWeekday.setDate(nextWeekday.getDate() + 2); // Monday
                } else if (dayOfWeek === 0) { // Sunday
                    nextWeekday.setDate(nextWeekday.getDate() + 1); // Monday
                }
                
                // Ensure it's within max date
                if (nextWeekday <= new Date(maxDateFormatted)) {
                    this.value = nextWeekday.toISOString().split('T')[0];
                }
            }
        });
        
        // Block specific blackout dates (holidays, consultant unavailability)
        const blackoutDates = [
            '2024-12-25', // Christmas
            '2025-01-01', // New Year
            '2025-01-15', // Maghe Sankranti
            '2025-02-19', // Shivaratri
            '2025-03-08', // International Women's Day
            // Add more blackout dates as needed
        ];
        
        dateInput.addEventListener('change', function(e) {
            const selectedDate = this.value;
            
            // Check if date is in blackout list
            if (blackoutDates.includes(selectedDate)) {
                alert('Bookings are not available on this date due to holiday/unavailability. Please select another date.');
                this.value = '';
                return;
            }
            
            // Check if date is too far in advance (more than 3 months for PTE)
            const testType = document.getElementById('test-type');
            if (testType && testType.value.toLowerCase().includes('pte')) {
                const threeMonthsFromNow = new Date(today);
                threeMonthsFromNow.setMonth(threeMonthsFromNow.getMonth() + 3);
                
                if (new Date(selectedDate) > threeMonthsFromNow) {
                    alert('PTE test bookings are only available up to 3 months in advance. Please select an earlier date.');
                    this.value = '';
                    return;
                }
            }
        });
        
        // Add custom date picker UI improvements
        dateInput.addEventListener('focus', function() {
            // Show a custom calendar guide
            showDateGuide();
        });
        
        function showDateGuide() {
            // Remove existing guide if present
            const existingGuide = document.getElementById('date-guide');
            if (existingGuide) existingGuide.remove();
            
            // Create guide element
            const guide = document.createElement('div');
            guide.id = 'date-guide';
            guide.className = 'mt-2 p-3 bg-blue-50 border border-blue-200 rounded-lg text-sm';
            
            const today = new Date();
            const nextWeekday = new Date(today);
            
            // Calculate next available weekday
            do {
                nextWeekday.setDate(nextWeekday.getDate() + 1);
            } while (nextWeekday.getDay() === 0 || nextWeekday.getDay() === 6);
            
            const nextAvailableDate = nextWeekday.toISOString().split('T')[0];
            const formattedDate = formatDateDisplay(nextAvailableDate);
            
            guide.innerHTML = `
                <div class="flex items-start gap-2">
                    <i class="fas fa-calendar-check text-blue-600 mt-0.5"></i>
                    <div>
                        <p class="font-medium text-blue-800 mb-1">Available Dates:</p>
                        <ul class="text-blue-700 space-y-1">
                            <li>• Earliest: <span class="font-semibold">Tomorrow</span></li>
                            <li>• Latest: <span class="font-semibold">6 months from now</span></li>
                            <li>• Weekdays only (Mon-Fri)</li>
                            <li>• Next available: ${formattedDate}</li>
                        </ul>
                        <p class="text-red-600 text-xs mt-2">
                            <i class="fas fa-exclamation-circle"></i> Weekends and holidays are blocked
                        </p>
                    </div>
                </div>
            `;
            
            dateInput.parentNode.appendChild(guide);
        }
        
        function formatDateDisplay(dateString) {
            const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
            return new Date(dateString).toLocaleDateString('en-US', options);
        }
        
        // Hide guide when clicking outside
        document.addEventListener('click', function(e) {
            if (!dateInput.contains(e.target)) {
                const guide = document.getElementById('date-guide');
                if (guide) {
                    setTimeout(() => guide.remove(), 300);
                }
            }
        });
        
        // Add date format validation
        const originalValue = dateInput.value;
        dateInput.addEventListener('blur', function() {
            if (this.value && !this.value.match(/^\d{4}-\d{2}-\d{2}$/)) {
                alert('Please enter date in YYYY-MM-DD format');
                this.value = '';
                this.focus();
            }
        });
    }
    
    // Also restrict dates in consultant booking forms
    const consultantDateInput = document.getElementById('consultant-date') || 
                                document.querySelector('input[type="date"][name*="date"]');
    
    if (consultantDateInput && consultantDateInput !== dateInput) {
        applyConsultantDateRestrictions(consultantDateInput);
    }
    
    function applyConsultantDateRestrictions(inputElement) {
        const today = new Date();
        const tomorrow = new Date(today);
        tomorrow.setDate(tomorrow.getDate() + 1);
        
        // Consultant booking: minimum 2 days notice
        const minDate = new Date(tomorrow);
        minDate.setDate(minDate.getDate() + 1); // 2 days from now
        
        inputElement.min = minDate.toISOString().split('T')[0];
        
        // Consultant booking: maximum 30 days ahead
        const maxDate = new Date(today);
        maxDate.setDate(maxDate.getDate() + 30);
        inputElement.max = maxDate.toISOString().split('T')[0];
        
        // Consultant specific blackout days (e.g., Sundays)
        inputElement.addEventListener('change', function() {
            const selectedDate = new Date(this.value);
            const dayOfWeek = selectedDate.getDay();
            
            // Consultants unavailable on Sundays
            if (dayOfWeek === 0) {
                alert('Consultant sessions are not available on Sundays. Please select another day.');
                this.value = '';
                
                // Suggest next Monday
                const nextMonday = new Date(selectedDate);
                nextMonday.setDate(nextMonday.getDate() + 1);
                if (nextMonday <= new Date(inputElement.max)) {
                    this.value = nextMonday.toISOString().split('T')[0];
                }
            }
        });
    }
    
    // Form validation for date field
    const form = dateInput ? dateInput.closest('form') : null;
    if (form) {
        form.addEventListener('submit', function(e) {
            const dateField = document.getElementById('preferred-date');
            if (!dateField || !dateField.value) {
                alert('Please select a preferred date.');
                e.preventDefault();
                return;
            }
            
            const selectedDate = new Date(dateField.value);
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            
            if (selectedDate <= today) {
                alert('Please select a future date. Previous dates are not allowed.');
                e.preventDefault();
                dateField.focus();
                return;
            }
            
            // Check day of week
            const dayOfWeek = selectedDate.getDay();
            if (dayOfWeek === 0 || dayOfWeek === 6) {
                alert('Bookings are only available on weekdays (Monday-Friday).');
                e.preventDefault();
                dateField.focus();
                return;
            }
            
            // Additional check for blackout dates
            const blackoutDates = getBlackoutDates();
            if (blackoutDates.includes(dateField.value)) {
                alert('Selected date is not available. Please choose another date.');
                e.preventDefault();
                dateField.focus();
            }
        });
    }
    
    function getBlackoutDates() {
        // Return array of blackout dates
        // You can fetch these from an API or keep them static
        return [
            '2024-12-25',
            '2025-01-01',
            '2025-01-15',
            '2025-02-19',
            '2025-03-08',
        ];
    }
    
    // Initialize date picker with custom UI
    function initializeDatePicker() {
        const dateInputs = document.querySelectorAll('input[type="date"]');
        
        dateInputs.forEach(input => {
            // Add calendar icon
            if (!input.previousElementSibling?.classList?.contains('calendar-icon')) {
                const iconWrapper = document.createElement('div');
                iconWrapper.className = 'relative';
                
                const icon = document.createElement('i');
                icon.className = 'fas fa-calendar-alt absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 pointer-events-none';
                
                input.parentNode.classList.add('relative');
                input.parentNode.insertBefore(icon, input);
                input.classList.add('pr-10');
            }
            
            // Add today's date as placeholder text
            input.addEventListener('focus', function() {
                if (!this.value) {
                    const today = new Date();
                    const tomorrow = new Date(today);
                    tomorrow.setDate(tomorrow.getDate() + 1);
                    
                    // Find next weekday
                    while (tomorrow.getDay() === 0 || tomorrow.getDay() === 6) {
                        tomorrow.setDate(tomorrow.getDate() + 1);
                    }
                    
                    this.setAttribute('placeholder', tomorrow.toISOString().split('T')[0]);
                }
            });
            
            input.addEventListener('blur', function() {
                this.removeAttribute('placeholder');
            });
        });
    }
    
    // Run initialization
    initializeDatePicker();
});