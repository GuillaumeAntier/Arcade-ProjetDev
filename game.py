from player import Player
from screenManager import ScreenManager
import pygame
import serial
import re
import os

# Define layers directly in game.py
layers = [
    [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 1, 0],
    ],
    # ... (rest of the layers)
]

class Game:

    def __init__(self):
        pygame.init()  
        self.screen = pygame.display.set_mode((1000, 1000)) 
        self.board = ScreenManager()
        self.players = [Player('1')]
        self.scores = []
        self.current_screen = "main_menu"
        self.arduino = serial.Serial(port="COM7", baudrate=9600, timeout=1)

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
            
            for player in self.players:
                player.update(joystick_data)  

            self.screen.fill((0, 0, 0))  
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
