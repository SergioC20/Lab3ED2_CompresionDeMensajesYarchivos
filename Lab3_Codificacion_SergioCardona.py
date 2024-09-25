import heapq
from collections import Counter

# Nodo del árbol de Huffman
class NodoHuffman:
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izq = None
        self.der = None

    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

# Función para construir el árbol de Huffman
def construir_arbol_huffman(frecuencias):
    heap = [NodoHuffman(caracter, freq) for caracter, freq in frecuencias.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        nodo_izq = heapq.heappop(heap)
        nodo_der = heapq.heappop(heap)
        nodo_fusion = NodoHuffman(None, nodo_izq.frecuencia + nodo_der.frecuencia)
        nodo_fusion.izq = nodo_izq
        nodo_fusion.der = nodo_der
        heapq.heappush(heap, nodo_fusion)

    return heap[0]

# Función para generar el código de Huffman
def generar_codigos_huffman(nodo, codigo_actual="", codigos={}):
    if nodo is None:
        return
    if nodo.caracter is not None:
        codigos[nodo.caracter] = codigo_actual
    generar_codigos_huffman(nodo.izq, codigo_actual + "0", codigos)
    generar_codigos_huffman(nodo.der, codigo_actual + "1", codigos)
    return codigos

# Función para decodificar un mensaje
def decodificar_mensaje(codigo_binario, raiz_huffman):
    mensaje_decodificado = []
    nodo_actual = raiz_huffman
    
    for bit in codigo_binario:
        if bit == "0":
            nodo_actual = nodo_actual.izq
        else:
            nodo_actual = nodo_actual.der
        
        # Si llegamos a una hoja, es un carácter
        if nodo_actual.izq is None and nodo_actual.der is None:
            mensaje_decodificado.append(nodo_actual.caracter)
            nodo_actual = raiz_huffman  # Regresar a la raíz para el siguiente carácter
    
    return ''.join(mensaje_decodificado)

# Función para leer el archivo log y obtener los datos de codificación
def leer_datos_de_log(archivo_log):
    frecuencias = {}
    mensaje_codificado = ""

    with open(archivo_log, "r", encoding='utf-8') as archivo:
        modo_automatico = False
        for linea in archivo:
            linea = linea.strip()
            if linea.startswith("Modo: Automático"):
                modo_automatico = True
            elif linea.startswith("Mensaje codificado:"):
                mensaje_codificado = linea.split(": ")[1]
            elif linea.startswith("Tabla de frecuencias:") and modo_automatico:
                tabla_frecuencias = linea.split(": ")[1].strip('{}').split(', ')
                for item in tabla_frecuencias:
                    caracter, freq = item.split(": ")
                    frecuencias[caracter.strip("'")] = int(freq)
            elif linea.startswith("Código de cada caracter:") and not modo_automatico:
                # En modo no automático no hay frecuencias, solo los códigos
                tabla_codigos = linea.split(": ")[1].strip('{}').split(', ')
                for item in tabla_codigos:
                    caracter, _ = item.split(": ")
                    frecuencias[caracter.strip("'")] = 1  # Crear un árbol binario igual para todos los caracteres
    
    return mensaje_codificado, frecuencias

# Función para manejar la descompresión
def manejar_descompresion():
    archivo_log = input("Introduce el nombre del archivo de log para descomprimir (incluye la extensión .log): ")
    
    try:
        # Leer los datos del archivo log
        mensaje_codificado, frecuencias = leer_datos_de_log(archivo_log)
        
        if not mensaje_codificado or not frecuencias:
            raise ValueError("El archivo de log no contiene datos válidos.")
        
        # Reconstruir el árbol de Huffman
        raiz_huffman = construir_arbol_huffman(frecuencias)
        
        # Decodificar el mensaje
        mensaje_decodificado = decodificar_mensaje(mensaje_codificado, raiz_huffman)
        
        print("\n--- Descompresión ---")
        print("Mensaje decodificado:", mensaje_decodificado)
    
    except FileNotFoundError:
        print(f"Error: El archivo '{archivo_log}' no fue encontrado.")
    except Exception as e:
        print(f"Error: {e}")

# Función para manejar la compresión automática
def manejar_compresion_automatica():
    mensaje = input("Introduce el mensaje a comprimir: ")
    frecuencias = Counter(mensaje)
    total_caracteres = len(mensaje)
    probabilidades = {caracter: freq / total_caracteres for caracter, freq in frecuencias.items()}
    
    # Construir el árbol de Huffman
    raiz_huffman = construir_arbol_huffman(frecuencias)
    
    # Generar los códigos de Huffman
    codigos_huffman = generar_codigos_huffman(raiz_huffman)
    
    # Codificar el mensaje
    mensaje_codificado = ''.join([codigos_huffman[caracter] for caracter in mensaje])
    
    # Mostrar los resultados
    print("\n--- Compresión Automática ---")
    print("Mensaje codificado:", mensaje_codificado)
    print("Tabla de frecuencias:", frecuencias)
    print("Probabilidad de cada caracter:", probabilidades)
    print("Código de cada caracter:", codigos_huffman)
    print("Tasa de compresión:", len(mensaje_codificado) / (len(mensaje) * 8))

    # Guardar los resultados en un archivo
    num_archivo = input("Introduce un número para el archivo de salida: ")
    with open(f"codificacion{num_archivo}.log", "w", encoding='utf-8') as archivo:
        archivo.write("Método: Huffman\n")
        archivo.write("Modo: Automático\n")
        archivo.write(f"Mensaje original: {mensaje}\n")
        archivo.write(f"Tabla de frecuencias: {frecuencias}\n")
        archivo.write(f"Probabilidad de cada caracter: {probabilidades}\n")
        archivo.write(f"Código de cada caracter: {codigos_huffman}\n")
        archivo.write(f"Tasa de compresión: {len(mensaje_codificado) / (len(mensaje) * 8)}\n")
        archivo.write(f"Mensaje codificado: {mensaje_codificado}\n")

# Función para manejar la compresión no automática
def manejar_compresion_no_automatica():
    mensaje = input("Introduce el mensaje a comprimir: ")
    print("Introduce la tabla de frecuencias (carácter y frecuencia separados por espacio, una línea por carácter).")
    print("Cuando termines, escribe 'fin'.")
    frecuencias = {}
    
    while True:
        entrada = input()
        if entrada.lower() == 'fin':
            break
        
        # Manejo especial para el espacio
        if entrada.startswith(" "):  # Si el carácter es un espacio
            frecuencia = int(entrada.strip().split()[0])
            frecuencias[" "] = frecuencia
        else:
            caracter, frecuencia = entrada.split()
            frecuencias[caracter] = int(frecuencia)
    
    try:
        raiz_huffman = construir_arbol_huffman(frecuencias)
        codigos_huffman = generar_codigos_huffman(raiz_huffman)
        
        # Codificar el mensaje
        mensaje_codificado = ''.join([codigos_huffman[caracter] for caracter in mensaje])
        
        # Mostrar los resultados
        print("\n--- Compresión No Automática ---")
        print("Mensaje codificado:", mensaje_codificado)
        print("Código de cada caracter:", codigos_huffman)

        # Guardar los resultados en un archivo
        num_archivo = input("Introduce un número para el archivo de salida: ")
        with open(f"codificacion{num_archivo}.log", "w", encoding='utf-8') as archivo:
            archivo.write("Método: Huffman\n")
            archivo.write("Modo: No Automático\n")
            archivo.write(f"Mensaje original: {mensaje}\n")
            archivo.write(f"Código de cada caracter: {codigos_huffman}\n")
            archivo.write(f"Mensaje codificado: {mensaje_codificado}\n")
    
    except ValueError as e:
        print(f"Error: {e}")
        print("Pasando a compresión automática...")
        manejar_compresion_automatica()

# Función para mostrar el submenú para Huffman
def mostrar_submenu_huffman():
    while True:
        print("\n--- Submenú Huffman ---")
        print("1. Codificación automática")
        print("2. Codificación no automática")
        print("3. Descompresión")
        print("4. Volver al menú principal")
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            manejar_compresion_automatica()
        elif opcion == "2":
            manejar_compresion_no_automatica()
        elif opcion == "3":
            manejar_descompresion()
        elif opcion == "4":
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

# Función principal para mostrar el menú principal
def mostrar_menu_principal():
    while True:
        print("\n--- Menú Principal ---")
        print("1. Huffman")
        print("2. Salir")
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            mostrar_submenu_huffman()
        elif opcion == "2":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    mostrar_menu_principal()
