// Get the checkbox and the div
const checkbox = document.getElementById('enable-authentication');
const div = document.getElementById('password-div');

// Function to toggle div visibility
function toggleDiv() {
    if (checkbox.checked) {
        div.style.display = 'block';  // Show div if checked
    } else {
        div.style.display = 'none';   // Hide div if unchecked
    }
}

// Add event listener to checkbox
checkbox.addEventListener('change', toggleDiv);

// Initial check when the page loads
toggleDiv();