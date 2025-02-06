class Bullet :
    
    def __init__(self, id, direction, speed, damage, x=0, y=0):

        self.id = id
        self.position = [x, y]
        self.direction = direction
        self.speed = speed
        self.damage = damage
        
    def update(self) :
        return
    
    def check_collision(player) :
        return
    
    def destroy(self) :
        return