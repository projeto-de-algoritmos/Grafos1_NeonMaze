import pygame as py #biblioteca para criar o jogo
from random import choice, randrange #biblioteca para escolher aleatoriamente um elemento de uma lista

#resolução da tela
largura = 1080
altura = 656

#tamanho do bloco
bloco = 32

#numero de linhas e colunas do tabuleiro
cols, rows = largura // bloco, altura // bloco # a quantidade de linhas e colunas é igual ao tamanho da tela dividido pelo tamanho do bloco

#criando a classe da celula
class Celula:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.paredes = {'encima': True, 'direita': True, 'embaixo': True, 'esquerda': True} #cria um dicionário com as paredes da celula
        self.visitado = False #cria um atributo para verificar se a celula já foi visitada

    #desenha as paredes da celula
    def mostrar_paredes(self, tela):
        x = self.x * bloco
        y = self.y * bloco

        #se a celula já foi visitada, ela é pintada de preto --> desativei a pintura de preto para a visualização do backgroud
        #if self.visitado:
            #py.draw.rect(tela, (0, 0, 0), (x, y, bloco, bloco))
        
        #se a celula ainda não foi visitada, ela é pintada de branco
        if self.paredes['encima']:
            py.draw.line(tela, (255, 255, 255), (x, y), (x + bloco, y), 4) #desenha a parede de cima
        if self.paredes['direita']:
            py.draw.line(tela, (255, 255, 255), (x + bloco, y), (x + bloco, y + bloco), 4) #desenha a parede da direita
        if self.paredes['embaixo']:
            py.draw.line(tela, (255, 255, 255), (x + bloco, y + bloco), (x, y + bloco), 4) #desenha a parede de baixo
        if self.paredes['esquerda']:
            py.draw.line(tela, (255, 255, 255), (x, y + bloco), (x, y), 4) #desenha a parede da esquerda
    
    #desenha a celula atual
    def desenha_celula_atual(self, tela):
        x = self.x * bloco
        y = self.y * bloco
        py.draw.rect(tela, (0, 255, 0), (x, y, bloco, bloco)) #pinta a celula atual de verde
    
    def get_rects(self): #retorna os retângulos das paredes da celula para verificar colisão com o jogador
        rects = []
        x, y = self.x * bloco, self.y * bloco
        if self.paredes['encima']:
            rects.append(py.Rect( (x, y), (bloco, 4) ))
        if self.paredes['direita']:
            rects.append(py.Rect( (x + bloco, y), (4, bloco) ))
        if self.paredes['embaixo']:
            rects.append(py.Rect( (x, y + bloco), (bloco , 4) ))
        if self.paredes['esquerda']:
            rects.append(py.Rect( (x, y), (4, bloco) ))
        return rects
    
    # verifica se a celula está na borda do tabuleiro e retorna o indice na lista de celulas
    def verifica_celula(self, x, y):
        index = lambda x, y: x + y * cols #cria uma função lambda para calcular o index da celula na lista a partir da posição x e y na matriz
        if x < 0 or y < 0 or x > cols - 1 or y > rows - 1: #verifica se a celula está fora dos limites do labirinto
            return False 
        return self.grid[index(x, y)] #retorna a celula atual se ela estiver dentro dos limites do labirinto

    def verifica_vizinhos(self, grid):
        self.grid = grid #recebe a lista de celulas para verificar os vizinhos da celula atual 
        vizinhos = []
        vizinhoDeCima = self.verifica_celula(self.x, self.y - 1) #verifica se a celula de cima existe
        vizinhoDaDireita = self.verifica_celula(self.x + 1, self.y) #verifica se a celula da direita existe
        vizinhoDeBaixo = self.verifica_celula(self.x, self.y + 1) #verifica se a celula de baixo existe
        vizinhoDaEsquerda = self.verifica_celula(self.x - 1, self.y) #verifica se a celula da esquerda existe        

        #se a celula de cima existe e não foi visitada, ela é adicionada na lista de vizinhos
        if vizinhoDeCima and not vizinhoDeCima.visitado:
            vizinhos.append(vizinhoDeCima)
        #se a celula da direita existe e não foi visitada, ela é adicionada na lista de vizinhos
        if vizinhoDaDireita and not vizinhoDaDireita.visitado:
            vizinhos.append(vizinhoDaDireita)
        #se a celula de baixo existe e não foi visitada, ela é adicionada na lista de vizinhos
        if vizinhoDeBaixo and not vizinhoDeBaixo.visitado:
            vizinhos.append(vizinhoDeBaixo)
        #se a celula da esquerda existe e não foi visitada, ela é adicionada na lista de vizinhos
        if vizinhoDaEsquerda and not vizinhoDaEsquerda.visitado:
            vizinhos.append(vizinhoDaEsquerda)
        
        #se a lista de vizinhos não estiver vazia, um vizinho é escolhido aleatoriamente
        return choice(vizinhos) if vizinhos else False
    
def remove_parede(atual, vizinho):  
    dx = atual.x - vizinho.x #calcula a diferença entre a posição x da celula atual e a posição x da celula vizinha
    dy = atual.y - vizinho.y #calcula a diferença entre a posição y da celula atual e a posição y da celula vizinha
        
    #se a diferença for 1, a celula vizinha está a direita da celula atual
    if dx == 1:
        atual.paredes['esquerda'] = False
        vizinho.paredes['direita'] = False
    #se a diferença for -1, a celula vizinha está a esquerda da celula atual
    elif dx == -1:
        atual.paredes['direita'] = False
        vizinho.paredes['esquerda'] = False
    #se a diferença for 1, a celula vizinha está embaixo da celula atual
    if dy == 1:
        atual.paredes['encima'] = False
        vizinho.paredes['embaixo'] = False      
    #se a diferença for -1, a celula vizinha está em cima da celula atual
    elif dy == -1:
        atual.paredes['embaixo'] = False
        vizinho.paredes['encima'] = False

#função para gerar o labirinto
def gera_labirinto(tela):
    #inicializando a celula inicial no canto superior esquerdo do labirinto
    grid = [Celula(col, row) for row in range(rows) for col in range(cols)] #cria uma lista com todas as celulas do labirinto
    celula_atual = grid[0] #define a celula inicial como a primeira celula da lista
    pilha = [] #cria uma pilha para armazenar as celulas visitadas
    contadorDeParada = 1 #contador para parar o loop
    while contadorDeParada != len(grid): #enquanto o contador for diferente do tamanho da lista de celulas, o loop continua
        celula_atual.visitado = True #marca a celula atual como visitada
        #celula_atual.desenha_celula_atual(tela) #pinta a celula atual de verde --> nao precisa mais
        proxima_celula = celula_atual.verifica_vizinhos(grid) #verifica se a celula atual tem vizinhos não visitados
        if proxima_celula: #se a celula atual tiver vizinhos não visitados
            proxima_celula.visitado = True #marca a proxima celula como visitada
            contadorDeParada += 1 #incrementa o contador de parada
            pilha.append(celula_atual) #adiciona a celula atual na pilha de celulas visitadas
            remove_parede(celula_atual, proxima_celula) #remove a parede entre a celula atual e a proxima celula
            celula_atual = proxima_celula #define a proxima celula como a celula atual
        elif pilha: #se a pilha não estiver vazia
            celula_atual = pilha.pop() #remove a ultima celula da pilha e define como a celula atual para continuar o processo de geração do labirinto
    return grid       
    
