//
$(document).ready(function() {
  load_status();
});

var current_status = "";

function get_status(callback) {
  var xhr = new XMLHttpRequest();

  xhr.open('GET', '/mqtt-service/status', true);

  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE){
      if (xhr.status === 200) {
        var response = JSON.parse(xhr.responseText);
        callback(null, response);
      } else {
        var e_message = `The request return ${xhr.status} error`;
        console.error(e_message);
        callback(e_message);
      }
    }
  };

  // Send request
  xhr.send();
}


function load_status() {
  get_status(function(error, response) {
    if (error) {
      console.log("Error loading status: ", error);
    } else {
      current_status = response['status'];

      var interruptor = document.getElementById("sensors_interruptor");

      // Set the correct position and data to interruptor
      if (current_status == "active") {
        interruptor.classList.add("interruptor-activado");
        interruptor.setAttribute( "title", "Activo durante " + response['time']);
      } else {
        interruptor.setAttribute( "title", "Parado durante " + response['time']);
      }
    }
  });
}


document.getElementById("circulo_interruptor").onclick = function() {
  change_status();
}

function change_status_request(callback){
  var xhr = new XMLHttpRequest();
  
  if (current_status == 'active'){
    new_status = 'off' 
  } else{
    new_status = 'on'
  }

  xhr.open('GET', '/mqtt-service/status/'+ new_status, true);

  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE){
      if (xhr.status === 200) {
        callback(null, JSON.parse(xhr.responseText));
      } else {
        console.error('La petición falló con estado: ' + xhr.status);
        callback('Error con la petición.')
      }
    }
  };

  // Enviar la petición
  xhr.send();
}

function change_status() {
  change_status_request(function(error, response) {
    if (error) {
      console.log("Error 2: ", error);
    }else {
      if (response['action'] == 'success') {
        current_status = response['status']
        change_interruptor_status();
      } else {
        alert("No se ha podido cambiar el estado del servicio MQTT");
      }
    }
  });
}

function change_interruptor_status() {

  var interruptor = document.getElementById("sensors_interruptor");
  
  if (current_status == "active") {
    interruptor.classList.remove("interruptor-desactivado");
    interruptor.classList.add("interruptor-activado");
    interruptor.setAttribute("title", "Activado por ti ahora mismo")
  } else if (current_status == "inactive"){
    interruptor.classList.remove("interruptor-activado");
    interruptor.classList.add("interruptor-desactivado");
    interruptor.setAttribute("title", "Parado por ti ahora mismo")
  }
}
