$(document).ready(function() {
    // Definir la función para realizar la solicitud AJAX
    function ejecutarSolicitud() {
        $.ajax({
            url: '/last-access-log-entry',
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                // Limpiar la tabla antes de agregar nuevos datos
                $('#sqlTable1 tbody').empty();
                
                // Verificar si data está definido y es iterable
                if (Array.isArray(data)) {
                    // Agregar datos escaneados a la tabla
                    data.forEach(function(query) {
                        $('#sqlTable1 tbody').append(
                            `<tr>
                                <td>${query.id}</td>
                                <td>${query.remote_host}</td>
                                <td>${query.date}</td>
                            </tr>`
                        );
                    });
                } else {
                    console.error('Error: Datos no válidos recibidos del servidor.');
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error('Error al cargar los datos:', errorThrown);
            }
        });
    }
    ejecutarSolicitud();
    // Establecer un intervalo para ejecutar la solicitud cada 5 segundos
    setInterval(ejecutarSolicitud, 5000);
});

