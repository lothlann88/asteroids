import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, ASTEROID_MIN_RADIUS
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from button import Button

player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

def score_for_radius(radius):
    if radius <= ASTEROID_MIN_RADIUS:
        return 100
    if radius <= ASTEROID_MIN_RADIUS * 2:
        return 50
    return 20

def init_game():
    """
    Initialize game state including sprite groups, containers, player, and asteroid field.
    
    Returns:
        tuple: (updatable, drawable, asteroids, shots, player) sprite groups and player instance
    """
    # Sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)
    
    # create player
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    # create asteroid field
    AsteroidField()
    
    return updatable, drawable, asteroids, shots, player

def show_game_over_screen(screen, final_score, clock):
    """
    Display game over screen with final score and buttons to play again or exit.
    
    Args:
        screen: pygame.Surface to draw on
        final_score: Final score to display
        clock: pygame.time.Clock for frame rate control
        
    Returns:
        str: "play_again" if Play Again button clicked, "exit" if Exit button clicked
    """
    # Create fonts
    title_font = pygame.font.Font(None, 72)
    score_font = pygame.font.Font(None, 48)
    
    # Create buttons
    button_width = 200
    button_height = 60
    button_y_spacing = 80
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2
    
    play_again_button = Button(
        center_x, 
        center_y + button_y_spacing // 2, 
        button_width, 
        button_height, 
        "Play Again",
        color=(50, 150, 50),
        hover_color=(70, 200, 70)
    )
    
    exit_button = Button(
        center_x, 
        center_y + button_y_spacing // 2 + button_height + 20, 
        button_width, 
        button_height, 
        "Exit",
        color=(150, 50, 50),
        hover_color=(200, 70, 70)
    )
    
    # Game over screen loop
    running = True
    while running:
        mouse_clicked = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_clicked = True
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Update buttons
        if play_again_button.update(mouse_pos, mouse_clicked):
            return "play_again"
        if exit_button.update(mouse_pos, mouse_clicked):
            return "exit"
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Draw "Game Over" text
        title_text = title_font.render("Game Over", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(center_x, center_y - 100))
        screen.blit(title_text, title_rect)
        
        # Draw final score
        score_text = score_font.render(f"Final Score: {final_score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(center_x, center_y - 40))
        screen.blit(score_text, score_rect)
        
        # Draw buttons
        play_again_button.draw(screen)
        exit_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

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

    # Initialize game
    updatable, drawable, asteroids, shots, player = init_game()

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
                    # Show game over screen
                    action = show_game_over_screen(screen, score, clock)
                    if action == "play_again":
                        # Reset game state
                        score = 0
                        lives = 3
                        score_surface = font.render(f"Score: {score}", True, "white")
                        lives_surface = font.render(f"Lives: {lives}", True, "white")
                        # Clear all sprites
                        for shot in list(shots):
                            shot.kill()
                        for asteroid in list(asteroids):
                            asteroid.kill()
                        for sprite in list(updatable):
                            sprite.kill()
                        # Reinitialize game
                        updatable, drawable, asteroids, shots, player = init_game()
                    elif action == "exit":
                        running = False
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
