import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, ASTEROID_MIN_RADIUS, UFO_SCORE
from logger import log_state, log_event, log_leaderboard_score
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from button import Button
from ufo import UFO, UFOShot, UFOField

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
    ufos = pygame.sprite.Group()
    ufo_shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    UFO.containers = (ufos, updatable, drawable)
    UFOShot.containers = (ufo_shots, updatable, drawable)
    UFOField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)
    
    # create player
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    # create asteroid field
    AsteroidField()
    # create ufo field
    UFOField.player = player
    UFOField()
    
    return updatable, drawable, asteroids, shots, ufos, ufo_shots, player

def show_game_over_screen(screen, final_score, clock):
    """
    Display game over screen with final score and buttons to play again or exit.
    
    Args:
        screen: pygame.Surface to draw on
        final_score: Final score to display
        clock: pygame.time.Clock for frame rate control
        
    Returns:
        tuple: ("play_again" or "exit", player_name)
    """
    # Create fonts
    title_font = pygame.font.Font(None, 72)
    score_font = pygame.font.Font(None, 48)
    
    # Create buttons
    button_width = 200
    button_height = 60
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2

    title_y = center_y - 160
    score_y = center_y - 100
    name_label_y = center_y - 40
    input_y = center_y - 10
    play_again_y = center_y + 70
    exit_y = center_y + 150
    
    play_again_button = Button(
        center_x, 
        play_again_y, 
        button_width, 
        button_height, 
        "Play Again",
        color=(50, 150, 50),
        hover_color=(70, 200, 70)
    )
    
    exit_button = Button(
        center_x, 
        exit_y, 
        button_width, 
        button_height, 
        "Exit",
        color=(150, 50, 50),
        hover_color=(200, 70, 70)
    )

    # Name input
    name = ""
    max_name_length = 16
    input_width = 320
    input_height = 48
    input_rect = pygame.Rect(
        center_x - input_width // 2,
        input_y,
        input_width,
        input_height,
    )
    input_active = True
    
    # Game over screen loop
    running = True
    while running:
        mouse_clicked = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit", name
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_clicked = True
                    input_active = input_rect.collidepoint(event.pos)
            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN:
                    return "play_again", name
                else:
                    if len(name) < max_name_length and event.unicode.isprintable():
                        name += event.unicode
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Update buttons
        if play_again_button.update(mouse_pos, mouse_clicked):
            return "play_again", name
        if exit_button.update(mouse_pos, mouse_clicked):
            return "exit", name
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Draw "Game Over" text
        title_text = title_font.render("Game Over", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(center_x, title_y))
        screen.blit(title_text, title_rect)
        
        # Draw final score
        score_text = score_font.render(f"Final Score: {final_score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(center_x, score_y))
        screen.blit(score_text, score_rect)

        # Draw name input
        name_label = score_font.render("Name:", True, (255, 255, 255))
        name_label_rect = name_label.get_rect(center=(center_x, name_label_y))
        screen.blit(name_label, name_label_rect)

        input_color = (255, 255, 255) if input_active else (180, 180, 180)
        pygame.draw.rect(screen, (30, 30, 30), input_rect)
        pygame.draw.rect(screen, input_color, input_rect, 2)

        display_name = name if name else "Enter name"
        name_color = (255, 255, 255) if name else (140, 140, 140)
        name_text = score_font.render(display_name, True, name_color)
        name_text_rect = name_text.get_rect(midleft=(input_rect.x + 10, input_rect.centery))
        screen.blit(name_text, name_text_rect)
        
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
    updatable, drawable, asteroids, shots, ufos, ufo_shots, player = init_game()

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
                distance = player.position.distance_to(asteroid.position)
                nearest = None
                for other in asteroids:
                    if not other.alive():
                        continue
                    d = player.position.distance_to(other.position)
                    if nearest is None or d < nearest[0]:
                        nearest = (d, other)
                log_event(
                    "player_hit",
                    player_pos=[round(player.position.x, 2), round(player.position.y, 2)],
                    player_radius=player.radius,
                    asteroid_pos=[round(asteroid.position.x, 2), round(asteroid.position.y, 2)],
                    asteroid_radius=asteroid.radius,
                    distance=round(distance, 2),
                    collides=distance <= player.radius + asteroid.radius,
                    asteroid_alive=asteroid.alive(),
                    nearest_asteroid_pos=[
                        round(nearest[1].position.x, 2),
                        round(nearest[1].position.y, 2),
                    ]
                    if nearest
                    else None,
                    nearest_asteroid_radius=nearest[1].radius if nearest else None,
                    nearest_asteroid_distance=round(nearest[0], 2) if nearest else None,
                )
                if lives <= 0:
                    print("Game over!")
                    print(f"Player hit asteroid with radius {asteroid.radius}")
                    print(f"Final Score: {score}")
                    # Show game over screen
                    action, player_name = show_game_over_screen(screen, score, clock)
                    log_leaderboard_score(player_name, score)
                    if action == "play_again":
                        # Reset game state
                        score = 0
                        lives = 3
                        score_surface = font.render(f"Score: {score}", True, "white")
                        lives_surface = font.render(f"Lives: {lives}", True, "white")
                        # Clear all sprites
                        for shot in list(shots):
                            shot.kill()
                        for ufo_shot in list(ufo_shots):
                            ufo_shot.kill()
                        for asteroid in list(asteroids):
                            asteroid.kill()
                        for ufo in list(ufos):
                            ufo.kill()
                        for sprite in list(updatable):
                            sprite.kill()
                        # Reinitialize game
                        updatable, drawable, asteroids, shots, ufos, ufo_shots, player = init_game()
                    elif action == "exit":
                        running = False
                else:
                    print("Player respawned")
                    print(f"lives remaining: {lives}")
                    player.kill()
                    for shot in list(shots):
                        shot.kill()
                    for ufo_shot in list(ufo_shots):
                        ufo_shot.kill()
                    for asteroid in list(asteroids):
                        asteroid.kill()
                    for ufo in list(ufos):
                        ufo.kill()
                    for sprite in list(updatable):
                        if isinstance(sprite, (AsteroidField, UFOField)):
                            sprite.kill()
                    AsteroidField()
                    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    UFOField.player = player
                    UFOField()
        for asteroid in asteroids:
            if not asteroid.alive():
                continue
            # check if asteroid collides with shot
            for shot in shots:
                if not shot.alive():
                    continue
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    score += score_for_radius(asteroid.radius)
                    score_surface = font.render(f"Score: {score}", True, "white")
                    log_event(f"asteroid_shot_score_{score_for_radius(asteroid.radius)}")
                    shot.kill()
                    asteroid.asteroid_split()
                    break
        for ufo in ufos:
            if not ufo.alive():
                continue
            # check if player collides with ufo
            if ufo.collides_with(player):
                lives -= 1
                lives_surface = font.render(f"Lives: {lives}", True, "white")
                distance = player.position.distance_to(ufo.position)
                log_event(
                    "player_hit_ufo",
                    player_pos=[round(player.position.x, 2), round(player.position.y, 2)],
                    player_radius=player.radius,
                    ufo_pos=[round(ufo.position.x, 2), round(ufo.position.y, 2)],
                    ufo_radius=ufo.radius,
                    distance=round(distance, 2),
                    collides=distance <= player.radius + ufo.radius,
                    ufo_alive=ufo.alive(),
                )
                if lives <= 0:
                    print("Game over!")
                    print(f"Player hit ufo")
                    print(f"Final Score: {score}")
                    action, player_name = show_game_over_screen(screen, score, clock)
                    log_leaderboard_score(player_name, score)
                    if action == "play_again":
                        score = 0
                        lives = 3
                        score_surface = font.render(f"Score: {score}", True, "white")
                        lives_surface = font.render(f"Lives: {lives}", True, "white")
                        for shot in list(shots):
                            shot.kill()
                        for ufo_shot in list(ufo_shots):
                            ufo_shot.kill()
                        for asteroid in list(asteroids):
                            asteroid.kill()
                        for ufo in list(ufos):
                            ufo.kill()
                        for sprite in list(updatable):
                            sprite.kill()
                        updatable, drawable, asteroids, shots, ufos, ufo_shots, player = init_game()
                    elif action == "exit":
                        running = False
                else:
                    print("Player respawned")
                    print(f"lives remaining: {lives}")
                    player.kill()
                    for shot in list(shots):
                        shot.kill()
                    for ufo_shot in list(ufo_shots):
                        ufo_shot.kill()
                    for asteroid in list(asteroids):
                        asteroid.kill()
                    for ufo in list(ufos):
                        ufo.kill()
                    for sprite in list(updatable):
                        if isinstance(sprite, (AsteroidField, UFOField)):
                            sprite.kill()
                    AsteroidField()
                    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    UFOField.player = player
                    UFOField()
        for ufo_shot in ufo_shots:
            if not ufo_shot.alive():
                continue
            if ufo_shot.collides_with(player):
                lives -= 1
                lives_surface = font.render(f"Lives: {lives}", True, "white")
                distance = player.position.distance_to(ufo_shot.position)
                log_event(
                    "player_hit_ufo_shot",
                    player_pos=[round(player.position.x, 2), round(player.position.y, 2)],
                    player_radius=player.radius,
                    ufo_shot_pos=[round(ufo_shot.position.x, 2), round(ufo_shot.position.y, 2)],
                    ufo_shot_radius=ufo_shot.radius,
                    distance=round(distance, 2),
                    collides=distance <= player.radius + ufo_shot.radius,
                    ufo_shot_alive=ufo_shot.alive(),
                )
                if lives <= 0:
                    print("Game over!")
                    print("Player hit ufo shot")
                    print(f"Final Score: {score}")
                    action, player_name = show_game_over_screen(screen, score, clock)
                    log_leaderboard_score(player_name, score)
                    if action == "play_again":
                        score = 0
                        lives = 3
                        score_surface = font.render(f"Score: {score}", True, "white")
                        lives_surface = font.render(f"Lives: {lives}", True, "white")
                        for shot in list(shots):
                            shot.kill()
                        for ufo_shot in list(ufo_shots):
                            ufo_shot.kill()
                        for asteroid in list(asteroids):
                            asteroid.kill()
                        for ufo in list(ufos):
                            ufo.kill()
                        for sprite in list(updatable):
                            sprite.kill()
                        updatable, drawable, asteroids, shots, ufos, ufo_shots, player = init_game()
                    elif action == "exit":
                        running = False
                else:
                    print("Player respawned")
                    print(f"lives remaining: {lives}")
                    player.kill()
                    for shot in list(shots):
                        shot.kill()
                    for ufo_shot in list(ufo_shots):
                        ufo_shot.kill()
                    for asteroid in list(asteroids):
                        asteroid.kill()
                    for ufo in list(ufos):
                        ufo.kill()
                    for sprite in list(updatable):
                        if isinstance(sprite, (AsteroidField, UFOField)):
                            sprite.kill()
                    AsteroidField()
                    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    UFOField.player = player
                    UFOField()
        for ufo in ufos:
            if not ufo.alive():
                continue
            for shot in shots:
                if not shot.alive():
                    continue
                if ufo.collides_with(shot):
                    log_event("ufo_destroyed")
                    score += UFO_SCORE
                    score_surface = font.render(f"Score: {score}", True, "white")
                    shot.kill()
                    ufo.kill()
                    break
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
