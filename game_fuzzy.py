import os
import math
import numpy as np
import pygame
import time
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from math import sin, radians, degrees, copysign
from pygame.math import Vector2
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image



# image = Image.open(r'C:\Users\frede\OneDrive\Documentos\Topicos especiais em instrumentacao\Trabalho bloco 1 Fuzzy\Fuzzy-Controller\car.png')
# #
# image.size
# #
# image.resize((55,30))


def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,255))
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('lasercorpsacadital.ttf',100)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((1280/2),(720/2))
    pygame.display.set_mode((1280, 720)).blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(2)


def crash():
    message_display('You crashed')
    time.sleep(2)
    pygame.quit()

def controle_fuzzy():

    # New Antecedent/Consequent objects hold universe variables and membership
    # functions
    posicao_lateral = ctrl.Antecedent(np.arange(-90, 90, 0.1), 'Posicao Lateral')
    posicao_derivadaerro = ctrl.Antecedent(np.arange(-3000, 3000, 0.1), 'Derivada Erro')
    posicao_frontal = ctrl.Antecedent(np.arange(30, 1120, 0.1), 'Posicao Frontal')
    angulo_volante = ctrl.Consequent(np.arange(-35, 35, 0.1), 'Angulo Volante')
    velocidade = ctrl.Consequent(np.arange(-1, 8, 0.1), 'Velocidade')

    # Custom membership functions can be built interactively with a familiar,
    posicao_derivadaerro['Muito Direita'] = fuzz.trapmf(posicao_derivadaerro.universe, [-3000, -2900, -800, -90])
    posicao_derivadaerro['Direita'] = fuzz.trapmf(posicao_derivadaerro.universe, [-800, -600, -150, 0])
    posicao_derivadaerro['Meio'] = fuzz.trimf(posicao_derivadaerro.universe, [-150, 0, 150])
    posicao_derivadaerro['Esquerda'] = fuzz.trapmf(posicao_derivadaerro.universe, [0, 150, 500, 600])
    posicao_derivadaerro['Muito Esquerda'] = fuzz.trapmf(posicao_derivadaerro.universe, [600, 800, 2900, 3000])
    # Funções de pertinência para os sensores laterais
    posicao_lateral['Muito Direita'] = fuzz.trapmf(posicao_lateral.universe, [-100, -90, -70, -35])
    posicao_lateral['Direita'] = fuzz.trapmf(posicao_lateral.universe, [-40, -20, -10, 0])
    posicao_lateral['Meio'] = fuzz.trimf(posicao_lateral.universe, [-15 , 0, 15])
    posicao_lateral['Esquerda'] = fuzz.trapmf(posicao_lateral.universe, [0, 10, 25, 40])
    posicao_lateral['Muito Esquerda'] = fuzz.trapmf(posicao_lateral.universe, [35, 70, 90, 100])
    # Funções de pertinência para o sensor frontal
    posicao_frontal['Perto'] = fuzz.trapmf(posicao_frontal.universe, [-1, 0, 100, 150])
    posicao_frontal['Longe'] = fuzz.trapmf(posicao_frontal.universe, [120, 450,900,1130])
    # Funções de pertinência para os sensores laterais
    angulo_volante['Muito Direita'] = fuzz.trapmf(angulo_volante.universe, [-33, -30, -15, -10])
    angulo_volante['Direita'] = fuzz.trapmf(angulo_volante.universe, [-12, -8, -2, 0])
    angulo_volante['Meio'] = fuzz.trimf(angulo_volante.universe, [-2, 0, 2])
    angulo_volante['Esquerda'] = fuzz.trapmf(angulo_volante.universe, [0, 2, 8, 12])
    angulo_volante['Muito Esquerda'] = fuzz.trapmf(angulo_volante.universe, [10, 15, 30, 35])
    # Funções de pertinência para o sensor frontal
    velocidade['Devagar'] = fuzz.trimf(velocidade.universe, [0.5, 2.5, 4])
    velocidade['Rapido'] = fuzz.trimf(velocidade.universe, [3, 7, 10])

    #Regras
    rule1 = ctrl.Rule(posicao_lateral['Meio'] & posicao_frontal['Longe'] & posicao_derivadaerro['Meio'], angulo_volante['Meio'])
    rule1_2 = ctrl.Rule(posicao_lateral['Meio'] & posicao_frontal['Longe'] & posicao_derivadaerro['Meio'], velocidade['Rapido'])

    rule2 = ctrl.Rule(posicao_lateral['Esquerda'] & posicao_frontal['Perto'] & posicao_derivadaerro['Muito Esquerda'], angulo_volante['Muito Direita'])
    rule2_2 = ctrl.Rule(posicao_lateral['Esquerda'] & posicao_frontal['Perto'] & posicao_derivadaerro['Muito Esquerda'], velocidade['Devagar']) #Devagar

    rule3 = ctrl.Rule(posicao_lateral['Direita'] & posicao_frontal['Perto'] & posicao_derivadaerro['Muito Direita'], angulo_volante['Muito Esquerda'])
    rule3_2 = ctrl.Rule(posicao_lateral['Direita'] & posicao_frontal['Perto'] & posicao_derivadaerro['Muito Direita'], velocidade['Devagar']) #Devagar

    rule4 = ctrl.Rule(posicao_lateral['Esquerda'] & posicao_frontal['Longe'] & posicao_derivadaerro['Esquerda'], angulo_volante['Meio'])
    rule4_2 = ctrl.Rule(posicao_lateral['Esquerda'] & posicao_frontal['Longe'] & posicao_derivadaerro['Esquerda'], velocidade['Rapido'])

    rule5 = ctrl.Rule(posicao_lateral['Direita'] & posicao_frontal['Longe']  & posicao_derivadaerro['Direita'], angulo_volante['Meio'])
    rule5_2 = ctrl.Rule(posicao_lateral['Direita'] & posicao_frontal['Longe'] & posicao_derivadaerro['Direita'], velocidade['Rapido'])

    rule6 = ctrl.Rule(posicao_lateral['Meio'] & posicao_frontal['Perto']  & posicao_derivadaerro['Meio'], angulo_volante['Meio'])
    rule6_2 = ctrl.Rule(posicao_lateral['Meio'] & posicao_frontal['Perto'] & posicao_derivadaerro['Meio'], velocidade['Rapido']) #Devagar

    rule7 = ctrl.Rule(posicao_lateral['Muito Esquerda'] & posicao_frontal['Perto']  & posicao_derivadaerro['Muito Esquerda'], angulo_volante['Muito Direita'])
    rule7_2 = ctrl.Rule(posicao_lateral['Muito Esquerda'] & posicao_frontal['Perto'] & posicao_derivadaerro['Muito Esquerda'], velocidade['Devagar'])

    rule8 = ctrl.Rule(posicao_lateral['Muito Direita'] & posicao_frontal['Perto']  & posicao_derivadaerro['Muito Direita'], angulo_volante['Muito Esquerda'])
    rule8_2 = ctrl.Rule(posicao_lateral['Muito Direita'] & posicao_frontal['Perto'] & posicao_derivadaerro['Muito Direita'], velocidade['Devagar'])

    rule9 = ctrl.Rule(posicao_lateral['Muito Esquerda'] & posicao_frontal['Longe']  & posicao_derivadaerro['Esquerda'], angulo_volante['Direita'])
    rule9_2 = ctrl.Rule(posicao_lateral['Muito Esquerda'] & posicao_frontal['Longe']  & posicao_derivadaerro['Esquerda'], velocidade['Rapido'])

    rule10 = ctrl.Rule(posicao_lateral['Muito Direita'] & posicao_frontal['Longe'] & posicao_derivadaerro['Direita'], angulo_volante['Esquerda'])
    rule10_2 = ctrl.Rule(posicao_lateral['Muito Direita'] & posicao_frontal['Longe'] & posicao_derivadaerro['Direita'], velocidade['Rapido'])

    rule11 = ctrl.Rule(posicao_lateral['Direita'] & posicao_frontal['Longe'] & posicao_derivadaerro['Meio'], angulo_volante['Esquerda'])
    rule11_2 = ctrl.Rule(posicao_lateral['Direita'] & posicao_frontal['Longe'] & posicao_derivadaerro['Meio'], velocidade['Rapido'])

    rule12 = ctrl.Rule(posicao_lateral['Esquerda'] & posicao_frontal['Longe'] & posicao_derivadaerro['Meio'], angulo_volante['Direita'])
    rule12_2 = ctrl.Rule(posicao_lateral['Esquerda'] & posicao_frontal['Longe'] & posicao_derivadaerro['Meio'], velocidade['Rapido'])

    rule13 = ctrl.Rule(posicao_lateral['Muito Esquerda'] & posicao_frontal['Perto'] & posicao_derivadaerro['Meio'], angulo_volante['Muito Direita'])
    rule13_2 = ctrl.Rule(posicao_lateral['Muito Esquerda'] & posicao_frontal['Perto'] & posicao_derivadaerro['Meio'], velocidade['Devagar'])

    rule14 = ctrl.Rule(posicao_lateral['Muito Direita'] & posicao_frontal['Perto'] & posicao_derivadaerro['Meio'], angulo_volante['Muito Esquerda'])
    rule14_2 = ctrl.Rule(posicao_lateral['Muito Direita'] & posicao_frontal['Perto'] & posicao_derivadaerro['Meio'], velocidade['Devagar'])

    rule15 = ctrl.Rule(posicao_lateral['Esquerda'] & posicao_frontal['Perto'] & posicao_derivadaerro['Esquerda'], angulo_volante['Muito Direita'])
    rule15_2 = ctrl.Rule(posicao_lateral['Esquerda'] & posicao_frontal['Perto'] & posicao_derivadaerro['Esquerda'], velocidade['Devagar']) #Devagar

    rule16 = ctrl.Rule(posicao_lateral['Direita'] & posicao_frontal['Perto'] & posicao_derivadaerro['Direita'], angulo_volante['Muito Esquerda'])
    rule16_2 = ctrl.Rule(posicao_lateral['Direita'] & posicao_frontal['Perto'] & posicao_derivadaerro['Direita'], velocidade['Devagar']) #Devagar

    rule17 = ctrl.Rule(posicao_lateral['Direita'] & posicao_frontal['Perto'] & posicao_derivadaerro['Meio'], angulo_volante['Muito Esquerda'])
    rule17_2 = ctrl.Rule(posicao_lateral['Direita'] & posicao_frontal['Perto'] & posicao_derivadaerro['Meio'], velocidade['Devagar'])

    rule18 = ctrl.Rule(posicao_lateral['Esquerda'] & posicao_frontal['Perto'] & posicao_derivadaerro['Meio'], angulo_volante['Muito Direita'])
    rule18_2 = ctrl.Rule(posicao_lateral['Esquerda'] & posicao_frontal['Perto'] & posicao_derivadaerro['Meio'], velocidade['Devagar'])

    rule19 = ctrl.Rule(posicao_lateral['Direita'] & posicao_frontal['Longe']  & posicao_derivadaerro['Esquerda'], angulo_volante['Esquerda'])
    rule19_2 = ctrl.Rule(posicao_lateral['Direita'] & posicao_frontal['Longe'] & posicao_derivadaerro['Esquerda'], velocidade['Rapido'])

    rule20 = ctrl.Rule(posicao_lateral['Direita'] & posicao_frontal['Perto']  & posicao_derivadaerro['Esquerda'], angulo_volante['Muito Esquerda']) #
    rule20_2 = ctrl.Rule(posicao_lateral['Direita'] & posicao_frontal['Perto'] & posicao_derivadaerro['Esquerda'], velocidade['Devagar'])

    rule21 = ctrl.Rule(posicao_lateral['Esquerda'] & posicao_frontal['Longe']  & posicao_derivadaerro['Direita'], angulo_volante['Direita'])
    rule21_2 = ctrl.Rule(posicao_lateral['Esquerda'] & posicao_frontal['Longe'] & posicao_derivadaerro['Direita'], velocidade['Rapido'])

    rule22 = ctrl.Rule(posicao_lateral['Esquerda'] & posicao_frontal['Perto']  & posicao_derivadaerro['Direita'], angulo_volante['Muito Esquerda'])
    rule22_2 = ctrl.Rule(posicao_lateral['Esquerda'] & posicao_frontal['Perto'] & posicao_derivadaerro['Direita'], velocidade['Devagar'])

    rule23 = ctrl.Rule(posicao_lateral['Muito Esquerda'] & posicao_frontal['Longe']  & posicao_derivadaerro['Meio'], angulo_volante['Direita'])
    rule23_2 = ctrl.Rule(posicao_lateral['Muito Esquerda'] & posicao_frontal['Longe']  & posicao_derivadaerro['Meio'], velocidade['Rapido'])

    rule24 = ctrl.Rule(posicao_lateral['Muito Direita'] & posicao_frontal['Longe'] & posicao_derivadaerro['Meio'], angulo_volante['Esquerda'])
    rule24_2 = ctrl.Rule(posicao_lateral['Muito Direita'] & posicao_frontal['Longe'] & posicao_derivadaerro['Meio'], velocidade['Rapido'])


    car_ctrl = ctrl.ControlSystem([rule1, rule1_2, rule2, rule2_2, rule3, rule3_2, rule4, rule4_2, rule5, rule5_2, rule6, rule6_2, rule7, rule7_2, rule8, rule8_2, rule9, rule9_2, rule10, rule10_2, rule11, rule11_2, rule12, rule12_2, rule13, rule13_2, rule14, rule14_2, rule15, rule15_2, rule16, rule16_2, rule17, rule17_2, rule18, rule18_2, rule19, rule19_2, rule20, rule20_2, rule21, rule21_2, rule22, rule22_2, rule23, rule23_2, rule24, rule24_2])
    carro = ctrl.ControlSystemSimulation(car_ctrl)
    return carro


class Car:
    def __init__(self, x, y, angle=0.0, length=1, max_steering=30, max_acceleration=3.0):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 8
        self.brake_deceleration = 20
        self.free_deceleration = 50
        self.acceleration = 0.0
        self.steering = 0.0

    def update(self, dt):
        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))

        if self.steering:
            turning_radius = self.length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt


class Game:


    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Simulador Fuzzy")
        width = 1280
        height = 720
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False



    def run(self):
        car_image = pygame.image.load('car.png')
        car_image = pygame.transform.scale(car_image, (45, 20))
        track_image = pygame.image.load('race_track.png')
        track_image = pygame.transform.scale(track_image, (1280, 720))
        track_mask = pygame.mask.from_threshold(track_image,pygame.Color('black'), (1, 1, 1, 255))
        car = Car(30, 1.5)
        ppu = 32
        #data = np.array([])
        dataSensors = np.zeros(3)
        dataSteering = np.zeros(1)
        dataVel = np.zeros(1)
        steer=0
        sensor_esquerdo = 0
        sensor_direito = 0
        sensor_frontal = 0
        distancia = 0
        movimento_carro = controle_fuzzy()
        car.velocity.x = 3
        erro_anterior = 10
        ploterror = np.zeros(1)

        while not self.exit:
            dt = self.clock.get_time() / 1000

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    plt.plot(range(0, (ploterror.reshape(1, ploterror.size)).size), ploterror)
                    plt.show()
                    self.exit = True
            a = []
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_UP]:
                pygame_position = np.round(car.position * ppu)
                #sensores
                for i in range(1500):
                    x =  np.int(pygame_position[0] + math.cos(math.radians(car.angle)) * i)
                    y =  np.int(pygame_position[1] - math.sin(math.radians(car.angle)) * i)
                    if (track_mask.get_at([x,y])==1):
                        pygame.draw.lines(self.screen,(255,0,0),True,[pygame_position, [x,y]])
                        sensor_frontal = math.hypot(x - pygame_position[0], y - pygame_position[1])
                        break

                for i in range(1500):
                     x = np.int(pygame_position[0] + math.cos(math.radians(car.angle+90)) * i)
                     y = np.int(pygame_position[1] - math.sin(math.radians(car.angle+90)) * i)
                     if (track_mask.get_at([x,y])==1):
                         pygame.draw.lines(self.screen,(255,0,0),True,[pygame_position, [x,y]])
                         sensor_esquerdo = math.hypot(x - pygame_position[0], y - pygame_position[1])
                         break

                for i in range(1500):
                    x = np.int(pygame_position[0] + math.cos(math.radians(car.angle - 90)) * i)
                    y = np.int(pygame_position[1] - math.sin(math.radians(car.angle - 90)) * i)
                    if (track_mask.get_at([x,y])==1):
                        pygame.draw.lines(self.screen,(255,0,0),True,[pygame_position, [x,y]])
                        sensor_direito = math.hypot(x - pygame_position[0], y - pygame_position[1])
                        break

                distancia = sensor_direito - sensor_esquerdo
                #print(distancia)
                # print("Erro anterior", abs(erro_anterior))
                errord = (abs(distancia) - abs(erro_anterior))/0.030

                #print(abs(distancia), "-", abs(erro_anterior))
                # print("Erro Derivada", errord)
                # print("Distância", distancia)
                # print("Frente:", sensor_frontal)
                #print(distancia)
                #Controlador fuzzy
                movimento_carro.input['Derivada Erro'] = errord
                movimento_carro.input['Posicao Lateral'] = distancia
                movimento_carro.input['Posicao Frontal'] = sensor_frontal
                movimento_carro.compute()

                car.velocity.x = movimento_carro.output['Velocidade']
                car.acceleration = -car.velocity.x / dt
                car.acceleration = max(-car.max_acceleration, min(car.acceleration, car.max_acceleration))
                car.steering = movimento_carro.output['Angulo Volante']
                car.steering = max(-car.max_steering, min(car.steering, car.max_steering))
                #
                # # User input
                # pressed = pygame.key.get_pressed()
                #
                # #b = np.zeros(4)
                # if pressed[pygame.K_UP]:
                #     #b[0] = 1
                #     if car.velocity.x < 0:
                #         car.acceleration = car.brake_deceleration
                #     else:
                #         car.acceleration += 1 * dt
                # elif pressed[pygame.K_DOWN]:
                #     #b[1] = 1
                #     if car.velocity.x > 0:
                #         car.acceleration = -car.brake_deceleration
                #     else:
                #         car.acceleration -= 1 * dt
                # elif pressed[pygame.K_SPACE]:
                #     if abs(car.velocity.x) > dt * car.brake_deceleration:
                #         car.acceleration = -copysign(car.brake_deceleration, car.velocity.x)
                #     else:
                #         car.acceleration = -car.velocity.x / dt
                # else:
                #     if abs(car.velocity.x) > dt * car.free_deceleration:
                #         car.acceleration = -copysign(car.free_deceleration, car.velocity.x)
                #     else:
                #         if dt != 0:
                #             car.acceleration = -car.velocity.x / dt
                # car.acceleration = max(-car.max_acceleration, min(car.acceleration, car.max_acceleration))
                # if pressed[pygame.K_RIGHT]:
                #     #b[2] = 1
                #     car.steering -= 30 * dt
                #     steer = car.steering
                # elif pressed[pygame.K_LEFT]:
                #     #b[3] = 1
                #     car.steering += 30 * dt
                #     steer = car.steering
                # else:
                #     car.steering = 0
                #
                #     if steer > 0:
                #         steer -= 30 * dt
                #     elif steer < 0:
                #         steer += 30 * dt
                #     else:
                #         steer = 0
                #
                #
                # car.steering = max(-car.max_steering, min(car.steering, car.max_steering))
                # steer = max(-car.max_steering, min(steer, car.max_steering))
                #
                # # b = np.array(b)
                # # dataKeys = np.vstack((dataKeys, b))
                #
                # print(car.velocity)
                #
                # b = np.array(car.steering)
                # dataSteering = np.vstack((dataSteering, b))

                # Logic
                car.update(dt)

            a.append(distancia)
            a = np.array(a)
            ploterror = np.vstack((ploterror, a))

            # Drawing
            self.screen.blit(track_image, [0, 0])
            rotated = pygame.transform.rotate(car_image, car.angle)
            rect = rotated.get_rect()
            #pega a posição do carro e compara com a mascara da pista
            position =[]
            pygame_position = np.round(car.position * ppu)
            rect.center
            for i in pygame_position:
                position.append(np.int(i))

            #se for uma posição da máscara, ele colide
            if (track_mask.get_at(position)==1):
                # df = pd.DataFrame(dataSensors)
                # df.to_csv(r'dataSensores.csv', header=None, index=False)
                # df2 = pd.DataFrame(dataSteering)
                # df2.to_csv(r'dataSteering.csv', header=None, index=False)
                # df3 = pd.DataFrame(dataVel)
                # df3.to_csv(r'dataVelocidade.csv', header=None, index=False)
                crash()

            self.screen.blit(rotated, car.position * ppu - (rect.width / 2, rect.height / 2))

            pygame.display.flip()


            # print(pygame_position)
            # print(pygame_position + abs(math.cos(math.degrees(abs(car.angle)))) * 100)
            # print("Car steering:", car.steering)
            # print("Car Angle:", car.angle)
            erro_anterior = distancia
            self.clock.tick(self.ticks)
        pygame.quit()

    # def extractCSV(self, data):
    #     df = pd.DataFrame(data)
    #     df.to_csv(index=False)

if __name__ == '__main__':
    game = Game()
    game.run()
