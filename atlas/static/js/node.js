const nodemailer = require('nodemailer');

const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
        user: 'tucorreo@gmail.com', 
        pass: 'tu-contraseña' 
    }
});

const mailOptions = {
    from: 'tucorreo@gmail.com',
    to: 'contacto@atlaspa.cl',
    subject: 'Nuevo Reclamo',
    text: `Nombre: ${req.body.nombre}\nCorreo: ${req.body.email}\nDescripción: ${req.body.descripcion}`
};

transporter.sendMail(mailOptions, function(error, info){
    if (error) {
        console.log(error);
    } else {
        console.log('Correo enviado: ' + info.response);
    }
});
