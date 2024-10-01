import re
from collections import Counter

def int_arith_code(mensaje_original, k):
    frecuencias = Counter(mensaje_original)
    R = 2 ** k  # Precisión que usamos en los cálculos
    l, u = 0, R - 1  # Inicializar los límites
    T = sum(frecuencias.values())  # Suma total de las frecuencias

    # Construir los límites f(i) y f(i+1) basados en las frecuencias acumuladas
    limites = {}
    acumulado = 0
    for simbolo, frecuencia in frecuencias.items():
        limites[simbolo] = (acumulado, acumulado + frecuencia)
        acumulado += frecuencia

    # Codificación del mensaje
    for simbolo in mensaje_original:
        s = u - l + 1
        f_i, f_i_plus_1 = limites[simbolo]
        
        # Ajustar los límites superior e inferior
        u = l + (s * f_i_plus_1) // T - 1
        l = l + (s * f_i) // T

        # Renormalización
        while True:
            if u < R // 2:
                l = 2 * l
                u = 2 * u + 1
            elif l >= R // 2:
                l = 2 * (l - R // 2)
                u = 2 * (u - R // 2) + 1
            elif l >= R // 4 and u < 3 * R // 4:
                l = 2 * (l - R // 4)
                u = 2 * (u - R // 4) + 1
            else:
                break

    # Retornar el valor codificado como un número binario
    codigo = (l + u) // 2  # Tomamos el valor intermedio entre `l` y `u`
    return bin(codigo)[2:], len(mensaje_original), frecuencias  # Convertir a binario sin el prefijo "0b"

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
        
        for simbolo, (f_i, f_i_plus_1) in limites.items():
            if f_i <= valor < f_i_plus_1:
                mensaje_decodificado.append(simbolo)
                u = l + (s * f_i_plus_1) // T - 1
                l = l + (s * f_i) // T
                break
        
        # Renormalización
        while True:
            if u < R // 2:
                l = 2 * l
                u = 2 * u + 1
                codigo = 2 * codigo
            elif l >= R // 2:
                l = 2 * (l - R // 2)
                u = 2 * (u - R // 2) + 1
                codigo = 2 * (codigo - R // 2)
            elif l >= R // 4 and u < 3 * R // 4:
                l = 2 * (l - R // 4)
                u = 2 * (u - R // 4) + 1
                codigo = 2 * (codigo - R // 4)
            else:
                break
            
            if l >= R:
                l -= R
                u -= R
                codigo -= R
    
    return ''.join(mensaje_decodificado)

def main():
    # Entrada del mensaje original
    mensaje_original = input("Introduce el mensaje a codificar: ")
    
    # Elegir valor para k
    k = 48  # Puedes cambiar este valor según tus necesidades
    
    # Codificación
    print("\nCodificando el mensaje original...")
    mensaje_codificado, n, frecuencias = int_arith_code(mensaje_original, k)
    print("Mensaje codificado (en bits):", mensaje_codificado)
    
    # Decodificación
    print("\nDecodificando el mensaje codificado...")
    mensaje_decodificado = int_arith_decode(mensaje_codificado, k, n, frecuencias)
    print("Mensaje decodificado:", mensaje_decodificado)
    
    # Verificar si la decodificación es igual al mensaje original
    if mensaje_original == mensaje_decodificado:
        print("\n¡La codificación y decodificación fueron exitosas!")
    else:
        print("\nError: el mensaje decodificado no coincide con el original.")

if __name__ == "__main__":
    main()
