from player import Player
from screenManager import ScreenManager
from database import Database


class Game:

    def __init__(self):
        self.board = ScreenManager()
        self.players = [Player('1'), Player('2')]
        self.scores = []
        self.current_screen = "main_menu"

    def run(self):
        return

    def handle_events(self):
        return

    def update(self):
        return

    def render(self):
        return

    def change_screen(self, screen_name):
        return
