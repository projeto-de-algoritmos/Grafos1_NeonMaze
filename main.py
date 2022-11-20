import pygame as py  # biblioteca para criar o jogo
# biblioteca para escolher aleatoriamente um elemento de uma lista
from random import choice
from button import *
import sys

# resolução da tela
largura = 1350
altura = 670

# tamanho do bloco
bloco = 50

# numero de linhas e colunas do tabuleiro
# a quantidade de linhas e colunas é igual ao tamanho da tela dividido pelo tamanho do bloco
cols, rows = largura // bloco, altura // bloco

# criando uma estrutura padrão do pygame
py.init()  # inicializa o pygame
tela = py.display.set_mode((largura, altura))  # cria a tela
py.display.set_caption("Neon Maze")  # define o título da janela
clock = py.time.Clock()  # cria um relógio para controlar a velocidade do jogo

# carregando imagens
fundo = py.image.load("img/neonCity.jpg")  # carrega a imagem de fundo
# redimensiona a imagem de fundo para o tamanho da tela
fundo = py.transform.scale(fundo, (largura, altura))
# aplica um filtro de suavização na imagem de fundo
fundo = py.transform.smoothscale(fundo, (largura, altura))
fundo2 = py.image.load("img/neonCity2.png")
fundo2 = py.transform.scale(fundo2, (largura, altura))
fundo2 = py.transform.smoothscale(fundo2, (largura, altura))
fundo3 = py.image.load("img/bondeDosEt.png")
fundo3 = py.transform.scale(fundo3, (largura, altura))
fundo3 = py.transform.smoothscale(fundo3, (largura, altura))

# carregando musica
py.mixer.init()  # inicializa o mixer do pygame
# carrega a música que será tocada no jogo
py.mixer.music.load('music/topGear.mp3')
py.mixer.music.set_volume(1)  # define o volume da música de fundo
py.mixer.music.play(-1)  # reproduz a música de fundo em loop


# configurando o jogador
player_speed = 5
player_img = py.image.load('img/etzinho.png').convert_alpha()
player_img = py.transform.scale(player_img, (bloco - 2 * 4, bloco - 2 * 4))
player_rect = player_img.get_rect()
player_rect.center = bloco // 2, bloco // 2
directions = {'a': (-player_speed, 0), 'd': (player_speed, 0),
              'w': (0, -player_speed), 's': (0, player_speed),
              'left': (-player_speed, 0), 'right': (player_speed, 0),
              'up': (0, -player_speed), 'down': (0, player_speed)}
teclas = {'a': py.K_a, 'd': py.K_d, 'w': py.K_w, 's': py.K_s,
          'left': py.K_LEFT, 'right': py.K_RIGHT, 'up': py.K_UP, 'down': py.K_DOWN}
direction = (0, 0)

celula_final_img = py.image.load('img/bondeDosET.png').convert_alpha()
celula_final_img = py.transform.scale(
    celula_final_img, (bloco - 2 * 4, bloco - 2 * 4))
celula_final_rect = celula_final_img.get_rect()
celula_final_rect.center = (cols - 1) * bloco + \
    bloco // 2, (rows - 1) * bloco + bloco // 2

celula_atual_img = py.image.load('img/pacman.png').convert_alpha()
celula_atual_img = py.transform.scale(
    celula_atual_img, (bloco - 2 * 4, bloco - 2 * 4))
celula_atual_rect = celula_atual_img.get_rect()
celula_atual_rect.center = bloco // 2, bloco // 2


# verifica se o jogador colidiu com alguma parede
def is_collide(x, y):
    tmp_rect = player_rect.move(x, y)
    if tmp_rect.collidelist(colisõesDeParedes) == -1:
        return False
    return True

# criando o menu principal


def menu():
    while True:
        # coloca a imagem de fundo na tela
        tela.blit(fundo2, (0, 0))
        # cria os textos do menu com a fonte neon na pasta font
        txt1 = py.font.Font('font/Monoton-Regular.ttf', 100).render('Neon Maze',
                            True, ("Blue")).get_rect(center=(largura // 2, altura // 2 - 200))
        txt2 = py.font.Font('font/Monoton-Regular.ttf', 20).render('Pressione qualquer tecla para começar',
                            True, ("Blue")).get_rect(center=(largura // 2, altura // 2 + 200))
        # coloca os textos na tela
        tela.blit(py.font.Font('font/Monoton-Regular.ttf',
                  100).render('Neon Maze', True, ("Gold")), txt1)
        tela.blit(py.font.Font('font/Monoton-Regular.ttf', 20).render(
        'Pressione        qualquer        tecla        para        começar', True, ("Gold")), txt2)

        # atualiza a tela
        py.display.update()
        # verifica se alguma tecla foi pressionada
        for event in py.event.get():
            if event.type == py.KEYDOWN:
                # se alguma tecla foi pressionada, sai do loop e inicia o jogo
                return True
            if event.type == py.QUIT:
                py.quit()
                exit()

# criando a classe da celula


class Celula:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # cria um dicionário com as paredes da celula
        self.paredes = {'encima': True, 'direita': True,
                        'embaixo': True, 'esquerda': True}
        self.visitado = False  # cria um atributo para verificar se a celula já foi visitada

    def get_rects(self):  # retorna os retângulos das paredes da celula para verificar colisão com o jogador
        rects = []
        x, y = self.x * bloco, self.y * bloco
        if self.paredes['encima']:
            rects.append(py.Rect((x, y), (bloco, 4)))
        if self.paredes['direita']:
            rects.append(py.Rect((x + bloco, y), (4, bloco)))
        if self.paredes['embaixo']:
            rects.append(py.Rect((x, y + bloco), (bloco, 4)))
        if self.paredes['esquerda']:
            rects.append(py.Rect((x, y), (4, bloco)))
        return rects

    # desenha as paredes da celula
    def mostrar_paredes(self):
        x = self.x * bloco
        y = self.y * bloco

        # se a celula já foi visitada, ela é pintada de preto --> desativei a pintura de preto para a visualização do backgroud
        # if self.visitado:
        #py.draw.rect(tela, (0, 0, 0), (x, y, bloco, bloco))

        # se a celula ainda não foi visitada, ela é pintada de dourado
        if self.paredes['encima']:
            # desenha a parede de cima
            py.draw.line(tela, ("Gold"), (x, y), (x + bloco, y), 4)
        if self.paredes['direita']:
            # desenha a parede da direita
            py.draw.line(tela, ("Gold"), (x + bloco, y),
                         (x + bloco, y + bloco), 4)
        if self.paredes['embaixo']:
            py.draw.line(tela, ("Gold"), (x + bloco, y + bloco),
                         (x, y + bloco), 4)  # desenha a parede de baixo
        if self.paredes['esquerda']:
            # desenha a parede da esquerda
            py.draw.line(tela, ("Gold"), (x, y + bloco), (x, y), 4)

    # desenha a celula atual
    def desenha_celula_atual(self):
        x = self.x * bloco
        y = self.y * bloco
        tela.blit(celula_atual_img, (x, y))

    # desenha a celula de destino
    def desenha_celula_final(self):
        x = self.x * bloco
        y = self.y * bloco
        # coloca a imagem da celula final na tela
        tela.blit(celula_final_img, (x, y))

    # verifica se a celula está na borda do tabuleiro e retorna o indice na lista de celulas
    def verifica_celula(self, x, y):
        # cria uma função lambda para calcular o index da celula na lista a partir da posição x e y na matriz
        def index(x, y): return x + y * cols
        # verifica se a celula está fora dos limites do labirinto
        if x < 0 or y < 0 or x > cols - 1 or y > rows - 1:
            return False
        # retorna a celula atual se ela estiver dentro dos limites do labirinto
        return grid[index(x, y)]

    def verifica_vizinhos(self):
        vizinhos = []
        # verifica se a celula de cima existe
        vizinhoDeCima = self.verifica_celula(self.x, self.y - 1)
        # verifica se a celula da direita existe
        vizinhoDaDireita = self.verifica_celula(self.x + 1, self.y)
        # verifica se a celula de baixo existe
        vizinhoDeBaixo = self.verifica_celula(self.x, self.y + 1)
        # verifica se a celula da esquerda existe
        vizinhoDaEsquerda = self.verifica_celula(self.x - 1, self.y)

        # se a celula de cima existe e não foi visitada, ela é adicionada na lista de vizinhos
        if vizinhoDeCima and not vizinhoDeCima.visitado:
            vizinhos.append(vizinhoDeCima)
        # se a celula da direita existe e não foi visitada, ela é adicionada na lista de vizinhos
        if vizinhoDaDireita and not vizinhoDaDireita.visitado:
            vizinhos.append(vizinhoDaDireita)
        # se a celula de baixo existe e não foi visitada, ela é adicionada na lista de vizinhos
        if vizinhoDeBaixo and not vizinhoDeBaixo.visitado:
            vizinhos.append(vizinhoDeBaixo)
        # se a celula da esquerda existe e não foi visitada, ela é adicionada na lista de vizinhos
        if vizinhoDaEsquerda and not vizinhoDaEsquerda.visitado:
            vizinhos.append(vizinhoDaEsquerda)

        # se a lista de vizinhos não estiver vazia, um vizinho é escolhido aleatoriamente
        return choice(vizinhos) if vizinhos else False


def remove_parede(atual, vizinho):
    # calcula a diferença entre a posição x da celula atual e a posição x da celula vizinha
    dx = atual.x - vizinho.x
    # calcula a diferença entre a posição y da celula atual e a posição y da celula vizinha
    dy = atual.y - vizinho.y

    # se a diferença for 1, a celula vizinha está a direita da celula atual
    if dx == 1:
        atual.paredes['esquerda'] = False
        vizinho.paredes['direita'] = False
    # se a diferença for -1, a celula vizinha está a esquerda da celula atual
    elif dx == -1:
        atual.paredes['direita'] = False
        vizinho.paredes['esquerda'] = False
    # se a diferença for 1, a celula vizinha está embaixo da celula atual
    if dy == 1:
        atual.paredes['encima'] = False
        vizinho.paredes['embaixo'] = False
    # se a diferença for -1, a celula vizinha está em cima da celula atual
    elif dy == -1:
        atual.paredes['embaixo'] = False
        vizinho.paredes['encima'] = False


# cria uma lista com todas as celulas do labirinto
grid = [Celula(col, row) for row in range(rows) for col in range(cols)]
# define a celula inicial como a primeira celula da lista
celula_atual = grid[0]
pilha = []  # cria uma pilha para armazenar as celulas visitadas
colisõesDeParedes = []  # criando a lista de colisões
# cria um retangulo para a celula de destino
celula_final_rect = py.Rect(
    cols * bloco - bloco, rows * bloco - bloco, bloco, bloco)


# loop principal do jogo para:
# 1) atualizar a tela
# 2) verificar eventos
# 3) atualizar o jogo
# 4) desenhar o jogo
# 5) controlar a velocidade do jogo (Taxa de quadros por segundo - FPS)
# 6) verificar se o jogo deve ser encerrado

rodando = menu()  # chama a função menu e armazena o valor retornado na variavel rodando

# criando a tela de vitória


def telaDeVitoria():
    while True:
        #aplicar uma tela preta para a tela de vitória
        tela.fill((0, 0, 0))

        # coloca a imagem de fundo na tela
        tela.blit(fundo3, (0, 50))
        # cria os textos do menu com a fonte neon na pasta font
        txt1 = py.font.Font('font/Monoton-Regular.ttf', 100).render('Você venceu!',
                            True, ("Green")).get_rect(center=(largura // 2, altura // 2 - 250))
        txt2 = py.font.Font('font/Monoton-Regular.ttf', 20).render('Pressione qualquer tecla para sair',
                            True, ("Green")).get_rect(center=(largura // 2, altura // 2 + 300))
        # coloca os textos na tela
        tela.blit(py.font.Font('font/Monoton-Regular.ttf',
                  100).render('Você venceu!', True, ("Green")), txt1)
        tela.blit(py.font.Font('font/Monoton-Regular.ttf', 20).render(
            'Pressione         qualquer         tecla         para         sair', True, ("Green")), txt2)

        # atualiza a tela
        py.display.update()
        # verifica se alguma tecla foi pressionada
        for event in py.event.get():
            if event.type == py.KEYDOWN:
                return False
            if event.type == py.QUIT:
                return False


while rodando:
    # Desenhando o fundo
    # preenche a tela com a cor preta (background)
    tela.fill(py.Color("black"))
    tela.blit(fundo, (0, 0))  # desenha a imagem de fundo na tela (background)

    for event in py.event.get():  # verifica os eventos
        if event.type == py.QUIT:  # se o evento for o botão de fechar a janela
            py.mixer.music.stop()  # para a música de fundo
            rodando = False  # encerra o jogo
            exit()  # encerra o programa

    # controles e movimentos do jogador
    teclaPrecionada = py.key.get_pressed()
    for tecla, tecla_value in teclas.items():
        if teclaPrecionada[tecla_value] and not is_collide(*directions[tecla]):
            direction = directions[tecla]
            break
    if not is_collide(*direction):
        player_rect.move_ip(direction)

    # desenhando o jogador
    tela.blit(player_img, player_rect)

    # desenhando o final do labirinto
    tela.blit(celula_final_img, celula_final_rect)

    # desenha as paredes de todas as celulas do labirinto na tela
    [cell.mostrar_paredes() for cell in grid]
    celula_atual.visitado = True  # marca a celula atual como visitada
    celula_atual.desenha_celula_atual()  # pinta a celula atual de verde
    grid[-1].desenha_celula_final()  # pinta a celula final de vermelho

    # verifica se a celula atual tem vizinhos não visitados
    proxima_celula = celula_atual.verifica_vizinhos()
    if proxima_celula:  # se a celula atual tiver vizinhos não visitados
        proxima_celula.visitado = True  # marca a proxima celula como visitada
        # adiciona a celula atual na pilha de celulas visitadas
        pilha.append(celula_atual)
        # remove a parede entre a celula atual e a proxima celula
        remove_parede(celula_atual, proxima_celula)
        celula_atual = proxima_celula  # define a proxima celula como a celula atual
    elif pilha:  # se a pilha não estiver vazia
        # remove a ultima celula da pilha e define como a celula atual para continuar o processo de geração do labirinto
        celula_atual = pilha.pop()

    # atualizando a lista de colisão
    colisõesDeParedes = sum([cell.get_rects() for cell in grid], [])

    # verifica o jogador colidiu com a celula final
    if player_rect.colliderect(celula_final_rect):
        py.mixer.music.stop()  # para a música de fundo
        # carrega o som de vitória e toca
        vitoria = py.mixer.Sound('music/vitoria.wav')
        vitoria.play()
        vitoria.set_volume(1)
        # trava o jogo e vai pra tela de vitória
        py.time.delay(3000)
        py.time.delay(0)
        rodando = telaDeVitoria()

    py.display.flip()  # atualiza a tela
    clock.tick(50)  # controla a velocidade do jogo
