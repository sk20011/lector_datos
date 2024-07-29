from flask import Flask, render_template, jsonify
import random
import string
import emoji
import time
import os
import mmap
from concurrent.futures import ThreadPoolExecutor
import io

app = Flask(__name__)

# Aqui definimos los emojis que queremos utilizar
listado_emojis = ''.join([
    emoji.emojize(':smile:'),
    emoji.emojize(':thumbs_up:'),
    emoji.emojize(':snake:'),
    emoji.emojize(':heart:'),
    emoji.emojize(':star:'),
    emoji.emojize(':sun:'),
    emoji.emojize(':moon:'),
    emoji.emojize(':fire:'),
    emoji.emojize(':zap:')
])

# Definimos los tipos de caracteres que utilizaremos en nuestro algoritmo
tipos_de_caracteres = string.ascii_letters + string.digits + string.punctuation + listado_emojis

def genera_guardar_datos(cantidad=1000000, longitud=255, archivo_salida="datos_generados.txt", chunk_tamanio=5000):
    if not os.path.exists(archivo_salida):
        print("Generando datos...")
        with open(archivo_salida, "w", encoding="utf-8") as archivo:
            for i in range(0, cantidad, chunk_tamanio):
                datos = [
                    ''.join(random.choice(tipos_de_caracteres) for _ in range(longitud)) + "\n"
                    for _ in range(min(chunk_tamanio, cantidad - i))
                ]
                archivo.writelines(datos)
                print(f"Escrito {i + len(datos)} de {cantidad} registros")
        print("Datos generados y guardados.")
    else:
        print("El archivo de datos ya existe. No se generarán nuevos datos.")

# Métodos de Lectura
def leer_linea_por_linea(archivo):
    start_time = time.time()
    with open(archivo, 'r', encoding="utf-8") as f:
        for line in f:
            pass  
    end_time = time.time()
    return end_time - start_time

def leer_completa_memoria(archivo):
    start_time = time.time()
    with open(archivo, 'r', encoding="utf-8") as f:
        data = f.read()
    end_time = time.time()
    return end_time - start_time

def leer_con_buffers(archivo, buffer_size=1048576): 
    start_time = time.time()
    with io.open(archivo, 'r', buffering=buffer_size, encoding="utf-8") as f:
        while chunk := f.read(buffer_size):
            pass  
    end_time = time.time()
    return end_time - start_time

def leer_con_mmap(archivo):
    start_time = time.time()
    with open(archivo, 'r', encoding="utf-8") as f:
        mmapped_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        while mmapped_file.readline():
            pass  
        mmapped_file.close()
    end_time = time.time()
    return end_time - start_time

def leer_con_multithreading(archivo, num_threads=1):
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        with open(archivo, 'r', encoding="utf-8") as f:
            file_size = os.path.getsize(archivo)
            chunk_size = file_size // num_threads
            futures = [
                executor.submit(procesar_chunk, archivo, i * chunk_size, chunk_size, i, file_size)
                for i in range(num_threads)
            ]
            for future in futures:
                future.result()
    end_time = time.time()
    return end_time - start_time

def procesar_chunk(archivo, start, size, thread_index, file_size):
    with open(archivo, 'r', encoding="utf-8") as f:
        f.seek(start)
        data = f.read(size)
        if thread_index == 0:
            data = data.splitlines(True)[1:]  
        elif thread_index == file_size // size - 1:
            data = data.splitlines()[:-1]  
        for line in data:
            pass  

def medir_tiempos(archivo, n=2):  
    tiempos = {
        "Línea por Línea": [],
        "Completa en Memoria": [],
        "Con Buffers": [],
        "Con mmap": [],
        "Con Multithreading": []
    }
    
    for _ in range(n):
        tiempos["Línea por Línea"].append(leer_linea_por_linea(archivo))
        tiempos["Completa en Memoria"].append(leer_completa_memoria(archivo))
        tiempos["Con Buffers"].append(leer_con_buffers(archivo))
        tiempos["Con mmap"].append(leer_con_mmap(archivo))
        tiempos["Con Multithreading"].append(leer_con_multithreading(archivo))
    
    tiempos_promedio = {metodo: sum(tiempos[metodo])/n for metodo in tiempos}
    
    return tiempos_promedio

# Función para determinar el método más rápido
def determinar_ganador(tiempos):
    metodo_ganador = min(tiempos, key=tiempos.get)
    return metodo_ganador

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_test')
def run_test():
    archivo = 'datos_generados.txt'
    genera_guardar_datos()
    tiempos = medir_tiempos(archivo)
    ganador = determinar_ganador(tiempos)
    return jsonify({
        "tiempos": tiempos,
        "ganador": ganador,
        "archivo": archivo,
        "tipo_de_datos": 'cadena de caracteres incluyendo letras, números, signos de puntuación y emojis'
    })

if __name__ == '__main__':
    app.run(debug=True)
