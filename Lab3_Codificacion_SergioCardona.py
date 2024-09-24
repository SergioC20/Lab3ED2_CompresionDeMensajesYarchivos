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

# Función para comprimir el mensaje usando Huffman en modo automático
def comprimir_huffman_automatico(mensaje):
    frecuencias = Counter(mensaje)
    total_caracteres = len(mensaje)
    probabilidades = {caracter: freq / total_caracteres for caracter, freq in frecuencias.items()}
    
    # Construir el árbol de Huffman
    raiz_huffman = construir_arbol_huffman(frecuencias)
    
    # Generar los códigos de Huffman
    codigos_huffman = generar_codigos_huffman(raiz_huffman)
    
    # Codificar el mensaje
    mensaje_codificado = ''.join([codigos_huffman[caracter] for caracter in mensaje])
    
    return mensaje_codificado, codigos_huffman, frecuencias, probabilidades

# Función para comprimir el mensaje usando Huffman en modo no automático
def comprimir_huffman_no_automatico(mensaje, frecuencias):
    for caracter in mensaje:
        if caracter not in frecuencias:
            raise ValueError(f"El carácter '{caracter}' no está en la tabla de frecuencias.")
    
    raiz_huffman = construir_arbol_huffman(frecuencias)
    codigos_huffman = generar_codigos_huffman(raiz_huffman)
    mensaje_codificado = ''.join([codigos_huffman[caracter] for caracter in mensaje])
    
    return mensaje_codificado, codigos_huffman

# Función para manejar la compresión automática
def manejar_compresion_automatica(mensaje):
    mensaje_codificado, codigos_huffman, frecuencias, probabilidades = comprimir_huffman_automatico(mensaje)
    
    # Mostrar los resultados
    print("\n--- Compresión Automática ---")
    print("\nMensaje codificado:", mensaje_codificado)
    print("\nTabla de frecuencias:", frecuencias)
    print("\nProbabilidad de cada caracter:", probabilidades)
    print("\nCódigo de cada caracter:", codigos_huffman)
    print("\nTasa de compresión:", len(mensaje_codificado) / (len(mensaje) * 8))

    # Guardar los resultados en un archivo
    num_archivo = input("Introduce un número para el archivo de salida: ")
    with open(f"codificacion{num_archivo}.log", "w") as archivo:
        archivo.write(f"------- Huffman Compresion Automatica -------\n")
        archivo.write(f"Mensaje original: {mensaje}\n")
        archivo.write(f"Mensaje codificado: {mensaje_codificado}\n")
        archivo.write(f"Tabla de frecuencias: {frecuencias}\n")
        archivo.write(f"Probabilidad de cada caracter: {probabilidades}\n")
        archivo.write(f"Código de cada caracter: {codigos_huffman}\n")
        archivo.write(f"Tasa de compresión: {len(mensaje_codificado) / (len(mensaje) * 8)}\n")

# Función para manejar la compresión no automática con fallback a la automática
def manejar_compresion_no_automatica(mensaje):
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
        mensaje_codificado, codigos_huffman = comprimir_huffman_no_automatico(mensaje, frecuencias)
        
        # Mostrar los resultados
        print("\n--- Compresión No Automática ---")
        print("\nMensaje codificado:", mensaje_codificado)
        print("\nCódigo de cada caracter:", codigos_huffman)

        # Guardar los resultados en un archivo
        num_archivo = input("Introduce un número para el archivo de salida: ")
        with open(f"codificacion{num_archivo}.log", "w") as archivo:
            archivo.write(f"------- Huffman Compresion No Automatica -------\n")
            archivo.write(f"Mensaje original: {mensaje}\n")
            archivo.write(f"Mensaje codificado: {mensaje_codificado}\n")
            archivo.write(f"Código de cada caracter: {codigos_huffman}\n")
    
    except ValueError as e:
        print(f"Error: {e}")
        print("Pasando a compresión automática...")
        manejar_compresion_automatica(mensaje)

# Función principal
def main():
    mensaje = input("Introduce el mensaje a comprimir: ")
    opcion = input("Selecciona el modo de compresión: 'automatica' o 'no automatica': ").strip().lower()
    
    if opcion == "automatica":
        manejar_compresion_automatica(mensaje)
    elif opcion == "no automatica":
        manejar_compresion_no_automatica(mensaje)
    else:
        print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
