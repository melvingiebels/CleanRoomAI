import pygame

class Button:
    def __init__(self, x, y, width, height, text, color, font_color, font_size):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font_color = font_color
        self.font_size = font_size

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, self.font_size)
        text_surface = font.render(self.text, True, self.font_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)
