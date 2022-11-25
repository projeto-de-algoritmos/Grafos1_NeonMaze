# Neon Maze
**Número da Lista**: 34<br>
**Conteúdo da Disciplina**: Grafos 1 - DFS<br>

# Alunos
|Matrícula | Aluno |
| -- | -- |
| 180144979  |  Caetano Santos Lucio |
| 200019228  |  Gustavo Martins Ribeiro |

# Sobre 
Jorginho é um filhote de ET muito serelepinho e está brincando de esconde-esconde com seus amiguinhos. Contudo, a fim de se esconderem de Jorginho, seus amigos se enfiaram em um local de difícil acesso. No entando, o famoso PAC-MAN, um dos maiores personagens da história dos video games resurge das cinzas para abrir caminho para o jorginho, mas nem tudo é de graça: o PAC-MAN tava locão e acabou gerando um labirinto neon psicodélico. Sua missão é guiar o Jorginho até seus amigos para que ele possa vencer a brincadeira e jogar na cara dos seus amigos que ele é o rei do pique-esconde! 

Boa sorte nessa empreitada!

![image](./img/etzinho.png)
### *Imagem 1* - Jorginho, o filhote de ET
![image](./img/bondeDosET.png)
### *Imagem 2* - Amiguinhos do Jorginho
![image](./img/pacman.png)
### *Imagem 3* - PAC-MAN locão

# Imagens do jogo

## 1) Menu inicial
![MenuInicial](./screenshots/menu_inicial.png)
### *Imagem 4* - Menu inicial do Neon Game

## 2) Labirinto (Aleatório)
![LabirintoNeonGame](./screenshots/labirinto.png)
### *Imagem 5* - Labirinto aleatório gerado por DFS & Backtraking

## 3) Tela de Vitória
![image](./screenshots/tela_de_vitoria.png)
### *Imagem 6* - Reconhecimento dos amiguinhos quando o jorginho vence
# Instalação 
**Linguagem**: Pyhton<br>
**Bibliotecas**: PyGame<br>

>A resolução padrão configurada para este projeto é de 1252x652 para melhor visualização do labirinto. Caso a resolução do seu sistema seja menor, sinta-se livre para mudar os parâmetros de ```altura``` e ```largura``` presentes nas primeiras linhas do arquivo ```\main.py```.

- ### Windows
Baixe o pacote Python3 do [site official](https://www.python.org/downloads/), e no momento da instação, marque a opção "Add Python to PATH" para no próximo passo instalar as dependências via terminal e rodar o nosso jogo.

- ### Linux
Execute no terminal do linux a atualização dos pacotes e instalação do python3

```bash
sudo apt update
sudo apt install python3
sudo apt install python3-pip
```
- ### Ambos os sistemas
Executar no terminal:

```bash
pip install pygame
```
# Execução
Abra um terminal na pasta raiz onde foram salvos os arquivos do projeto e execute o comando:
```
python ./main.py
```
ou 
```
python3 ./main.py
```
dependendo de alguma instalação prévia do Python.
# Uso 
O jorginho pode ser movimentando usando as teclas W(cima), A(esquerda), S(embaixo) e D(direita) e também usando os direcionais do teclado. Divirta-se!
