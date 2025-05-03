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

    let currentMatricula = '';
    let currentModelo = '';

    // Gestión de reserva con modal
    document.querySelectorAll('.reservationForm').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            currentMatricula = this.dataset.matricula;
            currentModelo = this.closest('.vehicle-card').querySelector('.vehicle-name').innerText;
            // set body del modal
            $('#reservationModal .modal-body').html(
                `¿Desea reservar el vehículo <strong>${currentModelo}</strong>?`
            );
            $('#reservationModal').modal('show');
        });
    });

    // Al pulsar "Reservar" en el modal
    document.getElementById('confirmReservationButton').addEventListener('click', function() {
        // ocultar botones del pie del modal
        $('#reservationModal .modal-footer button').hide();

        fetch(`/vehiculos/reservar`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                matricula: currentMatricula,
                id_usuario: userId   // ahora se envía el id de usuario
            })
        })
        .then(res => res.json())
        .then(data => {
            const body = $('#reservationModal .modal-body');
            if (data.status === 'success') {
                body.html(
                    `<div class="text-center">
                        <svg class="checkmark" viewBox="0 0 52 52">
                            <path d="M14 27 L22 35 L38 19"></path>
                        </svg>
                        <p>¡Vehículo reservado con éxito!</p>
                    </div>`
                );
                setTimeout(() => location.reload(), 1200);
            } else {
                body.html(`<p class="text-danger">Error al reservar vehículo.</p>`);
            }
        })
        .catch(() => {
            $('#reservationModal .modal-body').html(`<p class="text-danger">Error de conexión.</p>`);
        });
    });
});

// Gestion Mapa
let map, userMarker;

function initMap() {
    // Verificar si la API de Google Maps se cargó correctamente
    if (typeof google === 'undefined' || typeof google.maps === 'undefined') {
        alert("Error: No se pudo cargar la API de Google Maps. Verifica la clave API.");
        return;
    }

    // Centro inicial (Talavera)
    const initialCenter = { lat: 39.9620, lng: -4.8308 };

    // Delimitar un rectángulo que abarca Talavera y alrededores inmediatos
    const allowedBounds = {
        north: 40.00,   // latitud máxima
        south: 39.92,   // latitud mínima
        west: -4.88,    // longitud mínima
        east: -4.78     // longitud máxima
    };

    map = new google.maps.Map(document.getElementById("map"), {
        center: initialCenter,
        zoom: 13,
        restriction: {
            latLngBounds: allowedBounds,
            strictBounds: true // Impide desplazar el mapa fuera de Talavera
        },
        mapTypeControl: false,
        streetViewControl: false,
    });

    // Intentamos obtener la ubicación del usuario
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            position => {
                const userPos = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };

                // Verificar si la ubicación del usuario está dentro de los límites permitidos
                if (
                    userPos.lat >= allowedBounds.south &&
                    userPos.lat <= allowedBounds.north &&
                    userPos.lng >= allowedBounds.west &&
                    userPos.lng <= allowedBounds.east
                ) {
                    // Centrar el mapa en la posición del usuario
                    map.setCenter(userPos);
                    map.setZoom(15);

                    // Añadir un marcador para la ubicación actual
                    userMarker = new google.maps.Marker({
                        position: userPos,
                        map: map,
                        title: "Tú estás aquí"
                    });
                } else {
                    alert("Tu ubicación está fuera de los límites permitidos.");
                }
            },
            error => {
                console.error("Error al obtener ubicación:", error.message);
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            }
        );
    } else {
        alert("Tu navegador no soporta Geolocation.");
    }

    // Cargar vehículos desde la API
    fetch('/map/data')
        .then(res => res.json())
        .then(vehicles => {
            vehicles.forEach(v => {
                new google.maps.Marker({
                    position: { lat: v.lat, lng: v.lng },
                    map: map,
                    icon: {
                        url: v.icon,
                        scaledSize: new google.maps.Size(50, 50)
                    },
                    title: v.title
                });
            });
        })
        .catch(err => console.error('Error cargando vehículos:', err));
}

// Inicializar el mapa al cargar la página
window.onload = initMap;