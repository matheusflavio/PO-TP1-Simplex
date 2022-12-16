import numpy as np

def initializeMatrix(restrictions, variables):
    '''Return a matrix of zeros with VERO already configurated with the sizes given as params'''
    matrix = np.zeros((1 + restrictions, 2 * restrictions + variables + 1))
    matrixIndexToFillWithOne = 0

    # creating VERO on the matrix
    for i in range(1, restrictions + 1):
        for j in range(0, restrictions):
            if j == matrixIndexToFillWithOne:
                matrix[i][j] = 1
                matrixIndexToFillWithOne += 1
                break

    return matrix

def createNewPivot(matrix, lineIndex, columnIndex):
    '''Receive a full matrix, a line index and a column index
    and create a pivot on the element of the given indexes'''
    element = matrix[lineIndex, columnIndex]
    matrix[lineIndex] /= element
    element = matrix[lineIndex, columnIndex]

    # creating VERO on the matrix
    for i in range(0, np.shape(matrix)[0]):
        selected = matrix[i][columnIndex]
        if i == lineIndex or selected == 0:
            continue
        factor = -selected / element
        matrix[i] += matrix[lineIndex] * factor

def printArray(arr):
    '''Print all array itens using the format specs'''
    for item in arr:
        print("%.7f" % item, end=" ")
    print()
    
def printNumber(number):
    '''Print the given number using the format specs'''
    print("%.7f" % number, end=" ")
    print()