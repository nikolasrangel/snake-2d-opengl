from random import randint
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

'''
    COMPUTACAO GRAFICA - PROJETO FINAL
    GAME 2D - SNAKE

    NIKOLAS JOSE RANGEL DE SOUZA
    MATRICULA: 01720113
'''

# Atributos da janela
largura, altura = 500, 500  
# Relacao de quantos pixels na largura x altura
pixelMapaLargura, pixelMapaAltura = 50, 50
''' 
    Timer para a velocidade da Snake.
    A cada comida que a Snake come diminui-se este timer, de modo a tornar
    jogo mais rápido e aumentando, assim, a dificuldade.
'''
t = 100

''' 
    Snake será definida por duas variáveis:
    1 - Direção atual em que está percorrendo;
        - (0, 1): percorre para cima;
        - (0, -1): percorrendo para baixo;
        - (-1, 1): percorrendo para esquerda;
        - (1, 0): percorrendo para direita.
    2 - Lista de posições do corpo da Snake: ao passo que "come", a Snake cresce, isto é,
    acrescenta-se posições a esta lista.
        - cabeça da Snake posicionada inicialmente na posição (25,1).
'''
snake_corpo = [(25,1)]      # Possui uma posição (sua cabeça)
snake_direcao = (1, 0)      # Direção que está indo (começa indo para direita)

'''
    Tela tem as posições para altura e largura de 0 à 49
    [0, 49]
'''
comida = (12, 23)

'''
    Flags para o controle sobre a execução do jogo
'''
jogoExecucao     = False
jogoEncerrado    = False 

# Pontuacao
pontuacao = 0

def tecladoMovimentos(tecla, x, y):
    global jogoExecucao
    '''
        Determinar se jogo está pausado. Caso esteja, ao tirar jogo do pause
        deverá voltar ao loop para desenhar Snake
    '''
    flagEstavaParado = jogoExecucao

    # Ao apertar tecla 'P' pausa/start no jogo
    if tecla == b'p':
        jogoExecucao = not jogoExecucao
    # Ao apertar tecla 'S' começa o jogo:
    if tecla == b's':
        jogoExecucao = True
    # Reiniciar jogo ao apertar tecla "R"
    if tecla == b'r':
        reiniciarJogo()

    # Se estava parado e agora deu start: chama loop (função movimenta)
    if ( not flagEstavaParado ) and jogoExecucao:
        movimenta(1)  

def tecladoMovimentosTeclasEspeciais(tecla, x, y):
    global snake_direcao        
    
    if tecla == GLUT_KEY_UP:
        snake_direcao = (0, 1)                           
    if tecla == GLUT_KEY_DOWN:
        snake_direcao = (0, -1)                           
    if tecla == GLUT_KEY_LEFT:
        snake_direcao = (-1, 0)                           
    if tecla == GLUT_KEY_RIGHT:
        snake_direcao = (1, 0)     


def reiniciarJogo():
    global pontuacao, comida, snake_corpo, snake_direcao, jogoExecucao, jogoEncerrado, t
    pontuacao = 0
    comida = (12, 23)
    snake_corpo = [(25,1)]
    snake_direcao = (1, 0)
    jogoExecucao     = True
    jogoEncerrado    = False
    t = 100 


'''
    Função para movimentar a Snake de acordo com as interações pelo teclado.
    Snake é movimentada de acordo com a atual posicao da variavel "snake_direcao".
    Movimento é feito da seguinte maneira: insere na primeira posicao (em frente a cabeça da Snake) o novo pixel
        e remove o último pixel do corpo. Assim, de acordo com a direcao setada, dá a impressão do movimento.
'''
def movimenta(x):
    global comida
    global t
    global pontuacao
    global jogoEncerrado, jogoExecucao

    # Movimentar Snake de acordo com a direção atuaç
    novaPosicao = moveSnake(snake_corpo[0], snake_direcao)
    snake_corpo.insert(0, novaPosicao)     # Insere no comeco
    snake_corpo.pop()                      # Remove do final

    # Determinar posição da cabeça:
    (cabecaX, cabecaY) = snake_corpo[0]

    # Determinar se cabeça da Snake chocou-se com alguma parte do corpo (encerra jogo)
    # Condição é se a cabeça está na mesma posição que alguma outra parte
    for i in range(1, len(snake_corpo)):
        aux = snake_corpo[i]
        if cabecaX == aux[0] and cabecaY == aux[1]:
            jogoEncerrado = True
            jogoExecucao = False
            criaMenu() 

    # Determinar se Snake comeu a comida:
    if cabecaX == comida[0] and cabecaY == comida[1]:
        # Aumentar tamanho do corpo da Snake:
        snake_corpo.append(comida)
        # Gerar nova posição para a comida:
        comida = randint(1, 48), randint(1, 48)
        # Aumenta dificuldade do jogo ao diminuir o timer e Snake ir mais rápido
        t -= 5
        # Incrementa pontuacao
        pontuacao += 10
        # Atualiza pontuacao no menu
        criaMenu()
    
    if jogoExecucao:
        glutTimerFunc(t, movimenta, 1)
    elif jogoEncerrado:
        print("Jogo encerrado")

'''
    Realiza o movimento sobre o corpo da snake: incrementa a posicao mais o sentido atual que está indo
    Nesta função deve tratar os limites da janela: ao ultrapassar o usuário perde o jogo.
'''
def moveSnake(ponto1, ponto2):
    global jogoExecucao, jogoEncerrado
    x = ponto1[0] + ponto2[0]
    y = ponto1[1] + ponto2[1]

    if x >= 49 or y >= 49 or x <= 0 or y <=0 :
        jogoExecucao    = False
        jogoEncerrado   = True 

    return (x, y)

def desenhaComidas():
    glColor3f(0.67, 0.48, 1.0)
    # Envia coordenadas para desenhar a comida na tela:
    desenhaCorpo(comida[0], comida[1], 1, 1)

def desenhaSnake():
    glColor3f(1.0, 1.0, 1.0)  # Cor da Snake: branca
    for x, y in snake_corpo:  # Para cada pedaço de seu corpo
        desenhaCorpo(x, y, 1, 1)   # Desenha na posição (x, y) com altura e largura 1

'''
    Cria a 'dimensão interna' para janela.
    Objetivo é diminuir densidade de pixels na tela, assim, obtendo pixels maiores.
    Logo, cada pedaço do corpo da Snake é melhor visualizada no mapa.
'''
def resetaMapa(largura, altura, larguraPosicaoMapa, alturaPosicaoMapa):
    glViewport(0, 0, largura, altura)   # Especifica as dimensões da viewport
    glMatrixMode(GL_PROJECTION)         # Especifica o sistema de coordendas
    glLoadIdentity()                    # Reseta da matriz para identidade
    glOrtho(0.0, larguraPosicaoMapa, 0.0, alturaPosicaoMapa, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

'''
    Função responsável por desenhar um pixel do corpo da Snake.
'''   
def desenhaCorpo(x, y, largura, altura):
    glBegin(GL_QUADS)                                  
    glVertex2f(x, y)                                  
    glVertex2f(x + largura, y)                           
    glVertex2f(x + altura, y + altura)                  
    glVertex2f(x, y + altura)                         
    glEnd()                                            

'''
    Função desenha é chamada a todo instante
'''
def desenha():          
    global comida
    # Limpa a tela:
    glClear(GL_COLOR_BUFFER_BIT)
    # Faz com que a matriz corrente seja inicializada com a matriz identidade (nenhuma transformação é acumulada):    
    glLoadIdentity()  
    # Configura as dimensões internas do mapa de posições:
    resetaMapa(largura, altura, pixelMapaLargura, pixelMapaAltura)
    # Com a tela limpa, desenha toda a Snake na tela e as comida(s):
    desenhaComidas()
    desenhaSnake()
    # Se jogo foi encerrado:
    if jogoEncerrado:
        comida = (50, 50)
        desenhaTexto("Você perdeu! : (", 17, 30, corAlerta)
        desenhaTexto("Sua pontuação: " + str(pontuacao), 17, 25, corMensagem)
        desenhaTexto("Clique com botão direito para abrir menu", 5.5, 20, corMensagem)
        
    glutSwapBuffers()

def getPontuacao():
    return pontuacao

def criaMenu():
    menu = glutCreateMenu(menuAcoes)
    glutAddMenuEntry("Iniciar ('S')", 0)
    glutAddMenuEntry("Reiniciar jogo ('R')", 1)
    glutAddMenuEntry("Pausar/voltar ao jogo ('P')", 2)
    glutAddMenuEntry("", -1)
    glutAddMenuEntry("Sua pontuacao: " + str(getPontuacao()), -1)
    glutAddMenuEntry("", -1)
    glutAddMenuEntry("Sair", 3)
    glutAttachMenu(GLUT_RIGHT_BUTTON)

def menuAcoes(acao):
    global jogoExecucao
    global pontuacao
    flagEstavaParado = jogoExecucao

    if acao == 0:
        pontuacao = 0
        jogoExecucao = True
    elif acao == 1:
        reiniciarJogo()
    elif acao == 2:
        jogoExecucao = not jogoExecucao
    elif acao == 3:
        exit(0)
    else:
        return 0

    if ( not flagEstavaParado ) and jogoExecucao:
        movimenta(1)

    return 0

corAlerta = 0.9, 0.1, 0.1
corMensagem = 0.2, 0.2, 0.75

def desenhaTexto(string, x, y, cor): 
    glPushMatrix()
    glColor3f(cor[0], cor[1], cor[2])
    # Posição no universo onde o texto será colocado 
    glRasterPos2f(x, y)
    # Exibe caracter a caracter
    for char in string: 
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24,ord(char)) 
    glPopMatrix() 

# Função principal: inicializa glut e chama as funções
def main():
    glutInit(sys.argv)                                  # Inicializa glut
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)         # Aviso a glut de que tipo de modo de exibição é usado
    glutInitWindowSize(largura, altura)                 # Configura o tamanho da janela para um tamanho específico
    glutInitWindowPosition(640, 200)                    # Configura a posição da janela na tela
    glutCreateWindow(b"Snake 2D - Projeto Final CG")    # Cria janela com um título definido
    glutDisplayFunc(desenha)                            # Define a função de callback para exibição
    glutIdleFunc(desenha)                               # Realiza operações em segundo plano (chamando a função desenha())
    glutKeyboardFunc(tecladoMovimentos)                 # Receber interações pelo teclado                  
    glutSpecialFunc(tecladoMovimentosTeclasEspeciais)   # Receber interações pelo teclado
    criaMenu()
    glutMainLoop()                                     

# Exibir opções no console
print("Bem-vindo ao Snake 2D!")
print(":::::::::::::::::OPÇÕES::::::::::::::::: \n'S': iniciar jogo; \n'P': pausar/voltar ao jogo; \n'R': reiniciar o jogo.")

# Chamada a função principal
main()