document.addEventListener('DOMContentLoaded', function() {
    // Get the preloader element
    const preloader = document.querySelector('.preloader');
    
    // Hide preloader after page is fully loaded
    window.addEventListener('load', function() {
        // Add the fade-out class to start the transition
        preloader.classList.add('fade-out');
        
        // Remove the preloader from DOM after transition completes
        setTimeout(function() {
            preloader.style.display = 'none';
        }, 800);
    });
});