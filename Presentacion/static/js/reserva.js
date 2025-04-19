document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("reservaForm");
    const toast = document.getElementById("toast");
  
    const showToast = (msg, type = "success") => {
      toast.textContent = msg;
      toast.className = `toast ${type}`;
      setTimeout(() => toast.classList.add("hidden"), 3500);
      toast.classList.remove("hidden");
    };
  
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
  
      const vehiculo = document.getElementById("vehiculo").value;
      const fechaInicio = document.getElementById("fechaInicio").value;
      const fechaFin = document.getElementById("fechaFin").value;
      const direccion = document.getElementById("direccion").value;
  
      if (new Date(fechaInicio) >= new Date(fechaFin)) {
        showToast("La fecha fin debe ser posterior a la de inicio", "error");
        return;
      }
  
      try {
        const res = await fetch("/api/reservas", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            // Sustituye el token real si tu flujo de login te lo devuelve
            Authorization: "Bearer <token>"
          },
          body: JSON.stringify({
            vehiculo_id: vehiculo,
            fecha_inicio: fechaInicio,
            fecha_fin: fechaFin,
            punto_recogida: {
              lat: 0,
              lng: 0,
              direccion: direccion
            },
            punto_devolucion: {
              lat: 0,
              lng: 0,
              direccion: direccion
            }
          })
        });
  
        if (!res.ok) throw new Error((await res.json()).detail || res.statusText);
  
        showToast("¡Reserva creada con éxito!");
        form.reset();
      } catch (err) {
        console.error(err);
        showToast("Error al crear la reserva", "error");
      }
    });
  });  