import random
def siguienteValor(lista, voyPor):     # dada la lista de TODOS LOS STIM, Y UNA LISTA DE 3 AL AZAR, NOS ASEGURAMOS QUE EL SIGUIENTE ELEMENTO ES PSEUDORANDOM
    voyPor.pop(0)
    heTerminado= 0
    while (heTerminado < 1):
        valor = random.choice(lista)
        v3 = valor[2]
        if (valor not in voyPor) :
            v1 = voyPor[0][2] 
            v2 = voyPor[1][2]
            if(v1 == v2 and v2 != v3 or v1 != v2):  
                voyPor.append(valor)
                heTerminado = 1
                return voyPor
            

def elementoPorPorcentaje (item):
    if item == '100':
        lista = [1,1,1,1]
    elif item == '75':
        lista = [1,1,1,0]
    elif item == '50':
        lista = [1,1,0,0]
    return random.choice(lista) 
