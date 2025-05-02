// Vehicle List Animation y gestión del modal
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

    // Gestión de la expansión de la tarjeta
    vehicleCards.forEach(card => {
        card.addEventListener('click', (e) => {
            // Evitar que al hacer clic en el formulario se cierre la tarjeta
            if(e.target.closest('.reservationForm')) return;
            
            // Si ya está expandida, la colapsa
            if(card.classList.contains('expanded')){
                card.classList.remove('expanded');
            } else {
                // Colapsa cualquier tarjeta expandida
                vehicleCards.forEach(c => c.classList.remove('expanded'));
                card.classList.add('expanded');
            }
        });
    });
});