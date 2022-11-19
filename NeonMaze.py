import pygame as py #biblioteca para criar o jogo
from random import choice #biblioteca para escolher aleatoriamente um elemento de uma lista

#resolução da tela
largura = 1080
altura = 656

#tamanho do bloco
bloco = 32

#numero de linhas e colunas do tabuleiro
cols, rows = largura // bloco, altura // bloco # a quantidade de linhas e colunas é igual ao tamanho da tela dividido pelo tamanho do bloco

#criando uma estrutura padrão do pygame
py.init() #inicializa o pygame
tela = py.display.set_mode((largura, altura)) #cria a tela
py.display.set_caption("Neon Maze") #define o título da janela
clock = py.time.Clock() #cria um relógio para controlar a velocidade do jogo

#carregando imagens
fundo = py.image.load("background.png") #carrega a imagem de fundo
fundo = py.transform.scale(fundo, (largura, altura)) #redimensiona a imagem de fundo para o tamanho da tela
fundo = py.transform.smoothscale(fundo, (largura, altura)) #aplica um filtro de suavização na imagem de fundo

#carregando musica
py.mixer.init() #inicializa o mixer do pygame
py.mixer.music.load('music/Castelvania2.mp3') #carrega a música que será tocada no jogo
py.mixer.music.set_volume(1) #define o volume da música de fundo
py.mixer.music.play(-1) #reproduz a música de fundo em loop

#criando a classe da celula
class Celula:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.paredes = {'encima': True, 'direita': True, 'embaixo': True, 'esquerda': True} #cria um dicionário com as paredes da celula
        self.visitado = False #cria um atributo para verificar se a celula já foi visitada

    #desenha as paredes da celula
    def mostrar_paredes(self):
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
    def desenha_celula_atual(self):
        x = self.x * bloco
        y = self.y * bloco
        py.draw.rect(tela, (0, 255, 0), (x, y, bloco, bloco)) #pinta a celula atual de verde
    
    # verifica se a celula está na borda do tabuleiro e retorna o indice na lista de celulas
    def verifica_celula(self, x, y):
        index = lambda x, y: x + y * cols #cria uma função lambda para calcular o index da celula na lista a partir da posição x e y na matriz
        if x < 0 or y < 0 or x > cols - 1 or y > rows - 1: #verifica se a celula está fora dos limites do labirinto
            return False 
        return grid[index(x, y)] #retorna a celula atual se ela estiver dentro dos limites do labirinto

    def verifica_vizinhos(self):
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

#inicializando a celula inicial no canto superior esquerdo do labirinto
grid = [Celula(col, row) for row in range(rows) for col in range(cols)] #cria uma lista com todas as celulas do labirinto
celula_atual = grid[0] #define a celula inicial como a primeira celula da lista
pilha = [] #cria uma pilha para armazenar as celulas visitadas

#loop principal do jogo para:
# 1) atualizar a tela
# 2) verificar eventos
# 3) atualizar o jogo
# 4) desenhar o jogo
# 5) controlar a velocidade do jogo (Taxa de quadros por segundo - FPS)
# 6) verificar se o jogo deve ser encerrado

rodando = True
while rodando:
    # Desenhando o fundo
    tela.fill(py.Color("black")) #preenche a tela com a cor preta (background)
    tela.blit(fundo, (0, 0)) #desenha a imagem de fundo na tela (background)

    for event in py.event.get(): #verifica os eventos
        if event.type == py.QUIT: #se o evento for o botão de fechar a janela
            py.mixer.music.stop() #para a música de fundo
            rodando = False #encerra o jogo
            exit() #encerra o programa
    
    [cell.mostrar_paredes() for cell in grid] #desenha as paredes de todas as celulas do labirinto na tela
    celula_atual.visitado = True #marca a celula atual como visitada
    celula_atual.desenha_celula_atual() #pinta a celula atual de verde

    proxima_celula = celula_atual.verifica_vizinhos() #verifica se a celula atual tem vizinhos não visitados
    if proxima_celula: #se a celula atual tiver vizinhos não visitados
        proxima_celula.visitado = True #marca a proxima celula como visitada
        pilha.append(celula_atual) #adiciona a celula atual na pilha de celulas visitadas
        remove_parede(celula_atual, proxima_celula) #remove a parede entre a celula atual e a proxima celula
        celula_atual = proxima_celula #define a proxima celula como a celula atual
    elif pilha: #se a pilha não estiver vazia
        celula_atual = pilha.pop() #remove a ultima celula da pilha e define como a celula atual para continuar o processo de geração do labirinto
        



    py.display.flip() #atualiza a tela
    clock.tick(60) #controla a velocidade do jogo

