var sdata;

$(document).ready(function() {
    $('#cargar').on('click', function() {
        // Realizar la solicitud AJAX al servidor para escanear la red
        $.ajax({
            url: '/user/data/credentials',
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                sdata = data;
                // Limpiar la tabla antes de agregar nuevos datos
                $('#credenciales').empty();
                // Verificar si data está definido y es iterable
                if (Array.isArray(data)) {
                  // Agregar datos escaneados a la tabla
                  console.log(data);
                  data.forEach(function(credencial) {
                    
                    // Rellenamos la variable user en caso de que este vacío
                    if ((credencial.user === '') || (credencial.user === ' ')){
                      credencial.user = '-';
                    }
                    
                    // Definimos los ids de los elementos en relacion al id de la credencial
                    var icon_id = `icon_${credencial.id}`;
                    var p_id = `p_${credencial.id}`;
                    
                    // Creamos una contraseña oculta con el mismo numero de caracteres que la original
                    var hiden_password = '';
                    for (var i = 0; i < credencial.password.length; i++) {
                      hiden_password += "•";
                    }

                    $('#credenciales').append(`
                        <div id="${credencial.id}" class="tarjeta-cred">
                          <div class="estatico">
                            <p>Sitio Web:</p>
                            <p>Usuario:</p>
                            <p>Email:</p>
                            <p>Contraseña:</p>
                            <p>Descripción:</p>
                          </div>

                          <div class="dinamico">
                            <p>${credencial.site}</p>
                            <p>${credencial.user}</p>
                            <p>${credencial.email}</p>
                            <div class="password">
                              <span id="${icon_id}" class="material-symbols-outlined switch-password-icon" onclick="switch_password('${credencial.id}','${icon_id}','${p_id}')">visibility</span>
                              <p id="${p_id}" class="f_size_bullet_points" onclick="copyPasswordToClipboard(this)">${hiden_password}</p>
                            </div>
                            <p>${credencial.description}</p>
                          </div>
                        </div>
                      `);
                  });
                } else {
                  console.error('Error: Datos no válidos recibidos del servidor.');
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error('Error al extraer los datos de la BD:', errorThrown);
            }
        });
    });
});


function switch_password(id, icon_id, p_id){
  var icon = document.getElementById(icon_id);
  var p = document.getElementById(p_id);

  if (icon.textContent == "visibility") {
    var password = "";

    sdata.forEach(function(credencial){
      if (credencial.id == id) {
        password = credencial.password;
      }
    });

    p.textContent = password;
    p.classList.remove("f_size_bullet_points");
    icon.textContent = "visibility_off";
    icon.classList.add("icon_visibility_off");
  } else if (icon.textContent == "visibility_off") {
    var hide_password = "";
    var password_len = 8; //default

    sdata.forEach(function(credencial) {
      if (credencial.id == id) {
        password_len = credencial.password.length;
      }
    });

    for (var i = 0; i < password_len; i++) {
      hide_password += "•";
    }
      
    p.textContent = hide_password;
    p.classList.add("f_size_bullet_points");
    icon.textContent = "visibility";
    icon.classList.remove("icon_visibility_off");
  }

}


function copyPasswordToClipboard(element) {
  var text = element.innerText;
  navigator.clipboard.writeText(text).then(function() {
  }, function() {
      alert('Error al copiar el texto');
  });
}