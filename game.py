from player import Player
from screenManager import ScreenManager
import pygame
import serial
import re
import os

class Game:

    def __init__(self):
        pygame.init()  
        self.screen = pygame.display.set_mode((1000, 1000)) 
        self.board = ScreenManager()
        self.players = [Player('1'), Player('2')]
        self.scores = []
        self.current_screen = "main_menu"
        
        try:
            self.arduino = serial.Serial(port="COM7", baudrate=9600, timeout=1)
        except serial.SerialException as e:
            print(f"Erreur de connexion au port série : {e}")
            exit(1)  # Quittez le programme si la connexion échoue

    def read_joystick(self):
        if self.arduino.in_waiting > 0:
            data = self.arduino.readline().decode("utf-8").strip()
            try:
                match = re.search(r'X:\s*(\d+),\s*Y:\s*(\d+),\s*Bouton:\s*(\d+)', data)
                if match:
                    x = int(match.group(1))
                    y = int(match.group(2))
                    button = int(match.group(3))
                    return (x, y, button)
            except ValueError:
                print("Erreur de conversion des données")
        return None

    def run(self):
        running = True
        print("Démarrage de la boucle principale...")
        while running:
            joystick_data = self.read_joystick()  
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Gérer les entrées du clavier pour le deuxième tank
            keys = pygame.key.get_pressed()  # Récupérer l'état des touches
            if keys[pygame.K_UP]:  # Touche pour avancer
                self.players[1].position[1] -= self.players[1].movement_speed * 2
            if keys[pygame.K_DOWN]:  # Touche pour reculer
                self.players[1].position[1] += self.players[1].movement_speed * 2
            if keys[pygame.K_LEFT]:  # Touche pour tourner à gauche
                self.players[1].angle += self.players[1].rotation_speed
            if keys[pygame.K_RIGHT]:  # Touche pour tourner à droite
                self.players[1].angle -= self.players[1].rotation_speed

            # Mettre à jour les tanks
            for player in self.players:
                player.update(joystick_data)  

                # Mettre à jour les balles
                for bullet in player.bullets:
                    bullet.update()  # Mettre à jour la position de chaque balle

            self.screen.fill((10, 10, 10))  
            for player in self.players:
                player.render(self.screen) 
            pygame.display.flip()  
        
        pygame.quit()

    def handle_events(self):
        return

    def update(self):
        return

    def render(self):
        return

    def change_screen(self, screen_name):
        return
