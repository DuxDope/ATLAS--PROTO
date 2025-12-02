function goToScreen2() {
    const name = document.getElementById('name').value;

    const userNameElement = document.getElementById('userName');
    const customerIdElement = document.getElementById('customerId');
    const footerUserNameElement = document.getElementById('footerUserName');

    if (userNameElement) userNameElement.innerText = name;
    if (customerIdElement) customerIdElement.innerText = "Id: " + name;
    if (footerUserNameElement) footerUserNameElement.innerText = name;

    document.getElementById('screen1').classList.remove('visible');
    document.getElementById('screen2').classList.add('visible');
    document.getElementById('serviceScreen').classList.remove('visible');
}

function goToScreen1() {
    document.getElementById('screen2').classList.remove('visible');
    document.getElementById('screen1').classList.add('visible');
    document.getElementById('serviceScreen').classList.remove('visible');
}

function goToServiceScreen() {
    document.getElementById('screen2').classList.remove('visible');
    document.getElementById('serviceScreen').classList.add('visible');
}


function generarNumero(opcion) {
    const numero = Math.floor(1000 + Math.random() * 9000);
    const url = `/atencion2/?numero=${numero}&opcion=${opcion}`;
    window.location.href = url;
}


document.addEventListener("DOMContentLoaded", function() {
    console.log("DOM completamente cargado y analizado");
    const form = document.getElementById("form-identificacion");
    if (form) {
        form.addEventListener("submit", validateAndContinue);
    }
});

function validateRut(rut) {
    console.log("Validando RUT:", rut);
    const rutRegex = /^[0-9]+-[0-9kK]{1}$/;
    return rutRegex.test(rut);
}

function validateAndContinue(event) {
    console.log("Iniciando validación del formulario");

    const rut = document.getElementById("rut").value.trim();
    const name = document.getElementById("name").value.trim();

    console.log("Valores recibidos - RUT:", rut, "Nombre:", name);

    let valid = true;

    if (!rut || !name) {
        console.log("Campos vacíos detectados");
        alert("Por favor, complete ambos campos antes de continuar.");
        valid = false;
    } else if (!validateRut(rut)) {
        console.log("RUT inválido detectado");
        alert("Por favor, ingrese un RUT válido (ej: 12345678-9).");
        valid = false;
    }

    if (!valid) {
        console.log("Prevent default");
        event.preventDefault(); 
    }

    return valid;
}
