import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state
from player import Player
def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}") 
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()

# FPS limit
    clock = pygame.time.Clock()
    dt = 0

    # Screen setup and initialization
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    running = True
    # Player setup and initialization
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    # Game loop
    while running == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        log_state()
        screen.fill("black")
        # Player draw
        player.draw(screen)
        player.update(dt)
        pygame.display.flip()
        # FPS limit enforced and checked after each frame
        dt = clock.tick(60) / 1000.0



    

if __name__ == "__main__":
    main()