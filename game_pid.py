import os
import math
import numpy as np
import pygame
import time
from math import sin, radians, degrees, copysign
from pygame.math import Vector2
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


class PID:
    """PID controller."""

    def __init__(self, Kp, Ki, Kd, origin_time=None):
        if origin_time is None:
            origin_time = time.time()

        # Gains for each term
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

        # Corrections (outputs)
        self.Cp = 0.0
        self.Ci = 0.0
        self.Cd = 0.0

        self.previous_time = origin_time
        self.previous_error = 0.0

    def Update(self, error, current_time=None):
        if current_time is None:
            current_time = time.time()
        dt = current_time - self.previous_time
        if dt <= 0.0:
            return 0
        de = error - self.previous_error

        self.Cp = error
        self.Ci += error * dt
        self.Cd = de / dt

        self.previous_time = current_time
        self.previous_error = error

        return (
            (self.Kp * self.Cp)    # proportional term
            + (self.Ki * self.Ci)  # integral term
            + (self.Kd * self.Cd)  # derivative term
        )


class Car:
    def __init__(self, x, y, angle=0.0, length=1, max_steering=30, max_acceleration=1.0):
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
        controlador_lateral = PID(1, 0, 0.1)
        target_distance = 0
        controlador_frontal = PID(1, 0, 0)
        distancia_ideal = 10



        while not self.exit:
            dt = self.clock.get_time() / 1000


            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

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
                error = target_distance - distancia
                error_frontal = distancia_ideal - sensor_frontal
                correction = controlador_lateral.Update(error)
                correction_frontal = controlador_frontal.Update(error_frontal)
                car.steering = correction
                car.velocity.x = -correction_frontal
                car.acceleration = -car.velocity.x / dt
                car.acceleration = max(-car.max_acceleration, min(car.acceleration, car.max_acceleration))
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

            # for i in range(1500):
            #     x =  np.int(pygame_position[0] + math.cos(math.radians(car.angle + 45)) * i)
            #     y =  np.int(pygame_position[1] - math.sin(math.radians(car.angle + 45)) * i)
            #     if (track_mask.get_at([x,y])==1):
            #         pygame.draw.lines(self.screen,(255,0,0),True,[pygame_position, [x,y]])
            #         print('Sensor Diagonal Positiva: ', math.hypot(x - pygame_position[0], y - pygame_position[1]))
            #         a.append(math.hypot(x - pygame_position[0], y - pygame_position[1]))
            #         break
            #
            # for i in range(1500):
            #     x =  np.int(pygame_position[0] + math.cos(math.radians(car.angle - 45)) * i)
            #     y =  np.int(pygame_position[1] - math.sin(math.radians(car.angle - 45)) * i)
            #     if (track_mask.get_at([x,y])==1):
            #         pygame.draw.lines(self.screen,(255,0,0),True,[pygame_position, [x,y]])
            #         print('Sensor Diagonal Negativa: ', math.hypot(x - pygame_position[0], y - pygame_position[1]))
            #         a.append(math.hypot(x - pygame_position[0], y - pygame_position[1]))
            #         break



            c = np.array(car.velocity[0])
            dataVel = np.vstack((dataVel, c))

            self.screen.blit(rotated, car.position * ppu - (rect.width / 2, rect.height / 2))

            pygame.display.flip()


            # print(pygame_position)
            # print(pygame_position + abs(math.cos(math.degrees(abs(car.angle)))) * 100)
            # print("Car steering:", car.steering)
            # print("Car Angle:", car.angle)

            self.clock.tick(self.ticks)
        pygame.quit()

    # def extractCSV(self, data):
    #     df = pd.DataFrame(data)
    #     df.to_csv(index=False)

if __name__ == '__main__':
    game = Game()
    game.run()
