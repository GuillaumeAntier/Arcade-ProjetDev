import pygame
import pygame.mixer

class ScreenManager:
    def __init__(self, db):
        pygame.init()
        pygame.display.set_caption('Game')
        
        self.screen = pygame.display.set_mode((1920, 1080))
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.db = db
        
        self.fonts = {
            'default': pygame.font.Font('./static/font/ThaleahFat.ttf', 40),
            'title': pygame.font.Font('./static/font/ThaleahFat.ttf', 150),
            'tutorial': pygame.font.Font('./static/font/ThaleahFat.ttf', 30)
        }
        
        self.current_screen = "main_menu"
        self.previous_screen = None
        self.is_paused = False
        
        self.main_volume = 50  # Default to 50%
        self.music_volume = 50  # Default to 50%
        self.dragging_main = False
        self.dragging_music = False
        
        # Initialize player settings
        self.player_settings = {
            '1': {
                'rotation_speed': 50,
                'movement_speed': 50,
                'health_points': 100,
                'firepower': 50,
                'fire_rate': 50,
                'bullet_speed': 50
            },
            '2': {
                'rotation_speed': 50,
                'movement_speed': 50,
                'health_points': 100,
                'firepower': 50,
                'fire_rate': 50,
                'bullet_speed': 50
            }
        }
        
        # Player settings slider rects
        self.player_slider_rects = {
            '1': {
                'rotation_speed': pygame.Rect(0, 0, 0, 0),
                'movement_speed': pygame.Rect(0, 0, 0, 0),
                'health_points': pygame.Rect(0, 0, 0, 0),
                'firepower': pygame.Rect(0, 0, 0, 0),
                'fire_rate': pygame.Rect(0, 0, 0, 0),
                'bullet_speed': pygame.Rect(0, 0, 0, 0)
            },
            '2': {
                'rotation_speed': pygame.Rect(0, 0, 0, 0),
                'movement_speed': pygame.Rect(0, 0, 0, 0),
                'health_points': pygame.Rect(0, 0, 0, 0),
                'firepower': pygame.Rect(0, 0, 0, 0),
                'fire_rate': pygame.Rect(0, 0, 0, 0),
                'bullet_speed': pygame.Rect(0, 0, 0, 0)
            }
        }
        
        # Track which slider is currently being dragged
        self.dragging_slider = None
        
        self.menu_configs = {
            "main_menu": ["Game", "Options", "Tutorial", "Exit"],
            "options": ["Main Volume", "Music Volume", "Back"],
            "tutorial": ["Back"],
            "pause": ["Resume", "Options", "Main Menu"],
        }
        
        # Define the option screen items for navigation
        self.options_items = [
            "Main Volume", "Music Volume", 
            "P1 Rotation", "P1 Movement", "P1 Health", "P1 Firepower", "P1 Fire Rate", "P1 Bullet Speed",
            "P2 Rotation", "P2 Movement", "P2 Health", "P2 Firepower", "P2 Fire Rate", "P2 Bullet Speed",
            "Back"
        ]
        
        self.selected_menu_index = 0
        self.options_selected_index = 0
        
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
        
        self.BUTTON_SPACING = 20  # Spacing between buttons
    
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
                
                # Check volume sliders
                if self.main_slider_rect.collidepoint(mx, my):
                    self.dragging_main = True
                    self.dragging_slider = "main"
                elif self.music_slider_rect.collidepoint(mx, my):
                    self.dragging_music = True
                    self.dragging_slider = "music"
                
                # Check player settings sliders
                for player_id in ['1', '2']:
                    for setting, rect in self.player_slider_rects[player_id].items():
                        if rect.collidepoint(mx, my):
                            self.dragging_slider = f"player_{player_id}_{setting}"
                            
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.dragging_main = False
                self.dragging_music = False
                self.dragging_slider = None
                self.click = True
                
            elif event.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_pos()
                
                if self.dragging_slider:
                    if self.dragging_slider == "main":
                        self.main_volume = self.update_slider(mx, 760, 400)
                    elif self.dragging_slider == "music":
                        self.music_volume = self.update_slider(mx, 760, 400)
                    elif self.dragging_slider.startswith("player_"):
                        parts = self.dragging_slider.split("_", 2)  
                        if len(parts) >= 3:
                            _, player_id, setting = parts
                            slider_x = 760 if player_id == '1' else 1240
                            self.player_settings[player_id][setting] = self.update_slider(mx, slider_x, 400)
                    
            elif event.type == pygame.USEREVENT + 1:
                pygame.mixer.music.play()
                
            elif event.type == pygame.JOYAXISMOTION:
                self.handle_joystick_motion(event)
                
            elif event.type == pygame.JOYBUTTONDOWN and event.button == 0:
                self.activate_menu_item()
        
        pygame.mixer.music.set_volume((self.main_volume / 100) * (self.music_volume / 100))
        
        # Update player settings based on sliders 
        for player_id in ['1', '2']:
            settings = self.player_settings[player_id]
            self.db.save_settings(self.player_settings)  # Save settings
    
    def handle_key_event(self, event):
        if event.key == pygame.K_ESCAPE:
            if self.current_screen == "game":
                self.is_paused = not self.is_paused
            elif self.current_screen != "main_menu":
                self.current_screen = "main_menu"
                self.selected_menu_index = 0

        elif event.key == pygame.K_DOWN:
            if self.current_screen == "options":
                self.options_selected_index = (self.options_selected_index + 1) % len(self.options_items)
            else:
                menu_items = self.get_current_menu_items()
                if len(menu_items) > 0:
                    self.selected_menu_index = (self.selected_menu_index + 1) % len(menu_items)
                
        elif event.key == pygame.K_UP:
            if self.current_screen == "options":
                self.options_selected_index = (self.options_selected_index - 1) % len(self.options_items)
            else:
                menu_items = self.get_current_menu_items()
                if len(menu_items) > 0:
                    self.selected_menu_index = (self.selected_menu_index - 1) % len(menu_items)

        elif event.key == pygame.K_RETURN:
            if self.current_screen == "options" and self.options_selected_index == len(self.options_items) - 1:
                # Back button in options
                self.current_screen = self.previous_screen or "main_menu"
                self.selected_menu_index = 0
            else:
                self.activate_menu_item()

        elif event.key == pygame.K_LEFT:
            self.adjust_slider(-5)

        elif event.key == pygame.K_RIGHT:
            self.adjust_slider(5)
    
    def handle_joystick_motion(self, event):
        if event.axis == 1:  # Vertical axis
            if event.value > 0.5:  # Down
                if self.current_screen == "options":
                    self.options_selected_index = (self.options_selected_index + 1) % len(self.options_items)
                else:
                    self.selected_menu_index = (self.selected_menu_index + 1) % len(self.get_current_menu_items())
            elif event.value < -0.5:  # Up
                if self.current_screen == "options":
                    self.options_selected_index = (self.options_selected_index - 1) % len(self.options_items)
                else:
                    self.selected_menu_index = (self.selected_menu_index - 1) % len(self.get_current_menu_items())
                
        elif event.axis == 0:  # Horizontal axis
            if abs(event.value) > 0.5:
                normalized_value = event.value * 5  # Adjust sensitivity
                self.adjust_slider(int(normalized_value))
    
    def get_current_menu_items(self):
        if self.is_paused:
            return self.menu_configs["pause"]
        return self.menu_configs.get(self.current_screen, [])
    
    def activate_menu_item(self):
        if self.current_screen == "options":
            if self.options_selected_index == len(self.options_items) - 1:  # Back button
                self.current_screen = self.previous_screen or "main_menu"
                self.selected_menu_index = 0
            return
        
        selected_item = self.get_current_menu_items()[self.selected_menu_index]
        
        if self.current_screen == "main_menu":
            if selected_item == "Game":
                self.current_screen = "game"
                pygame.mixer.music.fadeout(1000)
            elif selected_item == "Options":
                self.previous_screen = "main_menu"
                self.current_screen = "options"
                self.options_selected_index = 0
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
                self.options_selected_index = 0
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
        y_pos = 300  # Starting position for first button
        
        for i, item in enumerate(self.get_current_menu_items()):
            button = self.draw_button(item, self.screen.get_width() // 2 - 150, y_pos, 300, 150, is_hovered=(self.selected_menu_index == i))
            buttons.append(button)
            y_pos += 175 + self.BUTTON_SPACING  # Add spacing between buttons
        
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
            button = self.draw_button(item, self.screen.get_width() // 2 - 150, y_pos, 300, 150, is_hovered=(self.selected_menu_index == i))
            buttons.append(button)
            y_pos += 175
        
        if self.click:
            for i, button in enumerate(buttons):
                if button.collidepoint(mx, my):
                    self.selected_menu_index = i
                    self.activate_menu_item()
    
    def draw_options_screen(self):
        # Draw title
        title_text = "Options"
        title_rect = self.get_text_rect(title_text, self.screen.get_width() // 2, 100, self.fonts['title'])
        self.draw_text(title_text, title_rect.x, title_rect.y, font=self.fonts['title'])
        
        mx, my = pygame.mouse.get_pos()
        
        # Draw two columns for player settings
        col1_x = 300
        col2_x = 1100
        start_y = 220
        spacing = 70
        
        # Draw audio settings
        self.draw_text("Audio Settings", col1_x, start_y)
        self.draw_text(f"Master Volume: {self.main_volume}", col1_x, start_y + spacing)
        self.main_slider_rect = self.draw_slider(col1_x + 360, start_y + spacing, 400, 20, self.main_volume, 
                                                 is_hovered=(self.options_selected_index == 0))
        
        self.draw_text(f"Music Volume: {self.music_volume}", col1_x, start_y + spacing * 2)
        self.music_slider_rect = self.draw_slider(col1_x + 360, start_y + spacing * 2, 400, 20, self.music_volume, 
                                                  is_hovered=(self.options_selected_index == 1))
        
        # Draw player 1 settings
        self.draw_text("Player 1 Settings", col1_x, start_y + spacing * 3)
        
        # Player 1 settings
        settings_y = start_y + spacing * 4
        for i, (setting, value) in enumerate(self.player_settings['1'].items()):
            # Format the setting name nicely
            setting_name = ' '.join(s.capitalize() for s in setting.split('_'))
            self.draw_text(f"{setting_name}: {value}", col1_x, settings_y + spacing * i)
            
            # Draw slider for this setting
            self.player_slider_rects['1'][setting] = self.draw_slider(
                col1_x + 360, 
                settings_y + spacing * i, 
                400, 20, 
                value,
                is_hovered=(self.options_selected_index == 2 + i)
            )
        
        # Draw player 2 settings
        self.draw_text("Player 2 Settings", col2_x, start_y + spacing * 3)
        
        # Player 2 settings
        for i, (setting, value) in enumerate(self.player_settings['2'].items()):
            # Format the setting name nicely
            setting_name = ' '.join(s.capitalize() for s in setting.split('_'))
            self.draw_text(f"{setting_name}: {value}", col2_x, settings_y + spacing * i)
            
            # Draw slider for this setting
            self.player_slider_rects['2'][setting] = self.draw_slider(
                col2_x + 360, 
                settings_y + spacing * i, 
                400, 20, 
                value,
                is_hovered=(self.options_selected_index == 8 + i)
            )
        
        # Draw back button
        back_button = self.draw_button("Back", self.screen.get_width() // 2 - 150, 900, 300, 100, 
                                      is_hovered=(self.options_selected_index == len(self.options_items) - 1))
        
        if self.click and back_button.collidepoint(mx, my):
            self.current_screen = self.previous_screen or "main_menu"
            self.selected_menu_index = 0
    
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
            y_offset += 30  # Increased spacing between lines
        
        mx, my = pygame.mouse.get_pos()
        back_button = self.draw_button("Back", self.screen.get_width() // 2 - 150, 825, 300, 150, 
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
        button_width = int(40 * scale_factor)
        button_height = int(60 * scale_factor)
        
        slider_button = pygame.transform.scale(
            self.images['slider_button'], 
            (button_width, button_height)
        )
        
        left_margin = 10
        right_margin = 10
        usable_width = width - left_margin - right_margin
        slider_x = x + left_margin + int((value / 100) * usable_width) - button_width // 2
        slider_y = y - button_height // 2 + height // 2
        
        self.screen.blit(slider_button, (slider_x, slider_y))
        
        return pygame.Rect(slider_x, slider_y, button_width, button_height)
    
    def update_slider(self, mouse_x, slider_x, slider_width):
        left_margin = 10
        right_margin = 10
        usable_width = slider_width - left_margin - right_margin
        
        # Calculate position relative to the slider
        relative_x = max(0, min(mouse_x - (slider_x + left_margin), usable_width))
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
            if self.options_selected_index == 0:  # Main volume
                self.main_volume = max(0, min(100, self.main_volume + direction))
            elif self.options_selected_index == 1:  # Music volume
                self.music_volume = max(0, min(100, self.music_volume + direction))
            elif 2 <= self.options_selected_index <= 7:  # Player 1 settings
                setting_index = self.options_selected_index - 2
                setting_keys = list(self.player_settings['1'].keys())
                if setting_index < len(setting_keys):
                    setting = setting_keys[setting_index]
                    self.player_settings['1'][setting] = max(0, min(100, self.player_settings['1'][setting] + direction))
            elif 8 <= self.options_selected_index <= 13:  # Player 2 settings
                setting_index = self.options_selected_index - 8
                setting_keys = list(self.player_settings['2'].keys())
                if setting_index < len(setting_keys):
                    setting = setting_keys[setting_index]
                    self.player_settings['2'][setting] = max(0, min(100, self.player_settings['2'][setting] + direction))