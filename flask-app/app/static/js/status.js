// status.js
$(document).ready(function() {
function actualizarTabla1() {
  $.ajax({
    url: "/devices-connection-status",
    type: "GET",
    dataType: "json",
    success: function(data) {
      $('#tabla-piso tbody').empty();

      if (Array.isArray(data)) {
         // Agregar datos escaneados a la tabla
         data.forEach(function(device) {
            $('#tabla-piso tbody').append(
                `<tr>
                    <td>${device.name}</td>
                    <td>${device.IP}</td>
                    <td>${device.status}</td>
                </tr>`
            );
        });
      } else {
        console.error('Error: Datos no válidos recibidos del servidor.');
      }
    },
    error: function(jqXHR, textStatus, errorThrown) {
      console.log("Error al obtener datos desde Flask:", jqXHR);
    }
  });
}
actualizarTabla1();
// Llamar a la función para actualizar la tabla cada 5000 milisegundos (5 segundos)
setInterval(actualizarTabla1, 5000);
});

