import pygame
import pygame.mixer

class ScreenManager:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Game')
        
        self.screen = pygame.display.set_mode((1920, 1080))
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.fonts = {
            'default': pygame.font.Font('./static/font/ThaleahFat.ttf', 40),
            'title': pygame.font.Font('./static/font/ThaleahFat.ttf', 150),
            'tutorial': pygame.font.Font('./static/font/ThaleahFat.ttf', 30)
        }
        
        self.current_screen = "main_menu"
        self.previous_screen = None
        self.is_paused = False
        
        self.main_volume = 0
        self.music_volume = 0
        self.dragging_main = False
        self.dragging_music = False
        
        self.menu_configs = {
            "main_menu": ["Game", "Options", "Tutorial", "Exit"],
            "options": ["Main Volume", "Music Volume", "Back"],
            "tutorial": ["Back"],
            "pause": ["Resume", "Options", "Main Menu"],
        }
        self.selected_menu_index = 0
        
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        
        pygame.mixer.music.set_volume((self.main_volume / 100) * (self.music_volume / 100))
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)
        self.current_music = None
        
        self.images = {
            'button': pygame.image.load('./static/design/button.png'),
            'background': pygame.image.load('./static/design/background.jpg'),
            'slider_bg': pygame.image.load('./static/design/slider_bg.png'),
            'slider_button': pygame.image.load('./static/design/slider_button.png'),
            'panel': pygame.image.load('./static/design/panel.png')
        }
        
        self.main_slider_rect = pygame.Rect(0, 0, 0, 0)
        self.music_slider_rect = pygame.Rect(0, 0, 0, 0)
        
        self.click = False
    
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
                
            elif event.type == pygame.KEYDOWN:
                self.handle_key_event(event)
                
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                if self.main_slider_rect.collidepoint(mx, my):
                    self.dragging_main = True
                if self.music_slider_rect.collidepoint(mx, my):
                    self.dragging_music = True
                    
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.dragging_main = False
                self.dragging_music = False
                self.click = True
                
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging_main:
                    self.main_volume = self.update_slider(event.pos[0], 700, 500)
                if self.dragging_music:
                    self.music_volume = self.update_slider(event.pos[0], 700, 500)
                    
            elif event.type == pygame.USEREVENT + 1:
                pygame.mixer.music.play()
                
            elif event.type == pygame.JOYAXISMOTION:
                self.handle_joystick_motion(event)
                
            elif event.type == pygame.JOYBUTTONDOWN and event.button == 0:
                self.activate_menu_item()
        
        pygame.mixer.music.set_volume((self.main_volume / 100) * (self.music_volume / 100))
    
    def handle_key_event(self, event):
        if event.key == pygame.K_ESCAPE:
            if self.current_screen == "game":
                self.is_paused = not self.is_paused
            elif self.current_screen != "main_menu":
                self.current_screen = "main_menu"

        elif event.key == pygame.K_DOWN:
            menu_items = self.get_current_menu_items()
            if len(menu_items) > 0:
                self.selected_menu_index = (self.selected_menu_index + 1) % len(menu_items)
                
        elif event.key == pygame.K_UP:
            menu_items = self.get_current_menu_items()
            if len(menu_items) > 0:
                self.selected_menu_index = (self.selected_menu_index - 1) % len(menu_items)

        elif event.key == pygame.K_RETURN:
            self.activate_menu_item()

        elif event.key == pygame.K_LEFT:
            self.adjust_slider(-1)

        elif event.key == pygame.K_RIGHT:
            self.adjust_slider(1)
    
    def handle_joystick_motion(self, event):
        if event.axis == 1:
            if event.value > 512 + 256:
                self.selected_menu_index = (self.selected_menu_index + 1) % len(self.get_current_menu_items())
            elif event.value < 512 - 256:
                self.selected_menu_index = (self.selected_menu_index - 1) % len(self.get_current_menu_items())
                
        elif event.axis == 0:
            normalized_value = (event.value - 512) / 512
            if self.current_screen == "options":
                if self.selected_menu_index == 0:
                    self.main_volume = max(0, min(100, self.main_volume + int(normalized_value * 10)))
                elif self.selected_menu_index == 1:
                    self.music_volume = max(0, min(100, self.music_volume + int(normalized_value * 10)))
    
    def get_current_menu_items(self):
        if self.is_paused:
            return self.menu_configs["pause"]
        return self.menu_configs.get(self.current_screen, [])
    
    def activate_menu_item(self):
        selected_item = self.get_current_menu_items()[self.selected_menu_index]
        
        if self.current_screen == "main_menu":
            if selected_item == "Game":
                self.current_screen = "game"
                pygame.mixer.music.fadeout(1000)
            elif selected_item == "Options":
                self.previous_screen = "main_menu"
                self.current_screen = "options"
            elif selected_item == "Tutorial":
                self.current_screen = "tutorial"
            elif selected_item == "Exit":
                self.running = False
                
        elif self.current_screen == "options" and selected_item == "Back":
            self.current_screen = self.previous_screen or "main_menu"
            
        elif self.is_paused:
            if selected_item == "Resume":
                self.is_paused = False
            elif selected_item == "Options":
                self.previous_screen = "game"
                self.current_screen = "options"
                self.is_paused = False
            elif selected_item == "Main Menu":
                self.current_screen = "main_menu"
                self.is_paused = False
                
        elif self.current_screen == "tutorial" and selected_item == "Back":
            self.current_screen = "main_menu"
    
    def update_screen(self):
        self.screen.blit(self.images['background'], (0, 0))
        
        if self.current_screen == "main_menu":
            self.draw_main_menu()
        elif self.current_screen == "game":
            self.draw_game_screen()
        elif self.current_screen == "options":
            self.draw_options_screen()
        elif self.current_screen == "tutorial":
            self.draw_tutorial_screen()
    
    def draw_main_menu(self):
        self.play_music('./static/music/menu.mp3')
        
        title_text = "War Game"
        title_rect = self.get_text_rect(title_text, self.screen.get_width() // 2, 150, self.fonts['title'])
        self.draw_text(title_text, title_rect.x, title_rect.y, font=self.fonts['title'])
        
        mx, my = pygame.mouse.get_pos()
        buttons = []
        y_pos = 300
        
        for i, item in enumerate(self.get_current_menu_items()):
            button = self.draw_button(item, 800, y_pos, 300, 150, is_hovered=(self.selected_menu_index == i))
            buttons.append(button)
            y_pos += 175
        
        if self.click:
            for i, button in enumerate(buttons):
                if button.collidepoint(mx, my):
                    self.selected_menu_index = i
                    self.activate_menu_item()
    
    def draw_game_screen(self):
        self.play_music("./static/music/game.mp3")
        
        if self.is_paused:
            self.draw_pause_menu()
    
    def draw_pause_menu(self):
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        title_text = "Pause"
        title_rect = self.get_text_rect(title_text, self.screen.get_width() // 2, 150, self.fonts['title'])
        self.draw_text(title_text, title_rect.x, title_rect.y, font=self.fonts['title'])
        
        mx, my = pygame.mouse.get_pos()
        buttons = []
        y_pos = 300
        
        for i, item in enumerate(self.get_current_menu_items()):
            button = self.draw_button(item, 800, y_pos, 300, 150, is_hovered=(self.selected_menu_index == i))
            buttons.append(button)
            y_pos += 175
        
        if self.click:
            for i, button in enumerate(buttons):
                if button.collidepoint(mx, my):
                    self.selected_menu_index = i
                    self.activate_menu_item()
    
    def draw_options_screen(self):
        mx, my = pygame.mouse.get_pos()
        
        title_text = "Audio"
        title_rect = self.get_text_rect(title_text, self.screen.get_width() // 2, 150, self.fonts['title'])
        self.draw_text(title_text, title_rect.x, title_rect.y, font=self.fonts['title'])
        
        self.draw_text(f"Master: {self.main_volume}", 700, 275)
        self.draw_text(f"Music: {self.music_volume}", 700, 525)
        
        self.main_slider_rect = self.draw_slider(700, 350, 500, 120, self.main_volume, 
                                                is_hovered=(self.selected_menu_index == 0))
        self.music_slider_rect = self.draw_slider(700, 600, 500, 120, self.music_volume, 
                                                 is_hovered=(self.selected_menu_index == 1))
        
        back_button = self.draw_button("Back", 800, 825, 300, 150, 
                                      is_hovered=(self.selected_menu_index == 2))
        
        buttons = [self.main_slider_rect, self.music_slider_rect, back_button]
        if self.click:
            for i, button in enumerate(buttons):
                if button.collidepoint(mx, my):
                    self.selected_menu_index = i
                    self.activate_menu_item()
    
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
        
        panel_x, panel_y = 275, 210
        panel_width, panel_height = 1400, 600
        panel_image = pygame.transform.scale(self.images['panel'], (panel_width, panel_height))
        self.screen.blit(panel_image, (panel_x, panel_y))
        
        title_text = "Tutorial"
        title_rect = self.get_text_rect(title_text, self.screen.get_width() // 2, 150, self.fonts['title'])
        self.draw_text(title_text, title_rect.x, title_rect.y, font=self.fonts['title'])
        
        y_offset = 350
        for line in tutorial_text:
            self.draw_text(line, 500, y_offset, font=self.fonts['tutorial'])
            y_offset += 20
        
        mx, my = pygame.mouse.get_pos()
        back_button = self.draw_button("Back", 800, 825, 300, 150, 
                                      is_hovered=(self.selected_menu_index == 0))
        
        if self.click and back_button.collidepoint(mx, my):
            self.selected_menu_index = 0
            self.activate_menu_item()
    
    def draw_text(self, text, x, y, start_color=(255, 255, 0), end_color=(255, 165, 0), 
                 outline_color=(0, 0, 0), font=None):
        if font is None:
            font = self.fonts['default']
        
        if font == self.fonts['title']:
            outline_width = 10
        elif font == self.fonts['tutorial']:
            outline_width = 2
        else:
            outline_width = 4
            
        outline_positions = [
            (x-outline_width, y-outline_width), (x+outline_width, y-outline_width),
            (x-outline_width, y+outline_width), (x+outline_width, y+outline_width),
            (x-outline_width, y), (x+outline_width, y),
            (x, y-outline_width), (x, y+outline_width)
        ]
        
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
    
    def get_text_rect(self, text, center_x, center_y, font):
        text_surface = font.render(text, True, (255, 255, 0))
        text_rect = text_surface.get_rect(center=(center_x, center_y))
        return text_rect
    
    def draw_button(self, text, x, y, width, height, is_hovered=False):
        scale_factor = 1.1 if is_hovered else 1.0
        scaled_width = int(width * scale_factor)
        scaled_height = int(height * scale_factor)
        
        button = pygame.Rect(
            x - (scaled_width - width) // 2, 
            y - (scaled_height - height) // 2, 
            scaled_width, scaled_height
        )
        
        button_image = pygame.transform.scale(self.images['button'], (scaled_width, scaled_height))
        self.screen.blit(button_image, (button.x, button.y))
        
        text_obj = self.fonts['default'].render(text, True, (255, 255, 0))
        text_rect = text_obj.get_rect(center=(button.x + scaled_width // 2, button.y + scaled_height // 2))
        
        self.draw_text(text, text_rect.x, text_rect.y)
        
        return button
    
    def draw_slider(self, x, y, width, height, value, is_hovered=False):
        slider_bg = pygame.transform.scale(self.images['slider_bg'], (width, height))
        self.screen.blit(slider_bg, (x, y))
        
        scale_factor = 1.1 if is_hovered else 1.0
        button_width = int(100 * scale_factor)
        button_height = int(100 * scale_factor)
        
        slider_button = pygame.transform.scale(
            self.images['slider_button'], 
            (button_width, button_height)
        )
        
        left_margin = 20
        right_margin = 20
        usable_width = width - button_width - left_margin - right_margin
        slider_x = x + left_margin + int((value / 100) * usable_width)
        slider_y = y - 20
        
        self.screen.blit(slider_button, (slider_x, slider_y))
        
        return pygame.Rect(slider_x, slider_y, button_width, button_height)
    
    def update_slider(self, mouse_x, slider_x, slider_width):
        button_width = 100
        left_margin = 20
        right_margin = 20
        usable_width = slider_width - button_width - left_margin - right_margin
        
        clamped_x = max(
            slider_x + left_margin, 
            min(mouse_x, slider_x + slider_width - right_margin - button_width)
        )
        
        relative_x = clamped_x - (slider_x + left_margin)
        new_value = (relative_x / usable_width) * 100
        
        return max(0, min(100, int(new_value)))
    
    def play_music(self, music_path):
        if self.current_music == music_path:
            return
            
        self.current_music = music_path
        
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(500)
        
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)
    
    def adjust_slider(self, direction):
        if self.current_screen == "options":
            if self.selected_menu_index == 0:
                self.main_volume = max(0, min(100, self.main_volume + direction * 5))
            elif self.selected_menu_index == 1:
                self.music_volume = max(0, min(100, self.music_volume + direction * 5))
