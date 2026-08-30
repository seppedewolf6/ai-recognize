import pygame

from character import Character

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

pygame.display.set_caption(
    "AI Gesture Controller"
)

clock = pygame.time.Clock()

character = Character(
    SCREEN_WIDTH // 2,
    SCREEN_HEIGHT // 2
)

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                character.action()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        character.move_left()

    if keys[pygame.K_RIGHT]:
        character.move_right()

    if keys[pygame.K_UP]:
        character.move_up()

    if keys[pygame.K_DOWN]:
        character.move_down()

    character.update(
        SCREEN_WIDTH,
        SCREEN_HEIGHT
    )

    screen.fill((30, 30, 30))

    character.draw(screen)

    font = pygame.font.Font(None, 32)

    text = font.render(
        "Arrow keys = Move | SPACE = Action",
        True,
        (255, 255, 255)
    )

    screen.blit(
        text,
        (20, 20)
    )

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
