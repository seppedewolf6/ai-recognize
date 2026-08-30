import pygame


class Character:

    def __init__(self, x, y):

        self.start_x = x
        self.start_y = y

        self.x = x
        self.y = y

        self.width = 40
        self.height = 60

        self.speed = 5

    def move_left(self):
        self.x -= self.speed

    def move_right(self):
        self.x += self.speed

    def move_up(self):
        self.y -= self.speed

    def move_down(self):
        self.y += self.speed

    def action(self, blocks):

        character_rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

        # Zoek een blok waar het karakter de blok raakt en verwijder het
        for block in blocks:

            if character_rect.colliderect(block):
                blocks.remove(block)

                print("Blok gebroken!")

                return True

        return False

    def reset(self):

        self.x = self.start_x
        self.y = self.start_y

    def update(self, screen_width, screen_height):

        self.x = max(
            0,
            min(
                self.x,
                screen_width - self.width
            )
        )

        self.y = max(
            0,
            min(
                self.y,
                screen_height - self.height
            )
        )

    def draw(self, screen):

        # Hoofd
        head_radius = 12

        head_x = int(self.x + self.width / 2)
        head_y = int(self.y + 12)

        pygame.draw.circle(
            screen,
            (255, 200, 150),
            (head_x, head_y),
            head_radius
        )

        # Lichaam
        pygame.draw.rect(
            screen,
            (50, 100, 200),
            (
                self.x + 10,
                self.y + 25,
                20,
                25
            )
        )

        # Benen
        pygame.draw.line(
            screen,
            (0, 0, 0),
            (self.x + 15, self.y + 50),
            (self.x + 10, self.y + 60),
            4
        )

        pygame.draw.line(
            screen,
            (0, 0, 0),
            (self.x + 25, self.y + 50),
            (self.x + 30, self.y + 60),
            4
        )

        # Armen
        pygame.draw.line(
            screen,
            (0, 0, 0),
            (self.x + 10, self.y + 30),
            (self.x, self.y + 40),
            4
        )

        pygame.draw.line(
            screen,
            (0, 0, 0),
            (self.x + 30, self.y + 30),
            (self.x + 40, self.y + 40),
            4
        )
