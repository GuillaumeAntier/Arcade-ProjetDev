import pygame
import random
import os

class Map:
    def __init__(self, name, obstacles=None, width=1920, height=1080, background_color=(10, 10, 10)):
        self.name = name
        self.width = width
        self.height = height
        self.background_color = background_color
        self.obstacles = obstacles if obstacles else []
        self.background_image = None
        
    def load_background(self, image_path):
        """Load a background image for the map"""
        if os.path.exists(image_path):
            self.background_image = pygame.image.load(image_path).convert()
            self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))
        else:
            print(f"Background image not found: {image_path}")
            
    def render(self, screen):
        """Render the map on the screen"""
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        else:
            screen.fill(self.background_color)
            
        for obstacle in self.obstacles:
            obstacle.render(screen)
            
    def check_collision(self, position, size):
        """Check if a position collides with any obstacle"""
        for obstacle in self.obstacles:
            if obstacle.check_collision(position, size):
                return True
        return False
        
    def get_spawn_points(self):
        """Return spawn points for players based on the map"""
        return [(400, 540), (1520, 540)]


class Obstacle:
    def __init__(self, x, y, width, height, color=(100, 100, 100)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.image = None
        
    def load_image(self, image_path):
        """Load an image for the obstacle"""
        if os.path.exists(image_path):
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        else:
            print(f"Obstacle image not found: {image_path}")
            
    def render(self, screen):
        """Render the obstacle on the screen"""
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, self.color, self.rect)
            
    def check_collision(self, position, size):
        """Check if a position collides with this obstacle"""
        player_rect = pygame.Rect(position[0] - size[0]/2, position[1] - size[1]/2, size[0], size[1])
        return self.rect.colliderect(player_rect)


class MapManager:
    def __init__(self):
        self.maps = []
        self.current_map = None
        self._create_predefined_maps()
        
    def _create_predefined_maps(self):
        """Create predefined maps"""
        empty_map = Map("Empty Arena")
        self.maps.append(empty_map)
        
        four_corners = Map("Four Corners")
        four_corners.obstacles = [
            Obstacle(0, 0, 400, 400),
            Obstacle(1520, 0, 400, 400),
            Obstacle(0, 680, 400, 400),
            Obstacle(1520, 680, 400, 400)
        ]
        self.maps.append(four_corners)
        
        central_fortress = Map("Central Fortress")
        central_fortress.obstacles = [
            Obstacle(860, 440, 200, 200),
            Obstacle(0, 0, 200, 200),
            Obstacle(1720, 0, 200, 200),
            Obstacle(0, 880, 200, 200),
            Obstacle(1720, 880, 200, 200)
        ]
        self.maps.append(central_fortress)
        
        maze = Map("Maze")
        maze.obstacles = [
            Obstacle(400, 0, 60, 680),
            Obstacle(800, 400, 60, 680),
            Obstacle(1200, 0, 60, 680),
            Obstacle(1600, 400, 60, 680),
            Obstacle(0, 400, 400, 60),
            Obstacle(1200, 400, 400, 60),
            Obstacle(400, 800, 400, 60),
            Obstacle(1600, 800, 320, 60)
        ]
        self.maps.append(maze)
        
        corridors = Map("Corridors")
        corridors.obstacles = [
            Obstacle(0, 300, 1520, 60),
            Obstacle(400, 700, 1520, 60),
            Obstacle(800, 0, 60, 250),
            Obstacle(1200, 400, 60, 250),
            Obstacle(600, 800, 60, 280),
            Obstacle(1400, 800, 60, 280)
        ]
        self.maps.append(corridors)
        
        symmetrical = Map("Symmetrical")
        symmetrical.obstacles = [
            Obstacle(910, 440, 100, 200),
            
            Obstacle(300, 200, 150, 150),
            Obstacle(300, 730, 150, 150),
            Obstacle(600, 440, 100, 200),
            
            Obstacle(1470, 200, 150, 150),
            Obstacle(1470, 730, 150, 150),
            Obstacle(1220, 440, 100, 200)
        ]
        self.maps.append(symmetrical)
        
        # Scattered map
        scattered = Map("Scattered")
        scattered.obstacles = [
            Obstacle(300, 200, 100, 100),
            Obstacle(700, 300, 100, 100),
            Obstacle(1100, 200, 100, 100),
            Obstacle(1500, 300, 100, 100),
            Obstacle(300, 600, 100, 100),
            Obstacle(700, 700, 100, 100),
            Obstacle(1100, 600, 100, 100),
            Obstacle(1500, 700, 100, 100),
            Obstacle(960, 540, 100, 100)
        ]
        self.maps.append(scattered)
        
    def select_random_map(self):
        """Select a random map from the predefined maps"""
        self.current_map = random.choice(self.maps)
        return self.current_map
        
    def get_map_by_name(self, name):
        """Get a map by its name"""
        for map in self.maps:
            if map.name.lower() == name.lower():
                self.current_map = map
                return map
        return None