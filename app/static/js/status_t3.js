// status_t3.js
$(document).ready(function() {
function actualizarTabla3() {
  $.ajax({
    url: "/server-info",
    type: "GET",
    dataType: "json",
    success: function(data) {
      // Iterar sobre los datos recibidos
      Object.keys(data).forEach(function(obj_columna) {
        // Buscar el elemento de la tabla con el atributo data-id correspondiente
        var fila = $("#tabla3-rsp tr[data-id='" + obj_columna + "']");

        // Actualizar las celdas de IP y STATUS si la fila se encuentra
        if (fila.length > 0) {
          fila.find(".status-data").text(data[obj_columna]['status-data']);
        }
      });
    },
    error: function(jqXHR, textStatus, errorThrown) {
      console.log("Error al obtener datos desde Flask:", jqXHR);
    }
  });
}
actualizarTabla3();
// Llamar a la función para actualizar la tabla cada 5000 milisegundos (5 segundos)
setInterval(actualizarTabla3, 3000);
});
