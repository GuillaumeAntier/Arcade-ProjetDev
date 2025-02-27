import math
import pygame
import os

class Player:

    def __init__(self, id, x=0, y=0):

        self.id = id
        self.name = ""
        self.rotation_speed = 1
        self.movement_speed = 1
        self.health_points = 100
        self.firepower = 1
        self.fire_rate = 1
        self.bullet_speed = 1
        self.position = [x, y]
        self.angle = 0
        self.tank_surface = self.create_tank_surface()  
        
    def create_tank_surface(self):
        layer_images = []
        for i in range(6):  
            image_path = os.path.join("graphics", f"tank-0{i}.png")
            print(f"Loading image from: {image_path}") 
            if os.path.exists(image_path):
                layer_image = pygame.image.load(image_path).convert_alpha()
                layer_images.append(layer_image)
            else:
                print(f"Image non trouvée : {image_path}")

        return layer_images 

    def set_position(self, x, y):
        self.position = [x, y]
    
    def set_name(self, name) :
        self.name = name
        return

    def move(self, dx, dy):
        self.position[0] += dx
        self.position[1] += dy

    def rotate(self, angle):
        self.angle = angle

    def shoot(self):
        return

    def take_damage(self, amount):
        return

    def update(self, joystick_data):
        if joystick_data:
            x, y, button = joystick_data
            dx = (x - 512) / 512
            dy = (y - 512) / 512
            
            if abs(dx) > 0.1 or abs(dy) > 0.1:
                self.angle = (math.degrees(math.atan2(dy, dx)) + 90) % 360  
                self.position[0] += dx * 2 
                self.position[1] += dy * 2

    def render(self, screen):
        for i, layer_image in enumerate(self.tank_surface):
            rotated_image = pygame.transform.rotate(layer_image, -self.angle) 
            new_rect = rotated_image.get_rect(center=(self.position[0], self.position[1] + i * -4))
            screen.blit(rotated_image, new_rect.topleft) 
            
    def reset(self):
        return
