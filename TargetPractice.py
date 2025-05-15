import math
import random
import time
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")

TARGET_INTERVAL = 500
NEW_TARGET_EVENT = pygame.USEREVENT
TARGET_MARGIN = 30

BACKGROUND_COLOR = (10, 30, 50)
MAX_LIVES = 3
HEADER_HEIGHT = 50

FONT = pygame.font.SysFont("comicsans", 24)


class AimTarget:
    MAX_RADIUS = 30
    GROWTH_SPEED = 0.2
    PRIMARY_COLOR = "red"
    SECONDARY_COLOR = "white"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 0
        self.growing = True

    def update(self):
        if self.radius + self.GROWTH_SPEED >= self.MAX_RADIUS:
            self.growing = False

        if self.growing:
            self.radius += self.GROWTH_SPEED
        else:
            self.radius -= self.GROWTH_SPEED

    def draw(self, screen):
        pygame.draw.circle(screen, self.PRIMARY_COLOR, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, self.SECONDARY_COLOR, (self.x, self.y), int(self.radius * 0.8))
        pygame.draw.circle(screen, self.PRIMARY_COLOR, (self.x, self.y), int(self.radius * 0.6))
        pygame.draw.circle(screen, self.SECONDARY_COLOR, (self.x, self.y), int(self.radius * 0.4))

    def is_hit(self, x, y):
        distance = math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
        return distance <= self.radius


def draw_screen(screen, targets):
    screen.fill(BACKGROUND_COLOR)

    for target in targets:
        target.draw(screen)


def format_time(seconds):
    milliseconds = int((seconds * 1000) % 1000) // 100
    seconds = int(seconds % 60)
    minutes = int(seconds // 60)

    return f"{minutes:02d}:{seconds:02d}.{milliseconds}"


def draw_header(screen, elapsed_time, hits, misses):
    pygame.draw.rect(screen, "grey", (0, 0, WIDTH, HEADER_HEIGHT))
    time_text = FONT.render(f"Time: {format_time(elapsed_time)}", True, "black")
    speed_text = FONT.render(f"Speed: {round(hits / elapsed_time, 1)} t/s", True, "black")
    hits_text = FONT.render(f"Hits: {hits}", True, "black")
    lives_text = FONT.render(f"Lives: {MAX_LIVES - misses}", True, "black")

    screen.blit(time_text, (10, 10))
    screen.blit(speed_text, (200, 10))
    screen.blit(hits_text, (400, 10))
    screen.blit(lives_text, (600, 10))


def end_game(screen, elapsed_time, hits, total_clicks):
    screen.fill(BACKGROUND_COLOR)
    time_text = FONT.render(f"Time: {format_time(elapsed_time)}", True, "white")
    speed_text = FONT.render(f"Speed: {round(hits / elapsed_time, 1)} t/s", True, "white")
    hits_text = FONT.render(f"Hits: {hits}", True, "white")
    accuracy = round(hits / total_clicks * 100, 1) if total_clicks > 0 else 0
    accuracy_text = FONT.render(f"Accuracy: {accuracy}%", True, "white")
    replay_text = FONT.render("Press SPACE or click to play again", True, "white")

    screen.blit(time_text, (center_text(time_text), 100))
    screen.blit(speed_text, (center_text(speed_text), 180))
    screen.blit(hits_text, (center_text(hits_text), 260))
    screen.blit(accuracy_text, (center_text(accuracy_text), 340))
    bubble_color = (255, 255, 255)
    text_color = (10, 30, 50)
    bubble_text = "Press SPACE or click to play again"
    replay_text = FONT.render(bubble_text, True, text_color)

    bubble_width = replay_text.get_width() + 40
    bubble_height = replay_text.get_height() + 20
    bubble_x = WIDTH // 2 - bubble_width // 2
    bubble_y = 430

    pygame.draw.rect(screen, bubble_color, (bubble_x, bubble_y, bubble_width, bubble_height), border_radius=12)

    screen.blit(replay_text, (WIDTH // 2 - replay_text.get_width() // 2, bubble_y + 10))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

    main()  



def center_text(text_surface):
    return WIDTH / 2 - text_surface.get_width() / 2


def main():
    running = True
    targets = []
    clock = pygame.time.Clock()

    hits = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    pygame.time.set_timer(NEW_TARGET_EVENT, TARGET_INTERVAL)

    while running:
        clock.tick(60)
        click_detected = False
        mouse_x, mouse_y = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == NEW_TARGET_EVENT:
                x = random.randint(TARGET_MARGIN, WIDTH - TARGET_MARGIN)
                y = random.randint(TARGET_MARGIN + HEADER_HEIGHT, HEIGHT - TARGET_MARGIN)
                targets.append(AimTarget(x, y))

            if event.type == pygame.MOUSEBUTTONDOWN:
                click_detected = True
                clicks += 1

        for target in targets:
            target.update()
            if target.radius <= 0:
                targets.remove(target)
                misses += 1

            if click_detected and target.is_hit(mouse_x, mouse_y):
                targets.remove(target)
                hits += 1

        if misses >= MAX_LIVES:
            end_game(SCREEN, elapsed_time, hits, clicks)

        draw_screen(SCREEN, targets)
        draw_header(SCREEN, elapsed_time, hits, misses)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
