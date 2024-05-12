// status.js
$(document).ready(function() {
function actualizarTabla1() {
  $.ajax({
    url: "/devices-connection-status",
    type: "GET",
    dataType: "json",
    success: function(data) {
      // Iterar sobre los datos recibidos
      Object.keys(data).forEach(function(dispositivo) {
        // Buscar el elemento de la tabla con el atributo data-id correspondiente
        var fila = $("#tabla-piso tr[data-id='" + dispositivo + "']");
        
        // Actualizar las celdas de IP y STATUS si la fila se encuentra
        if (fila.length > 0) {
          fila.find(".columnaSTATUS").text(data[dispositivo]['columnaSTATUS']);
        }
      });
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

