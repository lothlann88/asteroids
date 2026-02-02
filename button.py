import pygame


class Button:
    def __init__(self, x, y, width, height, text, color=(100, 100, 100), hover_color=(150, 150, 150), text_color=(255, 255, 255), font_size=36):
        """
        Create a button with hover and click detection.
        
        Args:
            x: X position of the button (center)
            y: Y position of the button (center)
            width: Width of the button
            height: Height of the button
            text: Text to display on the button
            color: Normal button color (RGB tuple)
            hover_color: Button color when hovered (RGB tuple)
            text_color: Text color (RGB tuple)
            font_size: Font size for the text
        """
        self.rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pygame.font.Font(None, font_size)
        self.is_hovered = False
        self.was_clicked = False
        
    def update(self, mouse_pos, mouse_clicked):
        """
        Update button state based on mouse position and click.
        
        Args:
            mouse_pos: Tuple of (x, y) mouse position
            mouse_clicked: Boolean indicating if mouse button was clicked this frame
            
        Returns:
            True if button was clicked, False otherwise
        """
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        if mouse_clicked and self.is_hovered:
            if not self.was_clicked:
                self.was_clicked = True
                return True
        else:
            self.was_clicked = False
            
        return False
    
    def draw(self, screen):
        """
        Draw the button on the screen.
        
        Args:
            screen: pygame.Surface to draw on
        """
        # Choose color based on hover state
        current_color = self.hover_color if self.is_hovered else self.color
        
        # Draw button rectangle
        pygame.draw.rect(screen, current_color, self.rect)
        pygame.draw.rect(screen, self.text_color, self.rect, 2)  # Border
        
        # Render and center text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
