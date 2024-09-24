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

# Función para comprimir el mensaje usando Huffman
def comprimir_huffman(mensaje):
    # Calcular la frecuencia de cada caracter en el mensaje
    frecuencias = Counter(mensaje)
    total_caracteres = len(mensaje)
    
    # Calcular la probabilidad de cada caracter
    probabilidades = {caracter: freq / total_caracteres for caracter, freq in frecuencias.items()}
    
    # Construir el árbol de Huffman
    raiz_huffman = construir_arbol_huffman(frecuencias)
    
    # Generar los códigos de Huffman
    codigos_huffman = generar_codigos_huffman(raiz_huffman)
    
    # Codificar el mensaje
    mensaje_codificado = ''.join([codigos_huffman[caracter] for caracter in mensaje])
    
    return mensaje_codificado, codigos_huffman, frecuencias, probabilidades

# Función principal
def main():
    mensaje = input("Introduce el mensaje a comprimir: ")
    mensaje_codificado, codigos_huffman, frecuencias, probabilidades = comprimir_huffman(mensaje)
    
    # Mostrar los resultados
    print("\nMensaje codificado:", mensaje_codificado)
    print("\nTabla de frecuencias:", frecuencias)
    print("\nProbabilidad de cada caracter:", probabilidades)
    print("\nCódigo de cada caracter:", codigos_huffman)
    print("\nTasa de compresión:", len(mensaje_codificado) / (len(mensaje) * 8))

    # Guardar los resultados en un archivo
    num_archivo = input("Introduce un número para el archivo de salida: ")
    with open(f"codificacion{num_archivo}.log", "w") as archivo:
        archivo.write(f"Mensaje original: {mensaje}\n")
        archivo.write(f"Mensaje codificado: {mensaje_codificado}\n")
        archivo.write(f"Tabla de frecuencias: {frecuencias}\n")
        archivo.write(f"Probabilidad de cada caracter: {probabilidades}\n")
        archivo.write(f"Código de cada caracter: {codigos_huffman}\n")
        archivo.write(f"Tasa de compresión: {len(mensaje_codificado) / (len(mensaje) * 8)}\n")

if __name__ == "__main__":
    main()
