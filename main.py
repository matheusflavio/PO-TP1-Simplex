from matrix import *
from getInputs import *
from simplex import *

def main():
    '''Leitura dos inputs e criação da matrix com VERO para o simplex'''
    (restrictions, variables, matrix) = readInputs()
    primal = Simplex(matrix, restrictions, variables)
    
    '''Checando se há B negativo. Caso não haja, executa o simplex diretamente na PL Primal'''
    negativeB = primal.getNegativesBIndexes()
    if(len(negativeB) == 0):
        primal.simplex()
        return

    '''Criando a PL auxiliar para o simplex dual'''
    auxvariables, auxrestrictions, aux = primal.createAuxMatrix()
    auxSimplex = Simplex(aux, auxrestrictions, auxvariables)
    
    '''Operações iniciais com a PL auxiliar para realizar o simplex dual até o ponto em que é possível identificar a inviabilidade'''
    auxSimplex.handleAux(negativeB)

    '''Testando a viabilidade da PL Auxiliar com a função is close igual sugerido no fórum'''
    if not np.isclose(auxSimplex.getObjetiveValue(), 0):
        print("inviavel")
        printArray(auxSimplex.getCertificate())
        return # Retorno vazio para parar a execução do simplex, uma vez que o resultado é obtido

    '''Preparando e executando os procedimentos da execução final do simplex sobre a PL auxiliar que é modificada a fim de obter todos os resultados'''
    auxSimplex.finalSimplex(primal)

main()