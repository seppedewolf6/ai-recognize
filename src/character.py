import pygame


class Character:

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.width = 40
        self.height = 60

        self.speed = 5

        # Voor de actie
        self.action_timer = 0

    def move_left(self):
        self.x -= self.speed

    def move_right(self):
        self.x += self.speed

    def move_up(self):
        self.y -= self.speed

    def move_down(self):
        self.y += self.speed

    def action(self):
        self.action_timer = 15
        print("ACTION!")

    def update(self, screen_width, screen_height):
        # Zorg dat het karakter binnen het scherm blijft

        self.x = max(
            0,
            min(self.x, screen_width - self.width)
        )

        self.y = max(
            0,
            min(self.y, screen_height - self.height)
        )

        # Action timer aftellen
        if self.action_timer > 0:
            self.action_timer -= 1

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

        # Laat het karakter tijdens ACTION een effect zien
        if self.action_timer > 0:

            pygame.draw.circle(
                screen,
                (255, 200, 0),
                (head_x, head_y),
                25,
                3
            )