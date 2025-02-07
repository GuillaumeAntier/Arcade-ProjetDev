from player import Player
from screenManager import ScreenManager
import pygame


class Game:

    def __init__(self):
        self.board = ScreenManager()
        self.players = [Player('1'), Player('2')]

    def run(self):
        pygame.init()

    def handle_events(self):
        return

    def update(self):
        return

    def render(self):
        return

    def change_screen(self, screen_name):
        return
