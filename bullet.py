import pygame
import math

class Bullet:
    def __init__(self, id, direction, speed, damage, x=0, y=0):
        self.id = id
        self.position = [x, y]
        self.direction = direction  # Angle in degrees
        self.speed = speed
        self.damage = damage
        self.image = pygame.image.load("graphics/bullet.png").convert_alpha()
        self.update_rotated_image()  # Initialiser l'image tournée

    def update_rotated_image(self):
        # Mettre à jour l'image tournée en fonction de la direction
        self.rotated_image = pygame.transform.rotate(self.image, -self.direction - 90)  # Inverser l'angle pour Pygame
        self.rect = self.rotated_image.get_rect(center=self.position)

    def update(self):
        # Convertir l'angle en radians pour le mouvement
        rad = math.radians(self.direction)
        self.position[0] += self.speed * math.cos(rad)
        self.position[1] += self.speed * math.sin(rad)

        # Mise à jour du rectangle de la balle
        self.update_rotated_image()  # Mettre à jour l'image tournée à chaque mouvement

    def check_collision(self, player):
        # Vérifiez si la balle touche la hitbox du joueur (qui tourne)
        hitbox_points = player.get_hitbox_points()
        
        # Utiliser la méthode du point-in-polygon
        def point_in_polygon(point, polygon):
            x, y = point
            n = len(polygon)
            inside = False
            
            p1x, p1y = polygon[0]
            for i in range(n + 1):
                p2x, p2y = polygon[i % n]
                if y > min(p1y, p2y):
                    if y <= max(p1y, p2y):
                        if x <= max(p1x, p2x):
                            if p1y != p2y:
                                xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                            if p1x == p2x or x <= xinters:
                                inside = not inside
                p1x, p1y = p2x, p2y
            
            return inside
        
        # Vérifier si le centre de la balle est dans la hitbox du joueur
        return point_in_polygon(self.position, hitbox_points)

    def render(self, screen):
        # Dessinez la balle tournée à sa position
        screen.blit(self.rotated_image, self.rect.topleft)
        
        # Option: dessinez un petit point rouge au centre de la balle pour le débogage
        pygame.draw.circle(screen, (255, 0, 0), [int(self.position[0]), int(self.position[1])], 2)

    def destroy(self):
        return