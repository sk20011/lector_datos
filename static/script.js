document.getElementById('theme').addEventListener('change', function() {
    if (this.checked) {
        document.body.classList.remove('light-theme');
        document.body.classList.add('dark-theme');
    } else {
        document.body.classList.remove('dark-theme');
        document.body.classList.add('light-theme');
    }
});

document.getElementById('runTestBtn').addEventListener('click', function() {
    const button = document.getElementById('runTestBtn');
    console.log("Botón presionado. Iniciando prueba...");
    document.getElementById('loading').style.display = 'flex';
    document.getElementById('results').style.display = 'none';
    button.disabled = true;

    fetch('/run_test')
        .then(response => {
            console.log("Respuesta recibida. Procesando...");
            return response.json();
        })
        .then(data => {
            console.log("Datos procesados:", data);
            document.getElementById('resultado_linea').innerHTML = data.tiempos["Línea por Línea"].toFixed(4);
            document.getElementById('resultado_memoria').innerHTML = data.tiempos["Completa en Memoria"].toFixed(4);
            document.getElementById('resultado_buffers').innerHTML = data.tiempos["Con Buffers"].toFixed(4);
            document.getElementById('resultado_mmap').innerHTML = data.tiempos["Con mmap"].toFixed(4);
            document.getElementById('resultado_multithreading').innerHTML = data.tiempos["Con Multithreading"].toFixed(4);
            document.getElementById('resultado_ganador').innerHTML = data.ganador;
            document.getElementById('resultado_archivo').innerHTML = data.archivo;
            document.getElementById('resultado_tipo').innerHTML = data.tipo_de_datos;

            document.getElementById('loading').style.display = 'none';
            document.getElementById('results').style.display = 'block';
            button.innerHTML = 'Volver a Ejecutar Lectura';
            button.disabled = false;
        })
        .catch(error => {
            console.error("Error al procesar la respuesta:", error);
            document.getElementById('loading').style.display = 'none';
            button.disabled = false;
        });
});
