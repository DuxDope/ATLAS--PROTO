<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {

    $nombre = $_POST['nombre'];
    $email = $_POST['email'];
    $descripcion = $_POST['descripcion'];


    $to = "reclamos@atlasxd.online";
    $subject = "Nuevo Reclamo - Atlas XD";
    

    $message = "Nuevo reclamo recibido:\n\n";
    $message .= "Nombre: " . $nombre . "\n";
    $message .= "Correo: " . $email . "\n";
    $message .= "Descripción:\n" . $descripcion . "\n";


    $headers = "From: " . $email . "\r\n";
    $headers .= "Reply-To: " . $email . "\r\n";
    $headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

    if (mail($to, $subject, $message, $headers)) {
        echo "Reclamo enviado con éxito. ¡Gracias por contactarnos!";
    } else {
        echo "Hubo un error al enviar el reclamo. Inténtalo nuevamente.";
    }
}
?>
