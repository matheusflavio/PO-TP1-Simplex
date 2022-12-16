import numpy as np

def readFirstLine():
    restrictions, variables = input().split()
    return (int(restrictions), int(variables))

def createInitialMatrix(restrictions, variables):
    matrix = np.zeros((1 + restrictions, 2 * restrictions + variables + 1))
    matrix[1:1+restrictions,0:restrictions] = np.eye(restrictions)
    return matrix

def readVectorC(variables):
    inputRead = input().split()
    vectorC = np.zeros(variables)
    for i in range(variables):
        vectorC[i] = -float(inputRead[i])
    return vectorC

def readRestrictionsLines(restrictions, variables, matrix):
    for i in range(restrictions):
        inputRead = input().split()
        array = np.zeros(variables)
        for j in range(variables):
            array[j] = float(inputRead[j])
        matrix[1+i,restrictions:restrictions+variables] = array
        matrix[1+i][-1] = float(inputRead[-1])

def readInputs():
    # Lendo as quantidades de variáveis e restrições
    restrictions, variables = readFirstLine()

    # Cria uma matrix de zeros já com sub matriz identidade referente ao VERO
    matrix = createInitialMatrix(restrictions, variables)

    # Lendo e colocando -c na posicação correta da matrix VERO
    matrix[0][restrictions:restrictions+variables] = readVectorC(variables)

    # Lendo e colocando as restrições na matrix com o VERO
    readRestrictionsLines(restrictions, variables, matrix)

    # Colocando 1 para os elementos correspondentes às variáveis adicionais
    matrix[1:1+restrictions,restrictions+variables:2 * restrictions + variables] = np.eye(restrictions)

    return (restrictions, variables, matrix)