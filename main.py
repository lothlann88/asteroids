import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state
from player import Player


player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}") 
    print(f"Screen height: {SCREEN_HEIGHT}")
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

# Sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    Player.containers = (updatable,drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)





    # Game loop
    running = True
    while running == True:
        
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # Update sprites in updatable group
        updatable.update(dt)

        screen.fill("black")
        # Draw sprites in drawable group    
        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()
        # FPS limit enforced and checked after each frame
        dt = clock.tick(60) / 1000.0



    

if __name__ == "__main__":
    main()