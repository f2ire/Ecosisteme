import pygame


def test():
    pygame.init()
    width, height = (200,200)
    screen = pygame.display.set_mode((width, height))

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (30, 30, 30)
    FONT = pygame.font.Font("freesansbold.ttf", 50)
    button = pygame.Rect(0, 100, 200, 200)
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # This block is executed once for each MOUSEBUTTONDOWN event.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 1 is the left mouse button, 2 is middle, 3 is right.
                if event.button == 1:
                    # `event.pos` is the mouse position.
                    if button.collidepoint(event.pos):
                        # Increment the number.
                        return False
                    else :
                        return True

        screen.fill(WHITE)
        pygame.draw.rect(screen, GRAY, button)
        text_surf = FONT.render("yes", True, BLACK)
        # You can pass the center directly to the `get_rect` method.
        text_rect = text_surf.get_rect(center=(100, 50))

        text_surf1 = FONT.render("no", True, BLACK)
        # You can pass the center directly to the `get_rect` method.
        text_rect1 = text_surf.get_rect(center=(100, 150))   

        screen.blit(text_surf, text_rect)
        screen.blit(text_surf1, text_rect1)

        pygame.display.update()
