from matrix import *

class Simplex:
    def __init__(self, matrix, restrictions, variables):
        '''Inicialização da classe com os dados para realizar o simplex'''
        self.matrix = matrix
        self.restrictions = restrictions
        self.variables = variables

    def getNegativesBIndexes(self):
        '''Checa valores negativos em B e retorna todos os índices em que isso acontece'''
        negativeBIndexes = []
        for i in range(1, self.restrictions + 1):
            if(self.matrix[i][2*self.restrictions + self.variables] < 0):
                negativeBIndexes = np.append(negativeBIndexes, i)
        
        return negativeBIndexes

    def createAuxMatrix(self):
        '''Cria a PL auxiliar para o método do simplex dual, além das variáiveis de apoio correspondentes às
        quantidades de restrições e de variáveis da PL auxiliar'''
        aux = self.matrix[1:self.restrictions+1, self.restrictions:2*self.restrictions+self.variables]
        aux = np.concatenate((np.zeros((1, self.variables + self.restrictions)), aux))
        #print(aux)

        intermediary = np.concatenate((np.ones((1, self.restrictions)),np.eye(self.restrictions)))
        aux = np.concatenate((aux,intermediary),axis=1)
        #print(aux)

        b = self.matrix[0:self.restrictions+1, 2*self.restrictions + self.variables:]
        aux = np.concatenate((aux, b), axis=1)
        #print(aux)

        intermediary = np.concatenate((np.zeros((1, self.restrictions)), np.eye(self.restrictions)))
        aux = np.concatenate((intermediary, aux), axis=1)
        #print(aux)

        variables = self.variables + self.restrictions
        restrictions = self.restrictions

        return variables, restrictions, aux

    def checkIfCIsPositive(self):
        '''Checando se todos os valores do vetor C são >= 0'''
        c = self.matrix[0:1, self.restrictions:2*self.restrictions + self.variables]
        for item in c[0]:
            if(item < 0):
                return False
        return True

    def getObjetiveValue(self):
        '''Retorna o valor da Função Objetivo'''
        return self.matrix[0][2*self.restrictions + self.variables]

    def getSolutionArray(self):
        '''Retorna o vetor que é a solução atual da PL segundo o simplex'''
        solution = np.zeros((0))
        for j in range(self.restrictions, self.restrictions + self.variables):
            if(self.matrix[0][j] == 0):
                aux, _ = self.getVariableValue(j)
                solution = np.append(solution, aux)
            else:
                solution = np.append(solution, 0)
        return solution

    def getPivotElementAndIndex(self):
        '''Seleciona e pivotea o próximo pivô para o método simplex. Retorna os índices da linha e coluna desse elemento'''
        selectedColumn = 0

        '''Procura pelo primeiro elemento negativo para otimalizar os valores da função'''
        for c in range(self.restrictions, 2*self.restrictions + self.variables):
            if(self.matrix[0][c] < 0):
                selectedColumn = c
                break

        minDivision = float('inf')
        pivotLine = 0

        '''Procura o elemento positivo da coluna selecionada que possui o menor resultado de divisão para ser o pivô'''
        for i in range(1, self.restrictions + 1):
            if(self.matrix[i][selectedColumn] > 0):
                actualDivision = self.matrix[i,2*self.restrictions + self.variables]/self.matrix[i][selectedColumn]
                if(actualDivision < minDivision):
                    '''Atualização do valor da menor divisão'''
                    minDivision = actualDivision
                    pivotLine = i
        
        if(pivotLine == 0):
            '''-1 é uma flag para identicar que a PL é ilimitada'''
            return -1, selectedColumn 

        '''Caso não ative a flag acima, retorna os índices'''
        return pivotLine, selectedColumn

    def getVariableValue(self, columnIndex):
        '''Retorna o valor da variável na função objetivo fazendo uso da solução simples final'''
        indexOfOne = 0
        index = 1
        for item in self.matrix[1:, columnIndex]:
            if(item != 0 and item != 1):
                return 0, 0
            if(item == 1):
                if(indexOfOne == 0):
                    indexOfOne = index
                    index += 1
                    continue
                else:
                    return 0, 0
            index += 1
        
        return self.matrix[indexOfOne, 2*self.restrictions + self.variables], indexOfOne

    def getInfinityCertificate(self, column):
        '''Return d vector as the unbounded certificate'''
        cColumn = column - self.restrictions
        d = np.zeros(self.variables + self.restrictions)
        d[cColumn] = 1

        index = 0
        for j in range(self.restrictions, self.restrictions + self.variables):
            if(index == cColumn):
                index += 1
                continue

            if(self.matrix[0][j] == 0):
                _, indexOfOne = self.getVariableValue(j)
                val = self.matrix[indexOfOne][column] * -1
                d[index] = val
            else:
                d[index] = 0

            index += 1
        
        d = d[:self.variables]
        printArray(d)
        return d

    def getCertificate(self):
        '''Retorna o certificado encontrado'''
        return self.matrix[0:1, 0:self.restrictions][0]

    def getOriginalC(self):
        '''Retorna a o valor original de c'''
        aux = self.matrix[0:1, self.restrictions:2*self.restrictions + self.variables]
        return aux

    def resetVero(self):
        '''Reseta o valor do VERO que armazena o registro de operações para 0'''
        for j in range(self.restrictions):
            self.matrix[0][j] = 0

    def handleAux(self, negativeB):
        '''Realiza todas as operações com a PL auxiliar até o ponto em que é possível definir se é inviável ou não'''

        '''Multiplicando as linhas cujos B são negativos por -1'''
        for line in negativeB:
            self.matrix[int(line)] *= -1

        '''Subtraindo todas as linhas da linha 0, que é a linha da função objetivo'''
        for line in self.matrix[1:]:
            self.matrix[0] -= line
        '''Execução do simplex para a PL Dual'''
        self.simplex(False)

    def finalSimplex(self, primal):
        '''Preparo e execução final do simplex para obter todos os resultados, dado que a PL não é inviável'''

        '''Pegando a solução da PL auxiliar'''
        auxSolution = self.getSolutionArray()

        '''Pegando o vetor c original e colcando na PL auxiliar'''
        cOriginal = primal.getOriginalC()
        self.matrix[0:1, self.restrictions:self.restrictions + self.variables] = cOriginal

        '''Gerando lista de colunas para remoção'''
        columnToRemove = []
        for i in range(2*primal.restrictions + primal.variables, 3*primal.restrictions + primal.variables):
            columnToRemove.append(i)
        
        '''Removendo colunas e resetando o VERO da PL aux'''
        self.matrix = np.delete(self.matrix, columnToRemove, axis=1)
        self.resetVero()

        '''Criando todos os pivôs necessários para a execução final do simplex'''
        index = 0
        for x in auxSolution:
            if x > 0:
                col = self.restrictions + index
                line = 0
                lineIndex = 1
                for i in self.matrix[1:, col]:
                    if i == 1:
                        line = lineIndex
                        break
                    lineIndex += 1
                createNewPivot(self.matrix, line, col)    
            index += 1
        
        '''Execução final do simplex com as modificações necessárias feitas'''
        finalSimplex = Simplex(self.matrix, primal.restrictions, primal.variables)
        finalSimplex.simplex()

    def simplex(self, usingDefaultPL = True):
        '''Executa todas as chamadas do método simplex'''

        '''Caso todos os valores de C são positivos e está na PL Primal, é uma solução ótima para a PL'''
        if(self.checkIfCIsPositive()):
            if(usingDefaultPL):
                print('otima')
                printNumber(self.getObjetiveValue())
                printArray(self.getSolutionArray())
                printArray(self.getCertificate())

            return # Retorno vazio para parar a execução do simplex, uma vez que o resultado é obtido

        '''Selecionando os indexes de linha e coluna para criar o pivô'''
        pivotLine, pivot_column = self.getPivotElementAndIndex()
        '''Identificação de PL ilimitada'''
        if(pivotLine == -1):
            if(usingDefaultPL):
                print("ilimitada")
                printArray(self.getSolutionArray())
                self.getInfinityCertificate(pivot_column)
            return # Retorno vazio para parar a execução do simplex, uma vez que o resultado é obtido

        '''Criação de um novo pivô para continuar com o método simplex'''
        createNewPivot(self.matrix, pivotLine, pivot_column)

        '''Nova chamada do simplex para continuar aplicando o método após criação do novo pivô'''
        self.simplex(usingDefaultPL)