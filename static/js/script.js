// Add any client-side functionality here
document.addEventListener('DOMContentLoaded', function() {
    // Example: Confirm before filing return
    const fileButtons = document.querySelectorAll('a[href*="file_return"]');
    fileButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to file this tax return? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });
    
    // Example: Format financial year input
    const financialYearInput = document.getElementById('financial_year');
    if (financialYearInput) {
        financialYearInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 4) {
                value = value.substring(0, 4) + '-' + value.substring(4, 6);
            }
            e.target.value = value;
        });
    }
});