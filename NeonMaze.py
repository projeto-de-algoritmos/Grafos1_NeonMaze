import pygame as py #biblioteca para criar o jogo
import random #biblioteca para gerar números pseudo-aleatórios

#resolução da tela
largura = 1080
altura = 656

#tamanho do bloco
bloco = 100

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

    py.display.flip() #atualiza a tela

    clock.tick(60) #controla a velocidade do jogo

