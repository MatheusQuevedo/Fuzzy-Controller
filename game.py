import os
import math
import numpy as np
import pygame
import time
from math import sin, radians, degrees, copysign
from pygame.math import Vector2
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

class Car:
    def __init__(self, x, y, angle=0.0, length=1, max_steering=90, max_acceleration=1.0):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 3
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
        pygame.display.set_caption("Car tutorial")
        width = 1280
        height = 720
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False


    def run(self):
        car_image = pygame.image.load('car.png')
        car_image = pygame.transform.scale(car_image, (45, 20))
        track_image = pygame.image.load('track_image.png')
        track_image = pygame.transform.scale(track_image, (1280, 720))
        track_mask = pygame.mask.from_threshold(track_image,pygame.Color('black'), (1, 1, 1, 255))
        car = Car(20, 2.3)
        ppu = 32

        while not self.exit:
            dt = self.clock.get_time() / 1000

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # User input
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_UP]:
                if car.velocity.x < 0:
                    car.acceleration = car.brake_deceleration
                else:
                    car.acceleration += 1 * dt
            elif pressed[pygame.K_DOWN]:
                if car.velocity.x > 0:
                    car.acceleration = -car.brake_deceleration
                else:
                    car.acceleration -= 1 * dt
            elif pressed[pygame.K_SPACE]:
                if abs(car.velocity.x) > dt * car.brake_deceleration:
                    car.acceleration = -copysign(car.brake_deceleration, car.velocity.x)
                else:
                    car.acceleration = -car.velocity.x / dt
            else:
                if abs(car.velocity.x) > dt * car.free_deceleration:
                    car.acceleration = -copysign(car.free_deceleration, car.velocity.x)
                else:
                    if dt != 0:
                        car.acceleration = -car.velocity.x / dt
            car.acceleration = max(-car.max_acceleration, min(car.acceleration, car.max_acceleration))

            if pressed[pygame.K_RIGHT]:
                car.steering -= 30 * dt
            elif pressed[pygame.K_LEFT]:
                car.steering += 30 * dt
            else:
                car.steering = 0
            car.steering = max(-car.max_steering, min(car.steering, car.max_steering))

            test = abs(car.steering)
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
                crash()
            #sensor ARRUMAR

            x =  pygame_position[0] + math.cos(math.radians(car.angle)) * 100
            y =  pygame_position[1] - math.sin(math.radians(car.angle)) * 100

            x1 = pygame_position[0] + math.cos(math.radians(car.angle+90)) * 100
            y1 = pygame_position[1] - math.sin(math.radians(car.angle+90)) * 100

            x2 = pygame_position[0] + math.cos(math.radians(car.angle - 90)) * 100
            y2 = pygame_position[1] - math.sin(math.radians(car.angle - 90)) * 100

            pygame.draw.lines(self.screen,(255,0,0),True,[pygame_position, [x,y]])
            pygame.draw.lines(self.screen, (255, 0, 0), True, [pygame_position, [x1, y1]])
            pygame.draw.lines(self.screen, (255, 0, 0), True, [pygame_position, [x2, y2]])


            self.screen.blit(rotated, car.position * ppu - (rect.width / 2, rect.height / 2))

            pygame.display.flip()

            print(pygame_position)
            print(pygame_position + abs(math.cos(math.degrees(abs(car.angle)))) * 100)
            print("Car steering:", car.steering)
            print("Car Angle:", car.angle)

            self.clock.tick(self.ticks)
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
