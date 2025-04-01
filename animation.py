import pygame
import sys

# Initialize Pygame
pygame.init()

# Window dimensions and FPS settings
WIDTH, HEIGHT = 600, 600
FPS = 60

# Define Colors
WHITE = (255, 255, 255)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up display and clock for frame rate control
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Physics Simulation")
clock = pygame.time.Clock()

# Border thickness and fan base area (drawn inside the border at the bottom)
BORDER = 30
FAN_BASE_HEIGHT = 120
fan_base_rect = pygame.Rect(BORDER, HEIGHT - BORDER - FAN_BASE_HEIGHT, WIDTH - 2 * BORDER, FAN_BASE_HEIGHT)

# Define circles with positions, velocities, radii, masses, and colors.
circles = [
    {"pos": [150, 550], "vel": [0, 0], "radius": 20, "mass": 0.04, "color": RED},
    {"pos": [300, 540], "vel": [0, 0], "radius": 30, "mass": 0.2,  "color": GREEN},
    {"pos": [450, 530], "vel": [0, 0], "radius": 40, "mass": 0.05, "color": BLUE}
]

# Wind schedule: wind force increases from 0 to 80 then decreases back to 0 in steps of 10.
wind_schedule = [0, 10, 20, 30, 40, 50, 60, 70, 80, 70, 60, 50, 40, 30, 20, 10, 0]
wind_index = 0  # Current index in the wind schedule
current_wind = wind_schedule[wind_index]
wind_timer = 0  # Timer (in seconds) to track when to update the wind force

running = True
while running:
    dt = clock.tick(FPS) / 1000.0  # Delta time in seconds for smooth frame-rate independent updates

    # Handle events (e.g., window close)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update wind force every 2 seconds
    wind_timer += dt
    if wind_timer >= 2.0:
        wind_timer -= 2.0
        wind_index += 1
        if wind_index < len(wind_schedule):
            current_wind = wind_schedule[wind_index]
        else:
            running = False  # End simulation when wind schedule is complete

    # Update physics for each circle: 
    # Acceleration due to wind is computed using a = F/m.
    for circle in circles:
        mass = circle["mass"]
        # Calculate horizontal acceleration based on current wind force and circle's mass.
        acceleration = current_wind / mass  # F = m * a => a = F / m
        circle["vel"][0] += acceleration * dt  # Update horizontal velocity
        circle["pos"][0] += circle["vel"][0] * dt  # Update horizontal position
        # Vertical position remains constant since the wind force is horizontal.

    # Drawing section:
    screen.fill(WHITE)  # Fill background with white

    # Draw fan base area (light gray rectangle at the bottom, within the border)
    pygame.draw.rect(screen, LIGHT_GRAY, fan_base_rect)

    # Draw dark gray border around the window
    pygame.draw.rect(screen, DARK_GRAY, (0, 0, WIDTH, HEIGHT), BORDER)

    # Draw each circle in its current position
    for circle in circles:
        pygame.draw.circle(screen, circle["color"], (int(circle["pos"][0]), int(circle["pos"][1])), circle["radius"])

    # Optional: display the current wind force at the top for reference
    font = pygame.font.SysFont(None, 24)
    text = font.render(f"Wind Force: {current_wind}", True, (0, 0, 0))
    screen.blit(text, (50, 10))

    pygame.display.flip()

    # End simulation after the final wind update when wind force returns to 0
    if wind_index == len(wind_schedule) - 1 and wind_timer >= 2.0:
        running = False

pygame.quit()
sys.exit()
