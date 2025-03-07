import pygame, sys
import pygame_widgets
import pygame.mixer 


class ScreenManager:
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Game')
        self.screen = pygame.display.set_mode((1920, 1080))
        self.font = pygame.font.Font('./static/font/ThaleahFat.ttf', 40)
        self.title_font = pygame.font.Font('./static/font/ThaleahFat.ttf', 150)
        self.tutorial_font = pygame.font.Font('./static/font/ThaleahFat.ttf', 30)
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_screen = "main_menu"
        self.main_volume = 0
        self.music_volume = 0
        self.dragging_main = False
        self.dragging_music = False

        pygame.mixer.music.set_volume((self.main_volume / 100) * (self.music_volume / 100))
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)

        self.button_image = pygame.image.load('./static/design/button.png') 
        self.background_image = pygame.image.load('./static/design/background.jpg')
        self.slider_bg_image = pygame.image.load('./static/design/slider_bg.png')  
        self.slider_button_image = pygame.image.load('./static/design/slider_button.png')
        self.panel_image = pygame.image.load('./static/design/panel.png')

        self.main_slider_rect = pygame.Rect(0, 0, 0, 0)
        self.music_slider_rect = pygame.Rect(0, 0, 0, 0)

        self.current_music = None
    
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.current_screen == "game":
                        if not hasattr(self, 'is_paused'):
                            self.is_paused = False
                        self.is_paused = not self.is_paused
                    elif event.key == pygame.K_ESCAPE and self.current_screen != "main_menu":
                        self.running = False
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.click = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                if self.main_slider_rect.collidepoint(mx, my):
                    self.dragging_main = True
                if self.music_slider_rect.collidepoint(mx, my):
                    self.dragging_music = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.dragging_main = False
                self.dragging_music = False
            if event.type == pygame.MOUSEMOTION:
                if self.dragging_main:
                    self.main_volume = self.update_slider(event.pos[0], 700)
                if self.dragging_music:
                    self.music_volume = self.update_slider(event.pos[0], 700)
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
        elif self.current_screen == "tutorial":
            self.draw_tutorial_screen()

    def draw_main_menu(self):
        self.change_music("./static/music/menu.mp3")

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
                self.previous_screen = "main_menu"
                self.current_screen = "options"
            elif intructions_button.collidepoint(mx, my):
                self.current_screen = "tutorial"
            elif quit_button.collidepoint(mx, my):
                self.running = False

    def draw_game_screen(self):
        self.change_music("./static/music/game.mp3")

        if hasattr(self, 'is_paused') and self.is_paused:
            self.draw_pause_menu()
        else:
            self.draw_text("Game", 20, 20)

            mx, my = pygame.mouse.get_pos()
            back_button = self.draw_button("Back", 800, 825, 300, 150)

            if self.click and back_button.collidepoint(mx, my):
                self.current_screen = "main_menu"   

    def draw_pause_menu(self):
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  
        self.screen.blit(overlay, (0, 0))
        
        text = "Pause"
        text_surface = self.title_font.render(text, True, (255, 255, 0))
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, 150))
        self.draw_text(text, text_rect.x, text_rect.y, font=self.title_font)
        
        mx, my = pygame.mouse.get_pos()
        resume_button = self.draw_button("Resume", 800, 300, 300, 150)
        options_button = self.draw_button("Options", 800, 475, 300, 150)
        main_menu_button = self.draw_button("Main Menu", 800, 650, 300, 150)
        
        if self.click:
            if resume_button.collidepoint(mx, my):
                self.is_paused = False
            elif options_button.collidepoint(mx, my):
                self.previous_screen = "game"
                self.current_screen = "options"
                self.is_paused = False
            elif main_menu_button.collidepoint(mx, my):
                self.current_screen = "main_menu"
                self.is_paused = False

    def draw_options_screen(self):
        mx, my = pygame.mouse.get_pos()

        back_button = self.draw_button("Back", 800, 825, 300, 150)

        text = "Audio"
        text_surface = self.title_font.render(text, True, (255, 255, 0))
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, 150))
        
        self.draw_text(text, text_rect.x, text_rect.y, font=self.title_font)
        
        # Dessiner le texte des volumes directement
        self.draw_text(f"Master: {self.main_volume}", 700, 275)
        self.draw_text(f"Music: {self.music_volume}", 700, 525)

        self.main_slider_rect = self.draw_slider(700, 350, 500, 120, self.main_volume)
        self.music_slider_rect = self.draw_slider(700, 600, 500, 120, self.music_volume)

        if self.click and back_button.collidepoint(mx, my):
            self.current_screen = self.previous_screen

    def draw_tutorial_screen(self):
        tutorial_text = [
            "Materiel et Controles :",
            "   - 2 joysticks (1 par joueur)",
            "   - 4 boutons poussoirs (2 par joueur)",
            "   - Navigation complete via joystick et boutons",
            "",
            "Deroulement d'une partie :",
            "   - Les joueurs apparaissent de chaque cote de l'ecran.",
            "   - Le joystick permet de tourner et d'avancer.",
            "   - Un bouton permet de tirer un projectile.",
            "   - Lorsqu'un projectile touche un joueur, il perd des points de vie.",
            "   - La partie se termine quand un joueur n'a plus de points de vie.",
            "",
            "Options et Personnalisation :",
            "   - Modifier la puissance, vitesse et autres statistiques des joueurs.",
            "   - Sauvegarde des scores en base de donnees.",
        ]

        panel_x = 275
        panel_y = 210
        panel_width = 1400
        panel_height = 600
        panel_image = pygame.transform.scale(self.panel_image, (panel_width, panel_height))
        self.screen.blit(panel_image, (panel_x, panel_y))

        y_offset = 350
        text = "Tutorial"
        text_surface = self.title_font.render(text, True, (255, 255, 0))
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, 150))
        
        self.draw_text(text, text_rect.x, text_rect.y, font=self.title_font)
        for line in tutorial_text:
            self.draw_text(line, 500, y_offset, font=self.tutorial_font)
            y_offset += 20 

        mx, my = pygame.mouse.get_pos()
        back_button = self.draw_button("Back", 800, 825, 300, 150)

        if self.click and back_button.collidepoint(mx, my):
            self.current_screen = "main_menu"
        pygame.display.update()

    def draw_text(self, text, x, y, start_color=(255, 255, 0), end_color=(255, 165, 0), outline_color=(0, 0, 0), font=None):

        if font is None :
            outline_positions = [(x-4, y-4), (x+4, y-4), (x-4, y+4), (x+4, y+4), (x-4, y), (x+4, y), (x, y-4), (x, y+4)]
        elif font == self.title_font:
            outline_positions = [(x-10, y-10), (x+10, y-10), (x-10, y+10), (x+10, y+10), (x-10, y), (x+10, y), (x, y-10), (x, y+10)]
        else:
            outline_positions = [(x-2, y-2), (x+2, y-2), (x-2, y+2), (x+2, y+2), (x-2, y), (x+2, y), (x, y-2), (x, y+2)]
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
        
        button_width = 100 
        button_height = 100
        slider_button = pygame.transform.scale(self.slider_button_image, (button_width, button_height))

        left_margin = 20
        right_margin = 20
        
        usable_width = width - button_width - left_margin - right_margin
        slider_x = x + left_margin + int((value / 100) * usable_width)
        slider_y = y - 20
        
        self.screen.blit(slider_button, (slider_x, slider_y))
        
        
        return pygame.Rect(slider_x, slider_y, button_width, button_height)
        
    def update_slider(self, mouse_x, slider_x):
        slider_width = 500
        slider_start_x = 700
        button_width = 100
        left_margin = 10
        right_margin = 10
        
        usable_width = slider_width - button_width - left_margin - right_margin

        clamped_x = max(slider_x + left_margin, min(mouse_x, slider_x + slider_width - right_margin - button_width))

        
        relative_x = clamped_x - (slider_x + left_margin)
        
        new_value = (relative_x / usable_width) * 100
        
        return max(0, min(100, int(new_value)))
    
    def change_music(self, new_music):
        if self.current_music == new_music:
            return  

        self.current_music = new_music

        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(500)  

        pygame.mixer.music.stop()  
        pygame.mixer.music.unload()  
        pygame.mixer.music.load(new_music)  
        pygame.mixer.music.play(-1) 



