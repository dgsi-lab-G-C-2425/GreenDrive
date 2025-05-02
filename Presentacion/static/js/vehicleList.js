// Vehicle List Animation
document.addEventListener("DOMContentLoaded", function() {
    const vehicleCards = document.querySelectorAll('.vehicle-card');
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if(entry.isIntersecting) {
                entry.target.classList.add('show');
            } else {
                entry.target.classList.remove('show');
            }
        });
    }, {
        threshold: 0.1
    });
    vehicleCards.forEach(card => {
        observer.observe(card);
    });
});