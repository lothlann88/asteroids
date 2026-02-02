import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, ASTEROID_MIN_RADIUS
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
import sys
from shot import Shot

player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

def score_for_radius(radius):
    if radius <= ASTEROID_MIN_RADIUS:
        return 100
    if radius <= ASTEROID_MIN_RADIUS * 2:
        return 50
    return 20

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}") 
    print(f"Screen height: {SCREEN_HEIGHT}")
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    # display score and lives
    score = 0
    font = pygame.font.Font(None, 36)
    score_surface = font.render(f"Score: {score}", True, "white")
    lives = 3
    lives_surface = font.render(f"Lives: {lives}", True, "white")
    # load background image
    background_image = pygame.image.load("Background Image.png")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable,drawable)
    Asteroid.containers = (asteroids,updatable,drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots,updatable,drawable)
    # create player
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    # create asteroid field
    AsteroidField()

    # Game loop
    running = True
    while running == True:
        
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # Update sprites in updatable group
        updatable.update(dt)
        for asteroid in asteroids:
            # check if player collides with asteroid
            if asteroid.collides_with(player):
                lives -= 1
                lives_surface = font.render(f"Lives: {lives}", True, "white")
                log_event("player_hit")
                if lives <= 0:
                    print("Game over!")
                    print(f"Player hit asteroid with radius {asteroid.radius}")
                    print(f"Final Score: {score}")
                    sys.exit()
                else:
                    print("Player respawned")
                    print(f"lives remaining: {lives}")
                    player.kill()
                    for shot in list(shots):
                        shot.kill()
                    for asteroid in list(asteroids):
                        asteroid.kill()
                    for sprite in list(updatable):
                        if isinstance(sprite, AsteroidField):
                            sprite.kill()
                    AsteroidField()
                    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        for asteroid in asteroids:
            # check if asteroid collides with shot
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    score += score_for_radius(asteroid.radius)
                    score_surface = font.render(f"Score: {score}", True, "white")
                    log_event(f"asteroid_shot_score_{score_for_radius(asteroid.radius)}")
                    shot.kill()
                    asteroid.asteroid_split()
        # Draw background image
        screen.blit(background_image, (0, 0))
        #screen.fill("black")

        # Draw sprites in drawable group    
        for obj in drawable:
            obj.draw(screen)
        screen.blit(score_surface, (16, 16))
        screen.blit(lives_surface, (16, 48))
        pygame.display.flip()
        # FPS limit enforced and checked after each frame
        dt = clock.tick(60) / 1000.0



    

if __name__ == "__main__":
    main()
