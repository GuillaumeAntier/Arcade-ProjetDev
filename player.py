class Player:

    def __init__(self, id, x=0, y=0):

        self.id = id
        self.rotation_speed = 1
        self.movement_speed = 1
        self.health_points = 100
        self.firepower = 1
        self.fire_rate = 1
        self.bullet_speed = 1

    def move(self, direction):
        return

    def rotate(self, angle):
        return

    def shoot(self):
        return

    def take_damage(self, amount):
        return

    def update(self):
        return

    def reset(self):
        return
