$(document).ready(function () {
    // Función para recargar la sección
    function recargarSeccion() {
        $("#camera-image1").load("#camera-image1");
        console.log('hola')
    }

    // Llama a la función cada 10 ms
    setInterval(recargarSeccion, 10); // 10 ms
});