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
        self.bg_tile = None
        self.tile_size = 128  
        
    def load_background(self, image_path):
        if os.path.exists(image_path):
            self.bg_tile = pygame.image.load(image_path).convert()
        else:
            print(f"Background image not found: {image_path}")
            
    def render(self, screen):
        if self.bg_tile:
            for y in range(0, self.height, self.tile_size):
                for x in range(0, self.width, self.tile_size):
                    screen.blit(self.bg_tile, (x, y))
        else:
            screen.fill(self.background_color)
            
        for obstacle in self.obstacles:
            obstacle.render(screen)
            
    def check_collision(self, position, size):
        for obstacle in self.obstacles:
            if obstacle.check_collision(position, size):
                return True
        return False
        
    def get_spawn_points(self):
        return [(300, 540), (1520, 540)]


class Obstacle:
    def __init__(self, x, y, width, height, color=(100, 100, 100)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.image = None
        self.tile = None
        self.tile_size = 64  
        
    def load_image(self, image_path):
        if os.path.exists(image_path):
            self.tile = pygame.image.load(image_path).convert_alpha()
        else:
            print(f"Obstacle image not found: {image_path}")
            
    def render(self, screen):
        if self.tile:
            temp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            
            for y in range(0, self.height, self.tile_size):
                for x in range(0, self.width, self.tile_size):
                    draw_width = min(self.tile_size, self.width - x)
                    draw_height = min(self.tile_size, self.height - y)
                    
                    temp_surface.blit(self.tile.subsurface((0, 0, draw_width, draw_height)), (x, y))
            screen.blit(temp_surface, (self.x, self.y))
        else:
            pygame.draw.rect(screen, self.color, self.rect)
            
    def check_collision(self, position, size):
        player_rect = pygame.Rect(position[0] - size[0]/2, position[1] - size[1]/2, size[0], size[1])
        return self.rect.colliderect(player_rect)


class MapManager:
    def __init__(self):
        self.maps = []
        self.current_map = None
        self.stone_wall_texture = None
        self.grass_texture = None
        self.load_textures()
        self._create_predefined_maps()
        
    def load_textures(self):
        stone_wall_path = "static/map/stone-wall-texture.png"
        grass_path = "static/map/grass-texture.png"
        
        if os.path.exists(stone_wall_path):
            self.stone_wall_texture = stone_wall_path
        else:
            print(f"Stone wall texture not found: {stone_wall_path}")
            
        if os.path.exists(grass_path):
            self.grass_texture = grass_path
        else:
            print(f"Grass texture not found: {grass_path}")
        
    def _create_predefined_maps(self):
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
        
        self.apply_textures_to_maps()
        
    def apply_textures_to_maps(self):
        for map in self.maps:
            if self.grass_texture:
                map.load_background(self.grass_texture)
            if self.stone_wall_texture:
                for obstacle in map.obstacles:
                    obstacle.load_image(self.stone_wall_texture)
        
    def select_random_map(self):
        self.current_map = random.choice(self.maps)
        return self.current_map
        
    def get_map_by_name(self, name):
        for map in self.maps:
            if map.name.lower() == name.lower():
                self.current_map = map
                return map
        return None