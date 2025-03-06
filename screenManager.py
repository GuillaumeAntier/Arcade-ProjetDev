import pygame, sys
import pygame_widgets
import pygame.mixer as music
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox


class ScreenManager:
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Game')
        self.screen = pygame.display.set_mode((1920, 1080))
        self.font = pygame.font.SysFont(None, 40)
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_screen = "main_menu"
        self.main_volume = 50
        self.music_volume = 50

        self.main_volume_slider = Slider(self.screen, 50, 180, 300, 40, min=0, max=100, step=1, initial=self.main_volume)
        self.music_volume_slider = Slider(self.screen, 50, 280, 300, 40, min=0, max=100, step=1, initial=self.music_volume)
        self.main_volume_text = TextBox(self.screen, 50, 150, 100, 30, fontSize=20)
        self.music_volume_text = TextBox(self.screen, 50, 250, 100, 30, fontSize=20)
        self.main_volume_text.disable()
        self.music_volume_text.disable()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update_screen()
            pygame.display.update()
            self.clock.tick(60)

    def handle_events(self):
        self.click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.click = True

    def update_screen(self):
        self.screen.fill((0, 0, 0))
        if self.current_screen == "main_menu":
            self.draw_main_menu()
        elif self.current_screen == "game":
            self.draw_game_screen()
        elif self.current_screen == "options":
            self.draw_options_screen()
        elif self.current_screen == "video":
            self.video_settings()
        elif self.current_screen == "audio":
            self.audio_settings()

    def draw_main_menu(self):
        self.draw_text("Main Menu", 20, 20)

        mx, my = pygame.mouse.get_pos()
        game_button = self.draw_button("Game", 50, 100, 200, 50)
        options_button = self.draw_button("Options", 50, 200, 200, 50)
        quit_button = self.draw_button("Quit", 50, 500, 200, 50)

        if self.click:
            if game_button.collidepoint(mx, my):
                self.current_screen = "game"
            elif options_button.collidepoint(mx, my):
                self.current_screen = "options"
            elif quit_button.collidepoint(mx, my):
                self.running = False

    def draw_game_screen(self):
        self.draw_text("Game", 20, 20)

        mx, my = pygame.mouse.get_pos()
        back_button = self.draw_button("Back", 50, 500, 200, 50)

        if self.click and back_button.collidepoint(mx, my):
            self.current_screen = "main_menu"

    def draw_options_screen(self):
        self.draw_text("Options", 20, 20)

        mx, my = pygame.mouse.get_pos()

        back_button = self.draw_button("Back", 50, 500, 200, 50)

        self.draw_text("Audio", 50, 100)
        self.main_volume_text.setText(f"Master: {self.main_volume_slider.getValue()}%")
        self.music_volume_text.setText(f"Music: {self.music_volume_slider.getValue()}%")

        self.main_volume_slider.draw()
        self.music_volume_slider.draw()

        self.main_volume_text.draw()
        self.music_volume_text.draw()

        if self.click:
            if back_button.collidepoint(mx, my):
                self.current_screen = "main_menu"
            else:
                self.main_volume = int(self.main_volume_slider.getValue())
                self.music_volume = int(self.music_volume_slider.getValue())

        pygame_widgets.update(pygame.event.get())

    def draw_text(self, text, x, y, color=(255, 255, 255)):
        text_obj = self.font.render(text, True, color)
        self.screen.blit(text_obj, (x, y))

    def draw_button(self, text, x, y, width, height):
        button = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, (255, 255, 255), button)
        self.draw_text(text, x + 10, y + 10, (0, 0, 0))
        return button
    
    def draw_slider(self, x, y, width, height, value):
        pygame.draw.rect(self.screen, (200, 200, 200), (x, y, width, height))  
        slider_x = x + int((value / 100) * width) - 5 
        pygame.draw.rect(self.screen, (255, 0, 0), (slider_x, y, 10, height))  
        return pygame.Rect(slider_x, y, 10, height)
