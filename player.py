import math
import pygame
import os
from bullet import Bullet

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
        self.bullets = []  # Liste pour stocker les balles
        self.last_shot_time = 0  # Pour contrôler la cadence de tir
        self.hitbox_width = 30  # Largeur de la hitbox
        self.hitbox_height = 30  # Hauteur de la hitbox
        
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

    def shoot(self, joystick_data):
        if joystick_data:
            x, y, button = joystick_data
            current_time = pygame.time.get_ticks()
            # Vérifiez si assez de temps s'est écoulé depuis le dernier tir
            if button == 0 and current_time - self.last_shot_time > 100 / self.fire_rate:  # Temps en millisecondes
                self.last_shot_time = current_time
                
                # Calculez la position du bout du canon (layer 5)
                # Obtenir l'angle en radians
                rad_angle = math.radians(self.angle - 90)  # Ajustez l'angle pour correspondre à la direction du tank
                
                # La longueur du canon depuis le centre du tank
                canon_length = 50  # Ajustez selon la taille réelle de votre sprite stack
                
                # Calculez la position du bout du canon
                canon_x = self.position[0] + canon_length * math.cos(rad_angle)
                canon_y = self.position[1] + 4 * -4 + canon_length * math.sin(rad_angle)
                
                # Créez la balle avec la bonne direction et position
                bullet = Bullet(
                    id=len(self.bullets), 
                    direction=self.angle - 90,  # Ajustez l'angle pour correspondre à la direction du tank
                    speed=self.bullet_speed,  # Augmentez la vitesse pour un meilleur effet
                    damage=self.firepower, 
                    x=canon_x, 
                    y=canon_y
                )
                self.bullets.append(bullet)

    def take_damage(self, amount):
        self.health_points -= amount
        if self.health_points < 0:
            self.health_points = 0
        return self.health_points <= 0  # Retourne True si le joueur est mort

    def update(self, joystick_data):
        if joystick_data:
            x, y, button = joystick_data
            dx = (x - 512) / 512
            dy = (y - 512) / 512
            
            if abs(dx) > 0.1 or abs(dy) > 0.1:
                self.angle = (math.degrees(math.atan2(dy, dx)) + 90) % 360  
                self.position[0] += dx * self.movement_speed * 2
                self.position[1] += dy * self.movement_speed * 2

            self.shoot(joystick_data)
        
        # Mettre à jour les balles et supprimer celles qui sont hors écran
        bullets_to_remove = []
        for i, bullet in enumerate(self.bullets):
            bullet.update()
            # Vérifiez si la balle est hors écran (ajustez les valeurs selon la taille de votre écran)
            if (bullet.position[0] < 0 or bullet.position[0] > 1000 or 
                bullet.position[1] < 0 or bullet.position[1] > 1000):
                bullets_to_remove.append(i)
        
        # Supprimez les balles hors écran
        for i in sorted(bullets_to_remove, reverse=True):
            if i < len(self.bullets):
                self.bullets.pop(i)

    def get_hitbox_points(self):
        """Retourne les 4 points du rectangle de hitbox après rotation"""
        # Définir les points du rectangle non tourné
        half_width = self.hitbox_width / 2
        half_height = self.hitbox_height / 2
        
        # Points du rectangle par rapport au centre (position du tank)
        points = [
            [-half_width, -half_height],  # Haut gauche
            [half_width, -half_height],   # Haut droite
            [half_width, half_height],    # Bas droite
            [-half_width, half_height]    # Bas gauche
        ]
        
        # Convertir l'angle en radians
        rad_angle = math.radians(self.angle)
        
        # Calculer les nouvelles positions des points après rotation
        rotated_points = []
        for x, y in points:
            # Appliquer la rotation
            rotated_x = x * math.cos(rad_angle) - y * math.sin(rad_angle)
            rotated_y = x * math.sin(rad_angle) + y * math.cos(rad_angle)
            
            # Ajouter la position du centre
            rotated_points.append([
                self.position[0] + rotated_x,
                self.position[1] + rotated_y
            ])
            
        return rotated_points

    def render(self, screen):
        # Dessiner le sprite stack (les couches de l'image du tank)
        for i, layer_image in enumerate(self.tank_surface):
            rotated_image = pygame.transform.rotate(layer_image, -self.angle)
            # Ajustez la position verticale pour l'effet de stack
            new_rect = rotated_image.get_rect(center=(self.position[0], self.position[1] + i * -4))
            screen.blit(rotated_image, new_rect.topleft)
        
        # Dessiner la hitbox qui tourne avec le tank
        hitbox_points = self.get_hitbox_points()
        pygame.draw.polygon(screen, (255, 0, 0), hitbox_points, 1)  # Dessiner avec une épaisseur de 1 pixel
            
        # Rendre les balles
        for bullet in self.bullets:
            bullet.render(screen)

    def reset(self):
        self.health_points = 100
        self.bullets = []
        return