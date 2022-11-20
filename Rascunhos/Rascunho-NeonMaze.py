from CreateMazeMap import *


def is_collide(x, y): #verifica se o jogador colidiu com alguma parede
    tmp_rect = player_rect.move(x, y)
    if tmp_rect.collidelist(colisõesDeParedes) == -1:
        return False
    return True

#criando uma estrutura padrão do pygame
py.init() #inicializa o pygame
tela = py.display.set_mode((largura, altura)) #cria a tela
py.display.set_caption("Neon Maze") #define o título da janela
clock = py.time.Clock() #cria um relógio para controlar a velocidade do jogo

#carregando imagens
fundo = py.image.load('img/background.png') #carrega a imagem de fundo
fundo = py.transform.scale(fundo, (largura, altura)) #redimensiona a imagem de fundo para o tamanho da tela
fundo = py.transform.smoothscale(fundo, (largura, altura)) #aplica um filtro de suavização na imagem de fundo

#carregando musica
py.mixer.init() #inicializa o mixer do pygame
py.mixer.music.load('music/Castelvania2.mp3') #carrega a música que será tocada no jogo
py.mixer.music.set_volume(1) #define o volume da música de fundo
py.mixer.music.play(-1) #reproduz a música de fundo em loop

#gerando o labirinto
maze = gera_labirinto(tela) #gera o labirinto

#configurando o jogador
player_speed = 5
player_img = py.image.load('img/etzinho.png').convert_alpha()
player_img = py.transform.scale(player_img, (bloco - 2 * 4, bloco - 2 * 4))
player_rect = player_img.get_rect()
player_rect.center = bloco // 2, bloco // 2
directions = {'a': (-player_speed, 0), 'd': (player_speed, 0), 'w': (0, -player_speed), 's': (0, player_speed)}
teclas = {'a': py.K_a, 'd': py.K_d, 'w': py.K_w, 's': py.K_s}
direction = (0, 0)

# criando a lista de colisão
colisõesDeParedes = sum([cell.get_rects() for cell in maze], [])

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


    # Desenhando o labirinto
    [cell.mostrar_paredes(tela) for cell in maze] #desenha as paredes de todas as celulas do labirinto na tela
    # Obs.: como o labirinto é gerado em outro arquivo, não fica visível a construção do labirinto na tela. 
    # Veja o arquivo backupNeonMaze.py para entender como o labirinto é gerado.





    py.display.flip() #atualiza a tela
    clock.tick(60) #controla a velocidade do jogo

