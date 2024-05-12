//
$(document).ready(function() {
  load_status();
});

var current_status = "";

function get_status(callback) {
  var xhr = new XMLHttpRequest();

  xhr.open('GET', '/control_save_sensor_data_status', true);

  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE){
      if (xhr.status === 200) {
        callback(null, xhr.responseText);
      } else {
        console.error('La petición falló con estado: ' + xhr.status);
        callback('Error')
      }
    }
  };

  // Enviar la petición
  xhr.send();
}

function load_status() {
  get_status(function(error, status) {
    if (error) {
      console.log("Error 2: ", error);
    } else {
      current_status = status;

      var interruptor = document.getElementById("interruptor");

      if (current_status == "true") {
        interruptor.classList.add("interruptor-activado");
      }
    }
  });
}

document.getElementById("circulo_interruptor").onclick = function() {
  change_status();
}

function change_status_request(callback){
  var xhr = new XMLHttpRequest();

  xhr.open('GET', '/control_save_sensor_data_change_status', true);

  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE){
      if (xhr.status === 200) {
        callback(null, xhr.responseText);
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
  change_status_request(function(error, status) {
    if (error) {
      console.log("Error 2: ", error);
    }else {
      current_status = status;

      change_interruptor_status();
    }
  });
}

function change_interruptor_status() {
  var interruptor = document.getElementById("interruptor");
  
  if (current_status == "true") {
    interruptor.classList.remove("interruptor-desactivado");
    interruptor.classList.add("interruptor-activado");
  } else if (current_status == "false"){
    interruptor.classList.remove("interruptor-activado");
    interruptor.classList.add("interruptor-desactivado");
  }
}
