import heapq
import math
import ast
import re
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

#funcion para escribir bits
def write_bit(bit, bits):
    bits.append(bit)

def read_bit(bits, index):
    if index < len(bits):
        return int(bits[index]), index + 1
    return None, index

def int_arith_code(mensaje, k, frecuencias):
    T = sum(frecuencias.values()) #total de frecuencias
    R = 2 ** k
    l = 0
    u = R - 1
    m = 0
    bits = []  # Lista donde almacenamos los bits codificados
    
    # Construimos los límites f(i) y f(i+1)
    limites = {}
    acumulado = 0
    for simbolo, frecuencia in frecuencias.items():
        limites[simbolo] = (acumulado, acumulado + frecuencia)
        acumulado += frecuencia
    
    # Codificación del mensaje
    for caracter in mensaje:
        s = u - l + 1
        f_i, f_i_plus_1 = limites[caracter]
        u = l + math.floor(s * f_i_plus_1 / T) - 1
        l = l + math.floor(s * f_i / T)
        
        while True:
            if l >= R // 2:  # Intervalo en la mitad superior
                write_bit(1, bits)
                u = 2 * u - R + 1
                l = 2 * l - R
                for _ in range(m):
                    write_bit(0, bits)
                m = 0
            elif u < R // 2:  # Intervalo en la mitad inferior
                write_bit(0, bits)
                u = 2 * u + 1
                l = 2 * l
                for _ in range(m):
                    write_bit(1, bits)
                m = 0
            elif l >= R // 4 and u < 3 * R // 4:  # Intervalo en la mitad intermedia
                u = 2 * u - R // 2 + 1
                l = 2 * l - R // 2
                m += 1
            else:
                break  # Salir del bucle interno
    
    # Salida final de bits
    if l >= R // 4:
        write_bit(1, bits)
        for _ in range(m):
            write_bit(0, bits)
        write_bit(0, bits)
    else:
        write_bit(0, bits)
        for _ in range(m):
            write_bit(1, bits)
        write_bit(1, bits)

    return bits
def int_arith_decode(mensaje_codificado, k, n, frecuencias):
    R = 2 ** k
    l, u = 0, R - 1
    T = sum(frecuencias.values())
    mensaje_decodificado = []
    
    # Construir los límites f(i) y f(i+1)
    limites = {}
    acumulado = 0
    for simbolo, frecuencia in frecuencias.items():
        limites[simbolo] = (acumulado, acumulado + frecuencia)
        acumulado += frecuencia
    
    # Convertir el mensaje codificado de string a un número entero
    codigo = int(mensaje_codificado, 2)
    
    for _ in range(n):
        s = u - l + 1
        valor = ((codigo - l + 1) * T - 1) // s
        
        # Encontrar el símbolo que corresponde al valor actual
        for simbolo, (f_i, f_i_plus_1) in limites.items():
            if f_i <= valor < f_i_plus_1:
                mensaje_decodificado.append(simbolo)
                u = l + (s * f_i_plus_1) // T - 1
                l = l + (s * f_i) // T
                break
        
        # Renormalización (ajuste de los intervalos)
        while True:
            # Si el rango completo se encuentra en la primera mitad
            if u < R // 2:
                l = 2 * l
                u = 2 * u + 1
                codigo = 2 * codigo
            # Si el rango completo se encuentra en la segunda mitad
            elif l >= R // 2:
                l = 2 * (l - R // 2)
                u = 2 * (u - R // 2) + 1
                codigo = 2 * (codigo - R // 2)
            # Si el rango está cerca del centro (renormalización en el tercer cuarto)
            elif l >= R // 4 and u < 3 * R // 4:
                l = 2 * (l - R // 4)
                u = 2 * (u - R // 4) + 1
                codigo = 2 * (codigo - R // 4)
            else:
                break
            
            # Esto asegura que el valor de `codigo` no exceda el tamaño de R
            codigo %= R
    
    return ''.join(mensaje_decodificado)

# Función para manejar la compresión automática
def manejar_compresion_automatica_huffman(mensaje=None):
    if mensaje is None:
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
        archivo.write(f"Mensaje codificado: {mensaje_codificado}\n")
        archivo.write(f"Tabla de frecuencias: {frecuencias}\n")
        archivo.write(f"Probabilidad de cada caracter: {probabilidades}\n")
        archivo.write(f"Código de cada caracter: {codigos_huffman}\n")
        archivo.write(f"Tasa de compresión: {len(mensaje_codificado) / (len(mensaje) * 8)}\n")
        


# Función para manejar la compresión no automática
def manejar_compresion_no_automatica_huffman():
    mensaje = input("Introduce el mensaje a comprimir: ")
    print("Introduce la tabla de frecuencias (carácter y frecuencia separados por espacio, una línea por carácter).")
    print("Nota: Para el espacio, ingresa 'espacio' seguido de su frecuencia (ejemplo: 'espacio 1').")
    print("Cuando termines, escribe 'fin'.")
    frecuencias_usuario = {}

    # Leer la tabla de frecuencias ingresada por el usuario
    while True:
        entrada = input().strip()
        if entrada.lower() == 'fin':
            break
        
        # Validación de que se ingresen dos valores separados (carácter y frecuencia)
        if len(entrada.split()) != 2:
            print("Error: Debes ingresar un carácter seguido de su frecuencia. Ejemplo: 'a 3'. Inténtalo de nuevo.")
            continue

        # Manejo del carácter de espacio
        partes = entrada.split()
        caracter, frecuencia_str = partes[0], partes[1]

        # Si se ingresa 'espacio', lo convertimos a un espacio real
        if caracter == 'espacio':
            caracter = ' '

        try:
            frecuencia = int(frecuencia_str)
            frecuencias_usuario[caracter] = frecuencia
        except ValueError:
            print("Error: Debes ingresar un número válido para la frecuencia. Inténtalo de nuevo.")
            continue

    # Validar si las frecuencias ingresadas coinciden con las frecuencias reales en el mensaje
    frecuencias_reales = Counter(mensaje)

    # Validar que todos los caracteres en el mensaje estén en la tabla de frecuencias
    for caracter, frecuencia_real in frecuencias_reales.items():
        if caracter not in frecuencias_usuario:
            print(f"Error: El carácter '{caracter}' no está presente en la tabla de frecuencias.")
            print("Pasando a compresión automática con el mismo mensaje...")
            manejar_compresion_automatica_huffman(mensaje)
            return
        elif frecuencias_usuario[caracter] != frecuencia_real:
            print(f"Error: La frecuencia del carácter '{caracter}' es incorrecta. Frecuencia real: {frecuencia_real}, pero se ingresó: {frecuencias_usuario[caracter]}.")
            print("Pasando a compresión automática con el mismo mensaje...")
            manejar_compresion_automatica_huffman(mensaje)
            return

    # Validar que ningún carácter de la tabla esté ausente en el mensaje
    for caracter in frecuencias_usuario:
        if caracter not in mensaje:
            print(f"Error: El carácter '{caracter}' fue ingresado en la tabla de frecuencias, pero no está presente en el mensaje.")
            print("Pasando a compresión automática con el mismo mensaje...")
            manejar_compresion_automatica_huffman(mensaje)
            return

    try:
        # Si todo es correcto, construir el árbol de Huffman
        raiz_huffman = construir_arbol_huffman(frecuencias_usuario)
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
            archivo.write(f"Mensaje codificado: {mensaje_codificado}\n")
            archivo.write(f"Código de cada caracter: {codigos_huffman}\n")

    except ValueError as e:
        print(f"Error: {e}")
        print("Pasando a compresión automática...")
        manejar_compresion_automatica_huffman(mensaje)


def decodificar_huffman(mensaje_codificado, codigos):
    mensaje_decodificado = ""
    codigo_actual = ""
    
    for bit in mensaje_codificado:
        codigo_actual += bit
        for caracter, codigo in codigos.items():
            if codigo == codigo_actual:
                mensaje_decodificado += caracter
                codigo_actual = ""
                break
    
    return mensaje_decodificado

def decodificar_huffman_desde_archivo():
    nombre_archivo = input("Introduce el nombre del archivo .log: ")
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
        
        datos = {}
        for linea in contenido.split('\n'):
            if ': ' in linea:
                clave, valor = linea.split(': ', 1)
                datos[clave] = valor
        
        mensaje_codificado = datos.get('Mensaje codificado')
        codigos = ast.literal_eval(datos.get('Código de cada caracter', '{}'))
        
        if not mensaje_codificado or not codigos:
            print("Error: No se encontró la información necesaria en el archivo.")
            return
        
        mensaje_decodificado = decodificar_huffman(mensaje_codificado, codigos)
        print("Mensaje decodificado:", mensaje_decodificado)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{nombre_archivo}'.")
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")



def manejar_compresion_automatica_aritmetica(mensaje=None):
    # Si no se pasa un mensaje (es None), pedimos al usuario que lo introduzca
    if mensaje is None:
        mensaje = input("Introduce el mensaje a comprimir: ")

    frecuencias = Counter(mensaje)
    k = 8  # Tamaño de los enteros en bits (definido por nosotros)
    T = sum(frecuencias.values())  # Total de frecuencias
    n = len(mensaje)  # Tamaño del mensaje

    # Codificar el mensaje usando codificación aritmética con enteros
    bits_codificados = int_arith_code(mensaje, k, frecuencias)
    num_bits_codificados = len(bits_codificados)

    # Tasa de compresión
    bits_originales = n * 8  # Cada carácter es de 8 bits
    tasa_compresion = num_bits_codificados / bits_originales

    # Mostrar los resultados
    print("\n--- Compresión Aritmética Automática ---")
    print("Mensaje codificado:", ''.join(map(str, bits_codificados)))
    print("Tabla de frecuencias:", frecuencias)
    print(f"k (bits por carácter): {k}")
    print(f"T (total de frecuencias): {T}")
    print(f"n (longitud del mensaje): {n}")
    print(f"Tasa de compresión: {tasa_compresion}")

    # Guardar los resultados en un archivo
    num_archivo = input("Introduce un número para el archivo de salida: ")
    with open(f"codificacion{num_archivo}.log", "w", encoding='utf-8') as archivo:
        archivo.write("Método: Aritmética\n")
        archivo.write("Modo: Automático\n")
        archivo.write(f"Mensaje original: {mensaje}\n")
        archivo.write(f"Mensaje codificado (en bits): {''.join(map(str, bits_codificados))}\n")
        archivo.write(f"Tabla de frecuencias: {frecuencias}\n")
        archivo.write(f"k (bits por carácter): {k}\n")
        archivo.write(f"T (total de frecuencias): {T}\n")
        archivo.write(f"n (longitud del mensaje): {n}\n")
        archivo.write(f"Tasa de compresión: {tasa_compresion}\n")

def manejar_compresion_no_automatica_aritmetica():
    mensaje = input("Introduce el mensaje a comprimir: ")
    print("Introduce la tabla de frecuencias (carácter y frecuencia separados por espacio, una línea por carácter).")
    print("Nota: Para el espacio, ingresa 'espacio' seguido de su frecuencia (ejemplo: 'espacio 1').")
    print("Cuando termines, escribe 'fin'.")
    frecuencias_usuario = {}

    # Leer la tabla de frecuencias ingresada por el usuario
    while True:
        entrada = input().strip()
        if entrada.lower() == 'fin':
            break
        
        # Validación de que se ingresen dos valores separados (carácter y frecuencia)
        partes = entrada.split()
        if len(partes) != 2:
            print("Error: Debes ingresar un carácter seguido de su frecuencia. Ejemplo: 'a 3'. Inténtalo de nuevo.")
            continue

        caracter, frecuencia_str = partes[0], partes[1]

        # Manejo del carácter de espacio
        if caracter == 'espacio':
            caracter = ' '  # Convertimos 'espacio' a un espacio real

        try:
            frecuencia = int(frecuencia_str)
            frecuencias_usuario[caracter] = frecuencia
        except ValueError:
            print("Error: Debes ingresar un número válido para la frecuencia. Inténtalo de nuevo.")
            continue

    # Verificar si las frecuencias ingresadas coinciden con las frecuencias reales en el mensaje
    frecuencias_reales = Counter(mensaje)

    # Validar que todos los caracteres en el mensaje estén en la tabla de frecuencias
    for caracter, frecuencia_real in frecuencias_reales.items():
        if caracter not in frecuencias_usuario:
            print(f"Error: El carácter '{caracter}' no está presente en la tabla de frecuencias.")
            print("Pasando a compresión automática con el mismo mensaje...")
            manejar_compresion_automatica_aritmetica(mensaje)  # Llamar al modo automático con el mismo mensaje
            return
        elif frecuencias_usuario[caracter] != frecuencia_real:
            print(f"Error: La frecuencia del carácter '{caracter}' es incorrecta. Frecuencia real: {frecuencia_real}, pero se ingresó: {frecuencias_usuario[caracter]}.")
            print("Pasando a compresión automática con el mismo mensaje...")
            manejar_compresion_automatica_aritmetica(mensaje)  # Llamar al modo automático con el mismo mensaje
            return

    # Validar que ningún carácter de la tabla esté ausente en el mensaje
    for caracter in frecuencias_usuario:
        if caracter not in mensaje:
            print(f"Error: El carácter '{caracter}' fue ingresado en la tabla de frecuencias, pero no está presente en el mensaje.")
            print("Pasando a compresión automática con el mismo mensaje...")
            manejar_compresion_automatica_aritmetica(mensaje)  # Llamar al modo automático con el mismo mensaje
            return

    # Solicitar el valor de k
    k = int(input("Introduce el valor de k (bits por carácter): "))

    T = sum(frecuencias_usuario.values())

    # Validación de k: debe cumplir que k >= 4T
    if k < 4 * T:
        print(f"Error: El valor de k debe ser al menos 4T (T = {T}). k debe ser >= {4 * T}.")
        print("Pasando a compresión automática con el mismo mensaje...")
        manejar_compresion_automatica_aritmetica(mensaje)  # Llamar al modo automático con el mismo mensaje
        return

    # Codificar el mensaje usando codificación aritmética con enteros
    bits_codificados = int_arith_code(mensaje, k, frecuencias_usuario)

    # Tasa de compresión
    n = len(mensaje)  # Tamaño del mensaje
    bits_originales = n * 8  # Cada carácter es de 8 bits
    tasa_compresion = len(bits_codificados) / bits_originales

    # Mostrar los resultados
    print("\n--- Compresión No Automática (Aritmética con Enteros) ---")
    print("Mensaje codificado (en bits):", ''.join(map(str, bits_codificados)))
    print("Tabla de frecuencias:", frecuencias_usuario)
    print(f"k (bits por carácter): {k}")
    print(f"T (total de frecuencias): {T}")
    print(f"n (longitud del mensaje): {n}")
    print(f"Tasa de compresión: {tasa_compresion}")

    # Guardar los resultados en un archivo
    num_archivo = input("Introduce un número para el archivo de salida: ")
    with open(f"codificacion{num_archivo}.log", "w", encoding='utf-8') as archivo:
        archivo.write("Método: Aritmética\n")
        archivo.write("Modo: No Automático\n")
        archivo.write(f"Mensaje original: {mensaje}\n")
        archivo.write(f"Mensaje codificado (en bits): {''.join(map(str, bits_codificados))}\n")
        archivo.write(f"Tabla de frecuencias: {frecuencias_usuario}\n")
        archivo.write(f"k (bits por carácter): {k}\n")
        archivo.write(f"T (total de frecuencias): {T}\n")
        archivo.write(f"n (longitud del mensaje): {n}\n")
        archivo.write(f"Tasa de compresión: {tasa_compresion}\n")

def parse_counter(counter_string):
    pairs = re.findall(r"'(.)':\s*(\d+)", counter_string)
    return {key: int(value) for key, value in pairs}

def decodificar_aritmetica_desde_archivo():
    nombre_archivo = input("Introduce el nombre del archivo .log: ")
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
        
        datos = {}
        for linea in contenido.split('\n'):
            if ': ' in linea:
                clave, valor = linea.split(': ', 1)
                datos[clave] = valor
        
        mensaje_codificado = datos.get('Mensaje codificado (en bits)')
        k = int(datos.get('k (bits por carácter)'))
        n = int(datos.get('n (longitud del mensaje)'))
        frecuencias = parse_counter(datos.get('Tabla de frecuencias', ''))
        
        if not all([mensaje_codificado, k, n, frecuencias]):
            print("Error: No se encontró toda la información necesaria en el archivo.")
            return
        
        mensaje_decodificado = int_arith_decode(mensaje_codificado, k, n, frecuencias)
        print("Mensaje decodificado:", mensaje_decodificado)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{nombre_archivo}'.")
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        import traceback
        traceback.print_exc()  # Esto imprimirá el traceback completo para depuración


# Función para mostrar el submenú para Huffman
def mostrar_submenu_huffman():
    while True:
        print("\n--- Submenú Huffman ---")
        print("1. Codificación automática")
        print("2. Codificación no automática")
        print("3. Decodificación")
        print("4. Volver al menú principal")
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            manejar_compresion_automatica_huffman()
        elif opcion == "2":
            manejar_compresion_no_automatica_huffman()
        elif opcion == "3":
            decodificar_huffman_desde_archivo()
        elif opcion == "4":
             break 
        else:
            print("Opción no válida. Intenta de nuevo.")


# Agregar al submenú de aritmética
def mostrar_submenu_aritmetica():
    while True:
        print("\n--- Submenú Aritmética ---")
        print("1. Codificación automática")
        print("2. Codificación no automática")
        print("3. Decodificación")
        print("4. Volver al menú principal")
        
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            manejar_compresion_automatica_aritmetica()
        elif opcion == "2":
            manejar_compresion_no_automatica_aritmetica()
        elif opcion == "3":
            decodificar_aritmetica_desde_archivo()
        elif opcion == "4":
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

# Función principal para mostrar el menú principal
def mostrar_menu_principal():
    while True:
        print("\n--- Menú Principal ---")
        print("1. Huffman")
        print("2. Aritmética")  
        print("3. Salir")
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            mostrar_submenu_huffman()
        elif opcion == "2":
            mostrar_submenu_aritmetica()  
        elif opcion == "3":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    mostrar_menu_principal()
