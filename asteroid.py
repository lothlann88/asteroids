import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event
import random
class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self._shape = self._build_shape()

    def _build_shape(self):
        points = []
        vertex_count = random.randint(8, 14)
        for i in range(vertex_count):
            angle = (i / vertex_count) * 360
            jitter = random.uniform(0.7, 1.15)
            distance = self.radius * jitter
            points.append(pygame.Vector2(0, 1).rotate(angle) * distance)
        return points

    def draw(self, screen):
        points = [self.position + p for p in self._shape]
        pygame.draw.polygon(screen, "white", points, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt

    def asteroid_split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            log_event("asteroid_split")
            random_vector = random.uniform(20,50)
            new_asteroid_1_vector = self.velocity.rotate(random_vector)
            new_asteroid_2_vector = self.velocity.rotate(-random_vector)
            new_asteroid_radius = self.radius - ASTEROID_MIN_RADIUS
            new_asteroid_1 = Asteroid(self.position.x, self.position.y, new_asteroid_radius)
            new_asteroid_1.velocity = new_asteroid_1_vector
            new_asteroid_2 = Asteroid(self.position.x, self.position.y, new_asteroid_radius)
            new_asteroid_2.velocity = new_asteroid_2_vector
