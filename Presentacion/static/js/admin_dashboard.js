function mostrarModal(datos) {
    // General
    document.getElementById('d-modelo').textContent = datos.modelo;
    document.getElementById('d-matricula').textContent = datos.matricula;
    document.getElementById('d-tipo').textContent = datos.tipo;
    document.getElementById('d-estado').textContent = datos.estado;
    document.getElementById('d-precio').textContent = datos.precio;

    // Batería
    document.getElementById('d-b-nivel').textContent   = datos.bateria.nivel_pct;
    document.getElementById('d-b-soh').textContent     = datos.bateria.soh_pct;
    document.getElementById('d-b-ciclos').textContent  = datos.bateria.ciclos;
    document.getElementById('d-b-temp').textContent    = datos.bateria.temperatura_c;
    document.getElementById('d-b-consumo').textContent = datos.bateria.consumo_instant_kW;
    document.getElementById('d-b-recup').textContent   = datos.bateria.recuperacion_kW;

    // Ubicación
    document.getElementById('d-ubic').textContent    =
        `${datos.ubicacion.lat.toFixed(3)}, ${datos.ubicacion.lng.toFixed(3)}`;
    document.getElementById('d-vel').textContent     = datos.ubicacion.velocidad_kmh;
    document.getElementById('d-geofence').textContent = datos.ubicacion.fuera_geofence ? 'Sí' : 'No';

    // Neumáticos
    const neulist = document.getElementById('d-neumaticos');
    neulist.innerHTML = '';
    datos.neumaticos.forEach(n => {
        neulist.innerHTML += `<li>${n.posicion}: ${n.psi} psi (${n.estado})</li>`;
    });

    // Conectividad
    document.getElementById('d-con-type').textContent = datos.conectividad.tipo;
    document.getElementById('d-con-rssi').textContent = datos.conectividad.rssi_dbm;
    document.getElementById('d-con-fw').textContent   = datos.conectividad.firmware;
    document.getElementById('d-con-upd').textContent  = datos.conectividad.actualizacion_pendiente ? 'Sí' : 'No';

    // Motor & Errores
    document.getElementById('d-m-temp').textContent = datos.motor.temp_controlador_c;
    document.getElementById('d-m-errs').textContent = datos.motor.errores.length > 0
        ? datos.motor.errores.join(', ')
        : 'Ninguno';

    // Muestra modal
    document.getElementById("vehiculoModal").style.display = "block";
}


document.querySelectorAll('.vehiculo-row').forEach(row => {
    row.addEventListener('click', function() {
        const vehiculoId = this.getAttribute('data-id');
        fetch(`/vehiculos/detalles/${vehiculoId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error al obtener datos');
                }
                return response.json();
            })
            .then(data => {
                mostrarModal(data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });
});

// Cerrar modal al hacer clic en la X o fuera del contenido
const modal = document.getElementById("vehiculoModal");
const span = document.getElementsByClassName("close")[0];
span.onclick = function() {
    modal.style.display = "none";
}
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

// Función para renderizar la tabla
function renderTable(vehiculos) {
let tbody = '';
vehiculos.forEach(vehiculo => {
    tbody += `
        <tr class="vehiculo-row" data-id="${vehiculo._id}">
            <td>${vehiculo.modelo}</td>
            <td>${vehiculo.matricula}</td>
            <td>${vehiculo.bateria.nivel_pct}%</td>
            <td>${vehiculo.estado}</td>
            <td>${vehiculo.precio} cents/min</td>
        </tr>
    `;
});
document.querySelector('.table tbody').innerHTML = tbody;
attachModalEvents();
}

// Función para cargar los vehículos mediante polling
function actualizarVehiculos() {
fetch('/vehiculos/json')
    .then(response => {
        if(!response.ok) throw new Error('Error al obtener los datos.');
        return response.json();
    })
    .then(data => {
        renderTable(data);
    })
    .catch(err => console.error(err));
}

// Reasigna el evento click a cada fila de la tabla
function attachModalEvents() {
document.querySelectorAll('.vehiculo-row').forEach(row => {
    row.addEventListener('click', function() {
        const vehiculoId = this.getAttribute('data-id');
        fetch(`/vehiculos/detalles/${vehiculoId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error al obtener datos');
                }
                return response.json();
            })
            .then(data => {
                mostrarModal(data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });
});
}

// Llama a actualizarVehiculos al cargar la página y cada 60 segundos
actualizarVehiculos();
setInterval(actualizarVehiculos, 60000);