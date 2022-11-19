import pygame as py #biblioteca para criar o jogo
import random #biblioteca para gerar números pseudo-aleatórios

#resolução da tela
largura = 800
altura = 600

#tamanho do bloco
bloco = 100

#numero de linhas e colunas do tabuleiro
cols, rows = largura // bloco, altura // bloco # a quantidade de linhas e colunas é igual ao tamanho da tela dividido pelo tamanho do bloco

#criando uma estrutura padrão do pygame
py.init() #inicializa o pygame
tela = py.display.set_mode((largura, altura)) #cria a tela
py.display.set_caption("Neon Maze") #define o título da janela
clock = py.time.Clock() #cria um relógio para controlar a velocidade do jogo

#loop principal do jogo para:
# 1) atualizar a tela
# 2) verificar eventos
# 3) atualizar o jogo
# 4) desenhar o jogo
# 5) controlar a velocidade do jogo (Taxa de quadros por segundo - FPS)
# 6) verificar se o jogo deve ser encerrado

rodando = True
while rodando:
    tela.fill(py.Color("black")) #preenche a tela com a cor preta (background)

    for event in py.event.get(): #verifica os eventos
        if event.type == py.QUIT: #se o evento for o botão de fechar a janela
            rodando = False #encerra o jogo
            exit() #encerra o programa
    
    py.display.flip() #atualiza a tela
    clock.tick(60) #controla a velocidade do jogo

