# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.7.1
#   kernelspec:
#     display_name: tcc
#     metadata:
#       interpreter:
#         hash: 85595fc6e4c66cea5298aa77223b4d67754825b590a0f7ffb3f639c26cc9de1a
#     name: tcc
# ---

# + tags=[]
# #!cat bibliotecas.txt | xargs -n 1 pip3 install
# -

#Importação de bibliotecas
import RPi.GPIO as GPIO
import time, copy
import board, busio, adafruit_vl53l0x
import serial
import numpy as np
from numpy import save
from datetime import datetime
import os
import sys
sys.path.append(os.path.abspath("RADAR.py"))
from RADAR import *
import copy


#Setup das portas logicas do Raspibery PI
class SetupGPIO:
    def __init__(self):
        self.objGPIO = GPIO
        self.objGPIO.cleanup() # limpa todos os estados de todas as portasmotorCar.
        self.objGPIO.setmode(GPIO.BCM) #Definindi uso dos numeros das portas por canais
    
    def get_gpio(self):
        return self.objGPIO

    def clean(self):
        self.objGPIO.cleanup()


class MotorCarro:
    def __init__(self, raspGPIO, servo):
        #GPIO Rodas dianteiras
        self.WLF = 21 #Roda Direita Frente
        self.WLB = 20 #Roda Direita pra trás
        self.WRF = 16 #Roda Esquerda Frente
        self.WRB = 12 #Roda Esquerda Frente
        self.servo = servo

        #GPIO Rodas dianteiras
        self.raspGPIO = raspGPIO
        self.raspGPIO.setup(self.WLF, self.raspGPIO.OUT)
        self.raspGPIO.setup(self.WLB, self.raspGPIO.OUT)
        self.raspGPIO.setup(self.WRF, self.raspGPIO.OUT)
        self.raspGPIO.setup(self.WRB, self.raspGPIO.OUT)
        self.stop()

    def stop(self):
        self.raspGPIO.output(self.WLF, self.raspGPIO.LOW)
        self.raspGPIO.output(self.WLB, self.raspGPIO.LOW)
        self.raspGPIO.output(self.WRF, self.raspGPIO.LOW)
        self.raspGPIO.output(self.WRB, self.raspGPIO.LOW)


    def forward(self):
        self.servo.rotateMotor('center')
        self.raspGPIO.output(self.WLF, self.raspGPIO.HIGH)
        self.raspGPIO.output(self.WRF, self.raspGPIO.HIGH)

    

    def backward(self):
        self.servo.rotateMotor('center')
        self.raspGPIO.output(self.WLB, self.raspGPIO.HIGH)
        self.raspGPIO.output(self.WRB, self.raspGPIO.HIGH)

        
    def left_forward(self):
        self.servo.rotateMotor('left')
        self.raspGPIO.output(self.WLF, self.raspGPIO.HIGH)
        self.raspGPIO.output(self.WRF, self.raspGPIO.HIGH)



    def right_forward(self):
        self.servo.rotateMotor('right')
        self.raspGPIO.output(self.WLF, self.raspGPIO.HIGH)
        self.raspGPIO.output(self.WRF, self.raspGPIO.HIGH)

    def left_backward(self):
        self.servo.rotateMotor('left')
        self.raspGPIO.output(self.WLB, self.raspGPIO.HIGH)
        self.raspGPIO.output(self.WRB, self.raspGPIO.HIGH)

    def right_backward(self):
        self.servo.rotateMotor('right')
        self.raspGPIO.output(self.WLB, self.raspGPIO.HIGH)
        self.raspGPIO.output(self.WRB, self.raspGPIO.HIGH)
    
    def movimentacarro(self, movimento):
        if movimento==0:
            self.forward()
        elif movimento==1:
             self.backward()
        elif movimento==2:
             self.left_forward()
        elif movimento==3:
             self.right_forward()
        elif movimento==4:
             self.left_backward()
        elif movimento==5:
             self.right_backward()
        time.sleep(0.5)

        self.stop()


class ServoMotor:
    def __init__(self, raspGPIO):
        self.position = ''
        self.servoPIN = 18
        self.raspGPIO = raspGPIO
        self.raspGPIO.setup(self.servoPIN, GPIO.OUT)
        self.servo = self.raspGPIO.PWM(self.servoPIN, 50) # GPIO 18 for PWM with 50Hz
        self.servo.start(0)
        time.sleep(2)

        duty = 11

        while duty >= 7:
            self.servo.ChangeDutyCycle(duty)
            time.sleep(0.3)
            self.servo.ChangeDutyCycle(0)
            time.sleep(0.7)
            duty -= 1
    
    def stop(self):
        self.servo.stop()
    
    def rotateMotor(self, position):
        print(position)
        if 'center' in position and 'center' not in self.position :
            print('position center')
            self.servo.ChangeDutyCycle(9)
            time.sleep(0.3)
            self.servo.ChangeDutyCycle(0)
            time.sleep(0.7)
            self.position = 'center'


        
        if 'left' in position and 'left' not in self.position:
            print('position left')
            self.servo.ChangeDutyCycle(11)
            time.sleep(0.3)
            self.servo.ChangeDutyCycle(0)
            time.sleep(0.7)            
            self.position = 'left'


        if 'right' in position and 'right' not in self.position:
            print('position right')
            self.servo.ChangeDutyCycle(7)
            time.sleep(0.3)
            self.servo.ChangeDutyCycle(0)
            time.sleep(0.7)            
            self.position = 'right'


# +
def mkdir(base):
    ''''
    Cria diretórios para salvar as matrizes 
    '''
    path = os.path.join('save', base)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def salvaMatrizes(matrizNome, matrizValor):
    ''''
    Cria diretórios para salvar as matrizes 
    Salva as matrizes com o nome e o valor passado como parametro
    '''
    today=datetime.today().strftime('%Y-%m-%d')
    mkdir(today)
    daytime=datetime.today().strftime('%H:%M:%S')
    np.savez(('save/%s/%s_%s.npz' % (today, matrizNome, daytime)), matrizValor)

def carregaMatriz(pasta, matrizNome):
    ''''
    Carrega as matrizes salvas no diretório
    '''
    path = os.path.join('save', pasta, matrizNome)
    load = np.load(path)
    return load['arr_0']


# -

class CarEnv:
    def __init__(self, motorCarro, radar):
        self.actions_space = ['forward', 'backward', 'leftforward', 'rightforward', 'leftbackward', 'rightbackward']
        self.initialradarpositions = radar.get_distancias()
        self.observation_space = np.array(np.zeros([len(initialradarpositions), len(self.actions_space)]))
        self.state = self.initialradarpositions
        self.done = False
        self.input_size = len(initialradarpositions)
        self.output_size = len(self.actions_space)
        self.motorCar =  motorCarro
        self.finishCount = 0
        self.radar = radar
    
    def finish(self, state):
        '''
        Quando o carro se movimentar 3 vezes para a frente sem parar é o objetivo dele
        '''
        print("STATE FINISH:", state)
        if(state[2]>100 and state[2]>100 and state[3]>100 and state[4]>100):
            self.finishCount+=1
        else:
            self.finishCount=0
        
        print("Count FINISH:", self.finishCount)

        self.finishStatus = False
        if self.finishCount>=3:
            self.finishStatus = True
        return self.finishStatus

    def step(self, action):
        self.take_action(action)
        self.state = self.getState()
        self.done = self.finish(self.state)
        stepP = copy.deepcopy(self.getReward()), self.state, self.done
        return stepP

    def getState(self):
        try:
            self.state = self.radar.get_distancias()
        finally:
           stepMotor.parar_motor()
        return self.state
        
    def take_action(self, action):
        movPosition = np.where(action == np.max(action)) 
        l = list(action).index(np.max(action))
        print('action', l, np.max(action), action)
        self.motorCar.movimentacarro(l)

    def getReward(self):
        f = lambda x: 10 if  x>100 else -10
        return f(max(self.state[:5]))



# ### Inicialização dos Hiperparametros
# Neste parte implementaremos a seguinte parte do código
#
# <img src="imagens/ars_part1.png" width=600 heigth=400>
#
# Inicialmente vamos usar steps_size=10 e epsodes=10 apenas para fins de comparação de resultados, ja que o ambiente é real de um carro autonomo
#
# self.directions = Total de matrizes de pertubações a serem contruidas ***number of directions sampled per iteration N***
#
# self.best_directions = Total de matrizes com recompensas melhores 
#
# Nunca as matrizes de pertubação pode ser maior que as matrizes de recompensas, por isso o uso do assert
#
# ***(number of top-performing directions to use b (b < N is allowed only for V1-t and V2-t)***
#
# self.noise = noise ν

class Hiperparametros():
    def __init__(self):
        self.steps = 10
        self.epsodes = 10
        self.lr = 0.02
        self.directions = 6
        self.best_directions = 6
        assert self.best_directions <= self.directions
        self.noise = 0.03
        self.seed = 1
        self.env_nome = ''



# Os bons resultados desse algoritmo se dão fortemente por causa da normalização dos dados
#
# De acordo com documento, a normalização é necessário por:
#
# "A normalização de estados usada por V2 é semelhante ao clareamento de dados usado em tarefas de regressão, e
# intuitivamente, garante que as políticas atribuam peso igual aos diferentes componentes dos estados. Para
# obter intuição de por que isso pode ajudar, suponha que uma coordenada de estado só tenha valores no intervalo
# 90, 100 enquanto outro componente de estado assume valores na faixa -1, 1. Então, pequenas mudanças em
# o ganho de controle em relação à primeira coordenada de estado levaria a mudanças maiores nas ações
# então, o mesmo tamanho muda em relação ao segundo componente de estado. Portanto, o clareamento permite
# a exploração isotrópica de pesquisa aleatória para ter igual influência sobre os vários componentes de estado"
#
#
# Nesse caso vamos normalizar os valores recebidos pelo radar que varia entre 1 e 899, que seriam equivalentes há 1cm e 89,9cm. 
#

#normalizacao dos estados (Standardization)
class Normalizacao():
    def __init__(self, inputs):
        '''
        Inicializa todos os parametros utilizados durante a normalização
        Keyword arguments:
        inputs -- array dos valores recebidos do sensor de distancia, ex: [30, 6, 3, 4, 8, 91, 819]
        '''
        self.n = np.zeros(inputs) #agregador de estados descobertos desde o inicio
        self.mean = np.zeros(inputs) #média de todos os valores de input
        self.mean_diff = np.zeros(inputs) #usado para o calculo da variancia
        self.var = np.zeros(inputs) #guarda os valores de variancia
    
    def observe(self, inputs):
        '''
        Realiza o calculo da variancia nos dados recebidos do sensor de movimento
        Keyword arguments:
        inputs -- array dos valores recebidos do sensor de distancia, ex: [30, 6, 3, 4, 8, 91, 819]
        '''
        self.n +=1. #indica em que ação é a atual
        last_mean = self.mean.copy() #guarda o valor da ultima média realizada 
        self.mean += (inputs - self.mean) / self.n #atualizando a média baseada na quantidade de ações ja realizadas
        self.mean_diff += (inputs - last_mean) * (inputs - self.mean) # pega a diferença atual e a média antiga
        self.var = (self.mean_diff/self.n).clip(min = 1e-2) #realiza o calculo da variancia, e limita o valor minino em 0.01

    def normalize(self, inputs):
        ''''
        Realiza o calculo da normalização(Padronização) dividindo realizando x- média(x) / desvio padrão de X
        Assim deixando todos os valores dentro da escala -1 e 1
        Essa forma é mais robusta contra outliers

        Keyword arguments:
        inputs -- array dos valores recebidos do sensor de distancia, ex: [30, 6, 3, 4, 8, 91, 819]

        Return:
        Normalized - Valores normalizados entre -1 e 1
        '''
        obs_mean = self.mean #Qual a média atual
        obs_std = np.sqrt(self.var) #Calcula Desvio padrão
        normalized = (inputs - obs_mean) / obs_std #(valor a ser nomalizado - média) / desvio padrão 
        return normalized


# Neste parte implementaremos as seguintes partes do código
#
# <img src="imagens/ars_part2.png" width=600 heigth=400>
#
# <img src="imagens/ars_part3.png" width=600 heigth=400>
#

class Politicas():
    '''
        A exploração acontece no espaço das politicas depois que todo um episódio e steps dele foram executados
        Diferente de outras IAs que usam exploração por ambientes e ações executadas
    '''

    def __init__(self, input_size, output_size):
        '''
        Keyword arguments:
        input_size -- Numeros de entradas
        output_size -- Numeros de saídas

        Return:
        '''
        self.theta = np.zeros((output_size, input_size)) #Cria uma matrix de pesos inicializado em zeros
        #Estamos seguindo o método do artivo pelo lado esquerdo, por isso usamos (output_size, input_size)
    
    def evaluate(self, input, delta=None, direction=None):
        ''''
        De acordo com a direção passada em direction é atualizada a matriz de pesos

        Keyword arguments:
        inputs -- array dos valores recebidos do sensor de distancia, ex: [30, 6, 3, 4, 8, 91, 819]
        delta -- Matrix de pertubação dos numeros 
        direction -- Indica a direção do calculo para positivo ou negativo
        '''

        if direction is None:
            return self.theta.dot(input) #retorna a matriz de pesos que multiplica com as entradas, sem pertubações
        elif direction == 'positive':
            return (self.theta + hp.noise * delta).dot(input) #retorna a matriz de pesos que multiplica com as entradas, com ruido de exploração mais pertubações positivas
        else: 
            return (self.theta - hp.noise * delta).dot(input)#retorna a matriz de pesos que multiplica com as entradas, com ruido de exploração mais pertubações negativas
    
    def samples_deltas(self):
        '''
        Gerando matrix de pertubação, matrix com numeros aleatórios
        '''
        return [np.random.randn(*self.theta.shape) for _ in range(hp.directions)]
        #retorna uma matrix com distribuição normal para o todas as matrizes de pertubaçao 
    
    def update(self, rollouts, sigma_r):
        '''
        Item 7 do Algoritmo, fazendo a atualização dos pesos

        Keyword arguments:
        rollouts -- conjunto de recompensa positiva, conjunto recompensa negativa e a matrizx de numeros aleatórios
        sigma_r -- Indica o desvio padrão da recompensa
        '''
        step = np.zeros(self.theta.shape) #Inicializa com as dimensões de pesos
        for r_pos, r_neg, d in rollouts:
            step += (r_pos - r_neg) * d #Somatoria das recompensas positivas e negativas e a multicao do delta
        self.theta += hp.learning_rate / (hp.best_directions * sigma_r) * step #Atualizando a matriz  de pesos


def explore(env, normalizer, policy, direction = None, delta=None):
    '''
         Faz a exploração do ambiente enquanto não finalizar e não terminar as execuções do epsodio
      
    '''
    state = env.getState() #ler o ambiente radar
    done = False #inicia em False o objetivo
    num_plays = 0. #contador de rodadas no episódio
    sum_rewards = 0 #soma das recompensas
    while not done and num_plays < hp.epsodes:
       print('Execucao: ', num_plays, ', Episodio: ', hp.epsodes, ' Finalizado: ', done)
       normalizer.observe(state) #Atualiza o calculo da variancia nos dados recebidos do sensor de movimento
       state = normalizer.normalize(state) #Realiza o calculo da normalização(Padronização) deixando todos os estados entre -1 e 1
       action = policy.evaluate(state, delta, direction) #atualizada a matriz de pesos de acordo com a direçao selecionada e retirna 
       reward, state, done = env.step(action) #Executa a ação selecionada e retirna a nova leitura do ambiente e se foi finalizado 
       print("Recompensa: ", reward)
       reward = max(min(reward, 1), -1)#evita outlier nas recompensas
       sum_rewards += reward #Soma das recompensas
       num_plays +=1 #atualida o numero da rodada
    return sum_rewards



# Neste parte implementaremos as seguintes partes do código
#
# <img src="imagens/ars_part4.png" width=600 heigth=400>

# +
#Treinando
def train(env, policy, normalizer, hp):
    ''''
      Realiza o treinamento da rede
   
    '''
    loadMatrixPositiveFilename = None
    LoadMatrixFolder = None
    loadMatrixNegativeFilename = None
    DeltaFilename = None
    for step in range(hp.steps):
        
        if loadMatrixPositiveFilename and loadMatrixNegativeFilename and LoadMatrixFolder and DeltaFilename:
            deltas = carregaMatriz(LoadMatrixFolder, loadMatrixPositiveFilename) #Inicializacao das pertubacoes (deltas) e as recompensas negativas e positivas)
            #positive_rewards = 
            negative_rewards = carregaMatriz(LoadMatrixFolder, DeltaFilename)
        else:
            deltas = policy.samples_deltas() #Inicializacao das pertubacoes (deltas) e as recompensas negativas e positivas)
            positive_rewards = [0] * hp.directions #inicializando a matriz de recompensas positivas
            negative_rewards = [0] * hp.directions #inicializando a matriz de recompensas negativas

        #obtendo as recompensas na direcao positiva
        for k in range(hp.directions):
            positive_rewards[k] = explore(env, normalizer, policy, direction='positive', delta=deltas[k])
            
        #obtendo recompensa na direcao negativa
        for k in range(hp.directions):
            positive_rewards[k] = explore(env, normalizer, policy,  direction='negative', delta=deltas[k])
        
        #obtendo todas as recompensas positivas e negativas para computar o desvio dessas recompensas
        all_reward = np.array(positive_rewards + negative_rewards)
        sigma_r = all_rewards.std()

        #ordenacao dos rollouts e selecao das melhores direcoes
        scores = {k: max(r_pos, r_neg) for k, (r_pos, r_neg) in enumerate(zip(positive_rewards, negative_rewards))}
        order = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)[:hp.best_directions]
        rollouts = [(positive_rewards[k], negative_rewards[k], deltas [k]) for k in order]

        #atualizacao de politica
        policy.update(rollouts, sigma_r)

        #impressao da recompensa
        reward_evaluation = explore(env, normalizer, policy)
        print('Step', step, 'Reward:',reward_evaluation )

    salvaMatrizes('positive_rewards', positive_rewards)
    salvaMatrizes('negative_rewards', negative_rewards)
    alvaMatrizes('deltas', deltas)

    
             

# + tags=[]


raspGPIO  = SetupGPIO()
raspGPIO = raspGPIO.get_gpio()
radar = radar_new(raspGPIO)
radar.initialize()
servo = ServoMotor(raspGPIO)
motorCar = MotorCarro(raspGPIO, servo)
print(radar.get_distancias())
motorCar.movimentacarro(1)
motorCar.movimentacarro(2)
motorCar.movimentacarro(3)
motorCar.movimentacarro(4)
motorCar.movimentacarro(5)
motorCar.movimentacarro(0)


carEnv = CarEnv(motorCar, radar)


# + tags=[]
print(radar.get_distancias())

# -

carEnv = CarEnv(motorCar, radar)


