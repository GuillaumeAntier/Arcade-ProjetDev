from player import Player
from screenManager import ScreenManager
import pygame
import serial
import re
import os
from map_manager import MapManager
from database import Database

class Game:

    def __init__(self):
        pygame.init()  
        self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN) 
        self.db = Database('database.sqlite')
        self.board = ScreenManager(self.db)
        self.map_manager = MapManager()
        self.current_map = self.map_manager.select_random_map()  
        
        # Initialize database
        self.db.create_table("scores", "id INTEGER PRIMARY KEY, player_name TEXT, score INTEGER")
        
        # Load player settings
        self.player_settings = self.db.load_settings()
        
        # Initialize default settings if not found in database
        if '1' not in self.player_settings:
            self.player_settings['1'] = {
                'rotation_speed': 1,
                'movement_speed': 5,
                'health_points': 100,
                'firepower': 10,
                'fire_rate': 1,
                'bullet_speed': 15
            }
        
        if '2' not in self.player_settings:
            self.player_settings['2'] = {
                'rotation_speed': 1,
                'movement_speed': 5,
                'health_points': 100,
                'firepower': 10,
                'fire_rate': 1,
                'bullet_speed': 15
            }
        
        # Initialize players with settings
        spawn_points = self.current_map.get_spawn_points()
        self.players = [
            Player('1', spawn_points[0][0], spawn_points[0][1], self.player_settings['1']), 
            Player('2', spawn_points[1][0], spawn_points[1][1], self.player_settings['2'])
        ]
        
        self.scores = []
        self.current_screen = "main_menu"
        self.game_over = False
        self.game_over_timer = 0
        self.winner = None
        
        pygame.display.set_caption(f"Tank Battle - Map: {self.current_map.name}")
        
        try:
            self.arduino = serial.Serial(port="COM7", baudrate=9600, timeout=1)
        except serial.SerialException as e:
            print(f"Erreur de connexion au port série : {e}")
            print("Utilisation du mode clavier")
            self.arduino = None  
        
        # Initialize fonts for game over messages
        self.font_large = pygame.font.SysFont(None, 72)
        self.font_medium = pygame.font.SysFont(None, 48)
        
        # Share settings with ScreenManager
        self.board.player_settings = self.player_settings
        self.board.on_settings_changed = self.on_settings_changed

    def on_settings_changed(self, settings):
        """Called when settings are changed in the ScreenManager"""
        self.player_settings = settings
        self.db.save_settings(self.player_settings)
        
        # Update player settings
        for player in self.players:
            if player.id in self.player_settings:
                player.apply_settings(self.player_settings[player.id])

    def read_joystick(self):
        if self.arduino and self.arduino.in_waiting > 0:
            data = self.arduino.readline().decode("utf-8").strip()
            try:
                j1_match = re.search(r'J1\[X:(\d+) Y:(\d+) B:(\d+)\]', data)
                j2_match = re.search(r'J2\[X:(\d+) Y:(\d+) B:(\d+)\]', data)
                a1_match = re.search(r'A1:(\d+)', data)
                b1_match = re.search(r'B1:(\d+)', data)
                a2_match = re.search(r'A2:(\d+)', data)
                b2_match = re.search(r'B2:(\d+)', data)
                
                if j1_match and j2_match and a1_match and b1_match and a2_match and b2_match:
                    j1_x = int(j1_match.group(1))
                    j1_y = int(j1_match.group(2))
                    j1_b = int(j1_match.group(3))
                    j2_x = int(j2_match.group(1))
                    j2_y = int(j2_match.group(2))
                    j2_b = int(j2_match.group(3))
                    a1 = int(a1_match.group(1))
                    b1 = int(b1_match.group(1))
                    a2 = int(a2_match.group(1))
                    b2 = int(b2_match.group(1))
                    
                    return {
                        'joystick1': {
                            'x': j1_x,
                            'y': j1_y,
                            'b': j1_b,
                            'a': a1,
                            'b_btn': b1
                        },
                        'joystick2': {
                            'x': j2_x,
                            'y': j2_y,
                            'b': j2_b,
                            'a': a2,
                            'b_btn': b2
                        }
                    }
                else:
                    print(f"Format de données non reconnu: {data}")
            except ValueError as e:
                print(f"Erreur de conversion des données du joystick: {e}")
                print(f"Données reçues: {data}")
        
        elif not self.arduino:
            keys = pygame.key.get_pressed()
            
            j1_x = 512
            j1_y = 512
            if keys[pygame.K_a]: j1_x = 312  # Gauche
            if keys[pygame.K_d]: j1_x = 712  # Droite
            if keys[pygame.K_w]: j1_y = 312  # Haut
            if keys[pygame.K_s]: j1_y = 712  # Bas
            
            j2_x = 512
            j2_y = 512
            if keys[pygame.K_LEFT]: j2_x = 312  # Gauche
            if keys[pygame.K_RIGHT]: j2_x = 712  # Droite
            if keys[pygame.K_UP]: j2_y = 312  # Haut
            if keys[pygame.K_DOWN]: j2_y = 712  # Bas
            
            a1 = 0 if keys[pygame.K_SPACE] else 1 
            b1 = 0 if keys[pygame.K_q] else 1  
            a2 = 0 if keys[pygame.K_RETURN] else 1 
            b2 = 0 if keys[pygame.K_RSHIFT] else 1 
            
            return {
                'joystick1': {
                    'x': j1_x,
                    'y': j1_y,
                    'b': 1,
                    'a': a1,
                    'b_btn': b1
                },
                'joystick2': {
                    'x': j2_x,
                    'y': j2_y,
                    'b': 1,
                    'a': a2,
                    'b_btn': b2
                }
            }
            
        return None

    def check_collision_with_obstacles(self, player):
        """Vérifie si un joueur entre en collision avec un obstacle sur la carte"""
        return self.current_map.check_collision(player.position, (player.hitbox_width, player.hitbox_height))

    def run(self):
        running = True
        print("Démarrage de la boucle principale...")
        print(f"Map actuelle: {self.current_map.name}")
        
        clock = pygame.time.Clock()
        
        # Initialize the ScreenManager
        self.board.current_screen = "main_menu"
        
        while running:
            # Handle common events for all screens
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.board.current_screen == "game":
                            self.board.is_paused = not self.board.is_paused
                        elif self.board.current_screen != "main_menu":
                            self.board.current_screen = "main_menu"
                        else:
                            running = False
            
            # Process screens based on the current state
            if self.board.current_screen == "main_menu":
                self.board.update_screen()
                self.board.handle_events()
                
                # If game was selected from menu
                if self.board.current_screen == "game":
                    self.reset_game()
                
            elif self.board.current_screen == "game":
                if self.board.is_paused:
                    self.board.update_screen()
                    self.board.handle_events()
                elif self.game_over:
                    self.handle_game_over()
                else:
                    self.update_game_state(clock)
            
            # Other screens handled by ScreenManager
            elif self.board.current_screen in ["options", "tutorial"]:
                self.board.update_screen()
                self.board.handle_events()
            
            pygame.display.flip()
            clock.tick(60)  # Limit to 60 FPS
        
        # Save settings before quitting
        self.db.save_settings(self.player_settings)
        
        pygame.quit()

    def update_game_state(self, clock):
        joystick_data = self.read_joystick()
        
        # Check for game over condition
        for i, player in enumerate(self.players):
            if player.health_points <= 0:
                self.game_over = True
                self.winner = "Player " + self.players[1-i].id  # Other player is the winner
                self.game_over_timer = pygame.time.get_ticks()
                
                # Save score to database
                self.db.save_score(self.winner, 1)
                return
        
        # Regular game update
        previous_positions = [player.position.copy() for player in self.players]
        
        if joystick_data:
            self.players[0].update(joystick_data['joystick1'], 1) 
            self.players[1].update(joystick_data['joystick2'], 2)  
        
        for i, player in enumerate(self.players):
            if self.check_collision_with_obstacles(player):
                player.position = previous_positions[i]

        for player in self.players:
            for bullet in player.bullets:
                previous_position = bullet.position.copy()
                bullet.update()
                
                if self.current_map.check_collision(bullet.position, (10, 10)):
                    bullet.to_destroy = True

        for i, player in enumerate(self.players):
            if player.health_points <= 0:
                continue
            
            for other_i, other_player in enumerate(self.players):
                if i != other_i:  # Don't check collision with yourself
                    bullets_to_remove = []
                    for bullet_idx, bullet in enumerate(other_player.bullets):
                        if bullet.check_collision(player):
                            print(f"Player {player.id} hit by bullet from Player {other_player.id}")
                            if player.take_damage(bullet.damage):
                                print(f"Player {player.id} has been defeated!")
                            bullets_to_remove.append(bullet_idx)
                    
                    for idx in sorted(bullets_to_remove, reverse=True):
                        if idx < len(other_player.bullets):
                            other_player.bullets.pop(idx)

        for player in self.players:
            player.cleanup_bullets()

        # Render the game
        self.current_map.render(self.screen)
        
        for player in self.players:
            player.render(self.screen)
        
        # Display map info
        font = pygame.font.SysFont(None, 24)
        map_text = font.render(f"Map: {self.current_map.name}", True, (255, 255, 255))
        self.screen.blit(map_text, (10, 10))

    def handle_game_over(self):
        # Check if we should return to main menu
        current_time = pygame.time.get_ticks()
        if current_time - self.game_over_timer > 5000:  # Return to main menu after 5 seconds
            self.board.current_screen = "main_menu"
            self.game_over = False
            return
        
        # Continue rendering game state
        self.current_map.render(self.screen)
        for player in self.players:
            player.render(self.screen)
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))
        
        # Draw game over message
        game_over_text = self.font_large.render("GAME OVER", True, (255, 0, 0))
        winner_text = self.font_medium.render(f"{self.winner} Wins!", True, (255, 255, 0))
        return_text = self.font_medium.render("Returning to main menu...", True, (255, 255, 255))
        
        self.screen.blit(game_over_text, 
                        (self.screen.get_width() // 2 - game_over_text.get_width() // 2, 
                         self.screen.get_height() // 2 - 100))
        self.screen.blit(winner_text, 
                        (self.screen.get_width() // 2 - winner_text.get_width() // 2, 
                         self.screen.get_height() // 2))
        self.screen.blit(return_text, 
                        (self.screen.get_width() // 2 - return_text.get_width() // 2, 
                         self.screen.get_height() // 2 + 100))
        
        # Handle any key press to speed up return to main menu
        keys = pygame.key.get_pressed()
        if any(keys) or pygame.mouse.get_pressed()[0]:
            self.board.current_screen = "main_menu"
            self.game_over = False
    
    def reset_game(self):
        # Reset map and players
        self.current_map = self.map_manager.select_random_map()
        spawn_points = self.current_map.get_spawn_points()
        
        # Reset player positions and states
        self.players = [
            Player('1', spawn_points[0][0], spawn_points[0][1], self.player_settings['1']), 
            Player('2', spawn_points[1][0], spawn_points[1][1], self.player_settings['2'])
        ]
        
        self.game_over = False
        self.winner = None
        
        pygame.display.set_caption(f"Tank Battle - Map: {self.current_map.name}")
        print(f"New game started. Map: {self.current_map.name}")

    def handle_events(self):
        return

    def update(self):
        return

    def render(self):
        return

    def change_screen(self, screen_name):
        self.board.current_screen = screen_name