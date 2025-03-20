import math
import pygame
import os
from bullet import Bullet

class Player:

    def __init__(self, id, x=0, y=0):
        self.id = id
        self.name = ""
        self.rotation_speed = 1
        self.movement_speed = 5
        self.health_points = 100
        self.firepower = 10
        self.fire_rate = 1
        self.bullet_speed = 15 
        self.position = [x, y]
        self.angle = 0
        self.tank_surface = self.create_tank_surface()  
        self.bullets = []  
        self.last_shot_time = 0 
        self.hitbox_width = 80 
        self.hitbox_height = 90  
        self.previous_a_button = 1 
        
    def create_tank_surface(self):
        layer_images = []
        for i in range(6):  
            if self.id == '1':
                image_path = os.path.join("graphics", f"green-tank-0{i}.png")
            else:
                image_path = os.path.join("graphics", f"red-tank-0{i}.png")
            print(f"Loading image from: {image_path}") 
            if os.path.exists(image_path):
                layer_image = pygame.image.load(image_path).convert_alpha()
                layer_images.append(layer_image)
            else:
                print(f"Image non trouvée : {image_path}")

        return layer_images 

    def set_position(self, x, y):
        self.position = [x, y]
    
    def set_name(self, name):
        self.name = name
        return

    def move(self, dx, dy):
        self.position[0] += dx
        self.position[1] += dy

    def rotate(self, angle):
        self.angle = angle

    def shoot(self, joystick_data, joystick_id):
        if joystick_data:
            a_button = joystick_data['a']
            current_time = pygame.time.get_ticks()
            
            button_pressed = (self.previous_a_button == 1 and a_button == 0)
            self.previous_a_button = a_button
            
            if button_pressed and current_time - self.last_shot_time > 200 / self.fire_rate: 
                self.last_shot_time = current_time
                
                rad_angle = math.radians(self.angle - 90)
                canon_length = 50
                
                canon_x = self.position[0] + canon_length * math.cos(rad_angle)
                canon_y = self.position[1] + 4 * -4 + canon_length * math.sin(rad_angle)
                
                bullet = Bullet(
                    id=len(self.bullets), 
                    direction=self.angle - 90,
                    speed=self.bullet_speed,
                    damage=self.firepower, 
                    x=canon_x, 
                    y=canon_y
                )
                self.bullets.append(bullet)
                print(f"Player {self.id} (Joystick {joystick_id}) fired a bullet")

    def take_damage(self, amount):
        self.health_points -= amount
        if self.health_points < 0:
            self.health_points = 0
        return self.health_points <= 0  

    def update(self, joystick_data, joystick_id):
        if joystick_data:
            x = joystick_data['x']
            y = joystick_data['y']
            
            dx = (x - 512) / 512
            dy = (y - 512) / 512
            
            if abs(dx) > 0.1 or abs(dy) > 0.1:
                self.angle = (math.degrees(math.atan2(dy, dx)) + 90) % 360
                self.position[0] += dx * self.movement_speed * 2
                self.position[1] += dy * self.movement_speed * 2
            
            self.shoot(joystick_data, joystick_id)
        
        self.position[0] = max(0, min(self.position[0], 1920))
        self.position[1] = max(0, min(self.position[1], 1080))

    def cleanup_bullets(self):
        self.bullets = [bullet for bullet in self.bullets if 
                        (0 <= bullet.position[0] <= 1920 and 
                         0 <= bullet.position[1] <= 1080 and
                         not bullet.to_destroy)]

    def get_hitbox_points(self):
        """Retourne les 4 points du rectangle de hitbox après rotation"""
        half_width = self.hitbox_width / 2
        half_height = self.hitbox_height / 2
        
        points = [
            [-half_width, -half_height],  
            [half_width, -half_height],   
            [half_width, half_height],    
            [-half_width, half_height]    
        ]
        
        rad_angle = math.radians(self.angle)
        
        rotated_points = []
        for x, y in points:
            rotated_x = x * math.cos(rad_angle) - y * math.sin(rad_angle)
            rotated_y = x * math.sin(rad_angle) + y * math.cos(rad_angle)
            
            rotated_points.append([
                self.position[0] + rotated_x,
                self.position[1] + rotated_y
            ])
            
        return rotated_points

    def render(self, screen):
        for i, layer_image in enumerate(self.tank_surface):
            rotated_image = pygame.transform.rotate(layer_image, -self.angle)
            new_rect = rotated_image.get_rect(center=(self.position[0], self.position[1] + i * -4))
            screen.blit(rotated_image, new_rect.topleft)
        
        hitbox_points = self.get_hitbox_points()
        pygame.draw.polygon(screen, (255, 0, 0), hitbox_points, 1) 
        
        font = pygame.font.SysFont(None, 24)
        health_text = font.render(f"Player {self.id}: {self.health_points} HP", True, (255, 255, 255))
        screen.blit(health_text, (self.position[0] - 50, self.position[1] - 50))
            
        for bullet in self.bullets:
            bullet.render(screen)

    def reset(self):
        self.health_points = 100
        self.bullets = []
        self.angle = 0
        return