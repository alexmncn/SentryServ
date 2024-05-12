$(document).ready(function() {
    $('#scanButton').on('click', function() {
        // Realizar la solicitud AJAX al servidor para escanear la red
        $.ajax({
            url: '/net-devices-scan',
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                // Limpiar la tabla antes de agregar nuevos datos
                $('#scanTable tbody').empty();

                // Verificar si data está definido y es iterable
                if (Array.isArray(data)) {
                  // Agregar datos escaneados a la tabla
                  data.forEach(function(host) {
                      $('#scanTable tbody').append(
                          `<tr>
                              <td>${host.Host}</td>
                              <td>${host.IP}</td>
                              <td>${host.Status}</td>
                          </tr>`
                      );
                  });
                } else {
                  console.error('Error: Datos no válidos recibidos del servidor.');
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error('Error al escanear la red:', errorThrown);
            }
        });
    });
});
