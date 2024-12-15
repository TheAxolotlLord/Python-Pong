import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
BALL_SIZE = 20  # Side length of the square ball
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
WHITE = (255, 255, 255)
FPS = 60

# Get the screen dimensions for full screen
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h

# Set up the display in full screen mode
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Pong")

# Ball class (now using a square)
class Ball:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.speed_x = 9
        self.speed_y = 9
        self.size = BALL_SIZE

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        # Bounce off top and bottom
        if self.y <= 0 or self.y + self.size >= HEIGHT:
            self.speed_y = -self.speed_y

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.speed_x = -self.speed_x

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.size, self.size))

# Paddle class
class Paddle:
    def __init__(self, x):
        self.x = x
        self.y = HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.speed = 10

    def move_up(self):
        if self.y > 0:
            self.y -= self.speed

    def move_down(self):
        if self.y + PADDLE_HEIGHT < HEIGHT:
            self.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT))

# Function to draw the close "X" button
def draw_close_button():
    # Set the size of the "X"
    button_size = 40
    x_pos = WIDTH - button_size - 10  # 10 pixels from the right edge
    y_pos = 10  # 10 pixels from the top

    # Draw the "X"
    pygame.draw.line(screen, WHITE, (x_pos, y_pos), (x_pos + button_size, y_pos + button_size), 5)
    pygame.draw.line(screen, WHITE, (x_pos, y_pos + button_size), (x_pos + button_size, y_pos), 5)

    return pygame.Rect(x_pos, y_pos, button_size, button_size)

# Main function
def main():
    clock = pygame.time.Clock()

    # Create the ball and paddles
    ball = Ball()
    left_paddle = Paddle(50)
    right_paddle = Paddle(WIDTH - 50 - PADDLE_WIDTH)

    score_left = 0
    score_right = 0

    # Load a custom font or use the default system font
    try:
        font = pygame.font.Font("Lexend-Bold.tff", 36) 
    except FileNotFoundError:
        font = pygame.font.Font(None, 36)  # Fallback to the system default font if custom font not found

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Move ball and paddles
        ball.move()

        # Left paddle controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            left_paddle.move_up()
        if keys[pygame.K_s]:
            left_paddle.move_down()

        # Right paddle controls
        if keys[pygame.K_UP]:
            right_paddle.move_up()
        if keys[pygame.K_DOWN]:
            right_paddle.move_down()

        # Ball collision with paddles
        if ball.x <= left_paddle.x + PADDLE_WIDTH and left_paddle.y <= ball.y <= left_paddle.y + PADDLE_HEIGHT:
            ball.speed_x = -ball.speed_x

        if ball.x + ball.size >= right_paddle.x and right_paddle.y <= ball.y <= right_paddle.y + PADDLE_HEIGHT:
            ball.speed_x = -ball.speed_x

        # Score update
        if ball.x <= 0:
            score_right += 1
            ball.reset()

        if ball.x + ball.size >= WIDTH:
            score_left += 1
            ball.reset()

        # Fill the screen with black
        screen.fill((0, 0, 0))

        # Draw paddles, ball, and scores
        left_paddle.draw(screen)
        right_paddle.draw(screen)
        ball.draw(screen)

        # Draw the close button
        close_button = draw_close_button()

        # Display the scores with custom font
        score_text = font.render(f"{score_left} - {score_right}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

        # Check for mouse click on the close button
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if close_button.collidepoint(mouse_x, mouse_y):
                pygame.quit()
                sys.exit()

        # Update the screen
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

if __name__ == "__main__":
    main()
