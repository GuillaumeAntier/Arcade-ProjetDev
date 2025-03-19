import pygame
import math

class Bullet:
    def __init__(self, id, direction, speed, damage, x=0, y=0):
        self.id = id
        self.position = [x, y]
        self.direction = direction  
        self.speed = speed
        self.damage = damage
        self.image = pygame.image.load("graphics/bullet.png").convert_alpha()
        self.update_rotated_image()  
        self.to_destroy = False 

    def update_rotated_image(self):
        self.rotated_image = pygame.transform.rotate(self.image, -self.direction - 90)  
        self.rect = self.rotated_image.get_rect(center=self.position)

    def update(self):
        rad = math.radians(self.direction)
        self.position[0] += self.speed * math.cos(rad)
        self.position[1] += self.speed * math.sin(rad)
        print(f"Bullet {self.id} position: {self.position}") 

        self.update_rotated_image()

    def check_collision(self, player):
        hitbox_points = player.get_hitbox_points()
        
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
        
        collision = point_in_polygon(self.position, hitbox_points)
        if collision:
            self.to_destroy = True 
        return collision

    def render(self, screen):
        screen.blit(self.rotated_image, self.rect.topleft)
        
        pygame.draw.circle(screen, (255, 0, 0), [int(self.position[0]), int(self.position[1])], 2)

    def destroy(self):
        self.to_destroy = True