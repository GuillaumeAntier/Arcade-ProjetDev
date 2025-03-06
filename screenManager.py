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
        self.font = pygame.font.Font('./static/font/ThaleahFat.ttf', 40)
        self.title_font = pygame.font.Font('./static/font/ThaleahFat.ttf', 150)
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_screen = "main_menu"
        self.main_volume = 0
        self.music_volume = 0

        self.main_volume_slider = Slider(self.screen, 50, 180, 300, 40, min=0, max=100, step=1, initial=self.main_volume)
        self.music_volume_slider = Slider(self.screen, 50, 280, 300, 40, min=0, max=100, step=1, initial=self.music_volume)
        self.main_volume_text = TextBox(self.screen, 50, 150, 100, 30, fontSize=20)
        self.music_volume_text = TextBox(self.screen, 50, 250, 100, 30, fontSize=20)
        self.main_volume_text.disable()
        self.music_volume_text.disable()

        pygame.mixer.music.set_volume((self.main_volume / 100) * (self.music_volume / 100))
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)

        self.button_image = pygame.image.load('./static/design/button.png') 
        self.background_image = pygame.image.load('./static/design/background.jpg')
        self.slider_bg_image = pygame.image.load('./static/design/slider_bg.png')  
        self.slider_button_image = pygame.image.load('./static/design/slider_button.png')  
    
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
            if event.type == pygame.USEREVENT + 1:
                pygame.mixer.music.play()
        
        pygame.mixer.music.set_volume((self.main_volume / 100) * (self.music_volume / 100))

    def update_screen(self):
        self.screen.blit(self.background_image, (0, 0))
        if self.current_screen == "main_menu":
            self.draw_main_menu()
        elif self.current_screen == "game":
            self.draw_game_screen()
        elif self.current_screen == "options":
            self.draw_options_screen()

    def draw_main_menu(self):
        if not pygame.mixer.music.get_busy() or pygame.mixer.music.get_pos() == -1:
            pygame.mixer.music.fadeout(1000)  
            pygame.mixer.music.unload()  
            pygame.mixer.music.load('./static/music/menu.mp3')
            pygame.mixer.music.play(-1)
        text = "War Game"
        text_surface = self.title_font.render(text, True, (255, 255, 0))
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, 150))
        
        self.draw_text(text, text_rect.x, text_rect.y, font=self.title_font)

        mx, my = pygame.mouse.get_pos()
        game_button = self.draw_button("Game", 800, 300, 300, 150)
        options_button = self.draw_button("Options", 800, 475, 300, 150)
        intructions_button = self.draw_button("Tutorial", 800, 650, 300, 150)
        quit_button = self.draw_button("Exit", 800, 825, 300, 150)

        if self.click:
            if game_button.collidepoint(mx, my):
                self.current_screen = "game"
                pygame.mixer.music.fadeout(1000)
            elif options_button.collidepoint(mx, my):
                self.current_screen = "options"
            elif quit_button.collidepoint(mx, my):
                self.running = False

    def draw_game_screen(self):
        if not pygame.mixer.music.get_busy() or pygame.mixer.music.get_pos() == -1:
            pygame.mixer.music.fadeout(1000)  # Faire un fondu de 1 seconde
            pygame.mixer.music.unload()  # Décharger la musique actuelle
            pygame.mixer.music.load('./static/music/game.mp3')
            pygame.mixer.music.play(-1)
        self.draw_text("Game", 20, 20)

        mx, my = pygame.mouse.get_pos()
        back_button = self.draw_button("Back", 800, 825, 300, 150)

        if self.click and back_button.collidepoint(mx, my):
            self.current_screen = "main_menu"   
            pygame.mixer.music.fadeout(1000)

    def draw_options_screen(self):
        mx, my = pygame.mouse.get_pos()

        back_button = self.draw_button("Back", 800, 825, 300, 150)

        text = "Audio"
        text_surface = self.title_font.render(text, True, (255, 255, 0))
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, 150))
        
        self.draw_text(text, text_rect.x, text_rect.y, font=self.title_font)
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
                pygame.mixer.music.set_volume((self.main_volume / 100) * (self.music_volume / 100))

        pygame_widgets.update(pygame.event.get())

    def draw_text(self, text, x, y, start_color=(255, 255, 0), end_color=(255, 165, 0), outline_color=(0, 0, 0), font=None):

        if font is None :
            outline_positions = [(x-4, y-4), (x+4, y-4), (x-4, y+4), (x+4, y+4), (x-4, y), (x+4, y), (x, y-4), (x, y+4)]
        else:
            outline_positions = [(x-10, y-10), (x+10, y-10), (x-10, y+10), (x+10, y+10), (x-10, y), (x+10, y), (x, y-10), (x, y+10)]
        if font is None:
            font = self.font

        for pos in outline_positions:
            text_obj = font.render(text, True, outline_color)
            self.screen.blit(text_obj, pos)
        
        text_surface = font.render(text, True, start_color)
        text_width, text_height = text_surface.get_size()
        gradient_surface = pygame.Surface((text_width, text_height), pygame.SRCALPHA)
        
        for i in range(text_height):
            ratio = i / text_height
            r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
            g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
            b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
            pygame.draw.line(gradient_surface, (r, g, b), (0, i), (text_width, i))
        
        text_surface.blit(gradient_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.screen.blit(text_surface, (x, y))

    def draw_button(self, text, x, y, width, height):
        button = pygame.Rect(x, y, width, height)
        button_image = pygame.transform.scale(self.button_image, (width, height))  
        self.screen.blit(button_image, (x, y))  

        text_obj = self.font.render(text, True, (255, 255, 0))
        text_rect = text_obj.get_rect(center=(x + width // 2, y + height // 2))

        outline_positions = [(text_rect.x-4, text_rect.y-4), (text_rect.x+4, text_rect.y-4), (text_rect.x-4, text_rect.y+4), (text_rect.x+4, text_rect.y+4), (text_rect.x-4, text_rect.y), (text_rect.x+4, text_rect.y), (text_rect.x, text_rect.y-4), (text_rect.x, text_rect.y+4)]
        for pos in outline_positions:
            outline_text_obj = self.font.render(text, True, (0, 0, 0))
            self.screen.blit(outline_text_obj, pos)

        self.draw_text(text, text_rect.x, text_rect.y, start_color=(255, 255, 0), end_color=(255, 165, 0))
        return button
    
    def draw_slider(self, x, y, width, height, value):
        
        slider_bg = pygame.transform.scale(self.slider_bg_image, (width, height))
        self.screen.blit(slider_bg, (x, y))
        
        slider_x = x + int((value / 100) * width) - (self.slider_button_image.get_width() // 2)
        
        self.screen.blit(self.slider_button_image, (slider_x, y))
        
        return pygame.Rect(slider_x, y, self.slider_button_image.get_width(), height)
