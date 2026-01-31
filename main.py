import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state
def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}") 
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()

# FPS limit
    Clock = pygame.time.Clock()
    dt = 0

    # Screen setup and initialization
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    running = True
    # Game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        log_state()
        screen.fill("black")
        pygame.display.flip()
        # FPS limit enforced and checked after each frame
        dt = Clock.tick(60) / 1000.0
        # print(f"FPS: {Clock.get_fps()}, dt: {dt}")

if __name__ == "__main__":
    main()