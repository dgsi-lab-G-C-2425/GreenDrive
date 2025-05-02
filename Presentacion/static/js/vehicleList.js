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

    // Gestión del modal emergente
    const modalOverlay = document.getElementById('vehicleModal');
    const modalClose = document.getElementById('modalClose');

    vehicleCards.forEach(card => {
        card.addEventListener('click', () => {
            modalOverlay.classList.add('show');
        });
    });

    modalClose.addEventListener('click', () => {
        modalOverlay.classList.remove('show');
    });

    // Cierra el modal si se hace clic fuera del contenido
    modalOverlay.addEventListener('click', (e) => {
        if(e.target === modalOverlay) {
            modalOverlay.classList.remove('show');
        }
    });
});