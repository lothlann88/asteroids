import pygame
import random
from circleshape import CircleShape
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    LINE_WIDTH,
    UFO_RADIUS,
    UFO_SPEED,
    UFO_SHOT_SPEED,
    UFO_SPAWN_RATE_SECONDS,
)
from logger import log_event


class UFO(CircleShape):
    def __init__(self, x, y, direction):
        super().__init__(x, y, UFO_RADIUS)
        self.velocity = pygame.Vector2(direction * UFO_SPEED, 0)
        self.shot_timer = random.uniform(0.6, 1.2)

    def draw(self, screen):
        body_rect = pygame.Rect(0, 0, self.radius * 2.2, self.radius)
        body_rect.center = self.position
        dome_rect = pygame.Rect(0, 0, self.radius, self.radius * 0.6)
        dome_rect.center = (self.position.x, self.position.y - self.radius * 0.25)

        pygame.draw.ellipse(screen, "white", body_rect, LINE_WIDTH)
        pygame.draw.ellipse(screen, "white", dome_rect, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt
        self.shot_timer -= dt

        if self.shot_timer <= 0 and hasattr(self, "player") and self.player and self.player.alive():
            self.shoot()
            self.shot_timer = random.uniform(0.6, 1.2)

        if (
            self.position.x < -self.radius * 3
            or self.position.x > SCREEN_WIDTH + self.radius * 3
            or self.position.y < -self.radius * 3
            or self.position.y > SCREEN_HEIGHT + self.radius * 3
        ):
            self.kill()

    def shoot(self):
        direction = (self.player.position - self.position)
        if direction.length() == 0:
            direction = pygame.Vector2(0, 1)
        direction = direction.normalize()
        shot = UFOShot(self.position.x, self.position.y, 4)
        shot.velocity = direction * UFO_SHOT_SPEED
        log_event("ufo_shot")


class UFOShot(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "red", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt

        if (
            self.position.x < -self.radius * 2
            or self.position.x > SCREEN_WIDTH + self.radius * 2
            or self.position.y < -self.radius * 2
            or self.position.y > SCREEN_HEIGHT + self.radius * 2
        ):
            self.kill()


class UFOField(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0

    def spawn(self):
        from_left = random.choice([True, False])
        direction = 1 if from_left else -1
        start_x = -UFO_RADIUS * 2 if from_left else SCREEN_WIDTH + UFO_RADIUS * 2
        start_y = random.uniform(UFO_RADIUS * 2, SCREEN_HEIGHT - UFO_RADIUS * 2)
        ufo = UFO(start_x, start_y, direction)
        ufo.player = getattr(self, "player", None)
        log_event("ufo_spawn")

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > UFO_SPAWN_RATE_SECONDS:
            self.spawn_timer = 0
            self.spawn()
