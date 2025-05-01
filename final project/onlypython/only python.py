import pygame
import random
import math
import time
import os

# ---------------- Record Persistence Functions ----------------

def load_records():
    records = []
    if os.path.exists("records.txt"):
        try:
            with open("records.txt", "r") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) == 2:
                        name, score_str = parts
                        try:
                            score_val = int(score_str)
                            records.append((name, score_val))
                        except:
                            pass
        except:
            pass
    records.sort(key=lambda x: x[1], reverse=True)
    return records

def save_records(records):
    records.sort(key=lambda x: x[1], reverse=True)
    with open("records.txt", "w") as f:
        for rec in records[:3]:
            f.write(f"{rec[0]},{rec[1]}\n")

def get_player_name():
    input_name = ""
    active = True
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    input_name = input_name[:-1]
                else:
                    input_name += event.unicode
        # Draw prompt screen
        screen.blit(mainbg, (0, 0))
        prompt = "Enter your name: " + input_name
        prompt_surface = pygame.font.Font(None, 80).render(prompt, True, WHITE)
        prompt_rect = prompt_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(prompt_surface, prompt_rect)
        pygame.display.flip()
        clock.tick(60)
    return input_name

def records_menu():
    # Show the records menu screen.
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    return
        screen.blit(mainbg, (0, 0))
        title_surface = title_font.render("Top Records", True, WHITE)
        title_rect = title_surface.get_rect(center=(WIDTH//2, 100))
        screen.blit(title_surface, title_rect)
        # Use different font sizes for 1st, 2nd, and 3rd
        if len(records_list) > 0:
            first = records_list[0]
            first_surface = pygame.font.Font(None, 100).render(f"1. {first[0]} - {first[1]}", True, WHITE)
            first_rect = first_surface.get_rect(center=(WIDTH//2, 250))
            screen.blit(first_surface, first_rect)
        if len(records_list) > 1:
            second = records_list[1]
            second_surface = pygame.font.Font(None, 80).render(f"2. {second[0]} - {second[1]}", True, WHITE)
            second_rect = second_surface.get_rect(center=(WIDTH//2, 350))
            screen.blit(second_surface, second_rect)
        if len(records_list) > 2:
            third = records_list[2]
            third_surface = pygame.font.Font(None, 60).render(f"3. {third[0]} - {third[1]}", True, WHITE)
            third_rect = third_surface.get_rect(center=(WIDTH//2, 450))
            screen.blit(third_surface, third_rect)
        # Back option at bottom.
        back_surface = pygame.font.Font(None, 80).render("Back", True, WHITE)
        back_rect = back_surface.get_rect(center=(WIDTH//2, HEIGHT - 100))
        screen.blit(back_surface, back_rect)
        pygame.display.flip()
        clock.tick(60)

# ---------------- Calculation Functions (replacing assembly routines) ----------------

wave_amplitude = 80.0
wave_frequency = 0.02
gravity = 0.4

def calculate_wave_offset(x: float) -> float:
    return math.sin(x * wave_frequency) * wave_amplitude

def apply_gravity(ball_velocity_y: float) -> float:
    return ball_velocity_y + gravity

def update_ball_x(ball_x: float, ball_velocity_x: float) -> float:
    return ball_x + ball_velocity_x

def update_ball_y(ball_y: float, ball_velocity_y: float) -> float:
    return ball_y + ball_velocity_y

# ---------------- Audio & Pygame Initialization ----------------

pygame.mixer.init()
collision_sound = pygame.mixer.Sound("collision.mp3")
pygame.mixer.music.load("main_theme.mp3")
pygame.mixer.music.play(-1)  # loop indefinitely

pygame.init()
WIDTH, HEIGHT = 1500, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Load backgrounds.
mainbg = pygame.image.load("mainbg.png")
mainbg = pygame.transform.scale(mainbg, (WIDTH, HEIGHT))
background1 = pygame.image.load("background1.jpg")
background1 = pygame.transform.scale(background1, (WIDTH, HEIGHT))
background2 = pygame.image.load("background2.jpg")
background2 = pygame.transform.scale(background2, (WIDTH, HEIGHT))
background3 = pygame.image.load("background3.jpg")
background3 = pygame.transform.scale(background3, (WIDTH, HEIGHT))
background4 = pygame.image.load("background4.jpg")
background4 = pygame.transform.scale(background4, (WIDTH, HEIGHT))

# Colors.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)

# Paddle and ball dimensions.
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 200
BALL_SIZE = 30

# Create the player paddle (left side) and right wall.
paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
wall = pygame.Rect(WIDTH - 10, 0, 10, HEIGHT)

# Create the AI goaler (used in rival mode only).
GOALER_WIDTH, GOALER_HEIGHT = 10, 200
goaler = pygame.Rect(WIDTH - 20, HEIGHT // 2 - GOALER_HEIGHT // 2, GOALER_WIDTH, GOALER_HEIGHT)
goaler_speed = 5

# Create the ball.
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
ball_velocity = [7, random.choice([-6, 6])]

# Score variables for regular modes.
score = 0
player_score = 0
goaler_score = 0
WIN_SCORE = 3

font = pygame.font.Font(None, 100)
clock = pygame.time.Clock()

# ---------------- Mode, Difficulty, & Countdown ----------------

# game_mode options: "normal", "wave", "Gravity", "rival", "journey", and "records"
game_mode = None      
# For non-Journey modes, use a difficulty selection.
difficulty = None     # Options: "Very Easy", "Easy", "Hard", "Very Hard", "Killer"
game_bg = None

game_started = False  # becomes True after countdown
countdown_start_time = None

# ---------------- Target Variables for Non-rival Modes ----------------

target_active = False
target_rect = None
target_points = None

# ---------------- Ball Rotation ----------------

ball_rotation_angle = 0

# ---------------- Difficulty Options (for non-Journey modes) ----------------

difficulty_options = ["Very Easy", "Easy", "Hard", "Very Hard", "Killer"]
selected_difficulty_index = 0

# ---------------- Journey Mode Variables ----------------

journey_modes = ["normal", "wave", "Gravity"]
journey_step_index = 0       # 0 = normal, 1 = wave, 2 = Gravity
journey_step_points = 0      # Points in current step (reset after 5)
journey_total_points = 0     # Cumulative record in Journey mode
journey_speed_multiplier = 1.0  # Increases every full cycle
record_entered = False       # To ensure record entry occurs only once

# ---------------- Global Records ----------------

records_list = load_records()  # List of tuples (name, score)

# ---------------- Utility Functions ----------------

def draw_capsule_paddle(surface, color, rect):
    radius = PADDLE_WIDTH // 2
    pygame.draw.rect(surface, color, (rect.x, rect.y + radius, rect.width, rect.height - 2 * radius))
    pygame.draw.circle(surface, color, (rect.centerx, rect.top + radius), radius)
    pygame.draw.circle(surface, color, (rect.centerx, rect.bottom - radius), radius)

def create_rotating_ball(size):
    ball_surface = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(ball_surface, WHITE, (size // 2, size // 2), size // 2)
    pygame.draw.line(ball_surface, BLACK, (0, 0), (size, size), 3)
    pygame.draw.line(ball_surface, BLACK, (size, 0), (0, size), 3)
    return ball_surface

ball_image = create_rotating_ball(BALL_SIZE)

def reset_ball(difficulty_level="Easy"):
    ball.x = WIDTH // 2 - BALL_SIZE // 2
    ball.y = HEIGHT // 2 - BALL_SIZE // 2
    speeds = {
        "Very Easy": (3, 2),
        "Easy": (5, 4),
        "Hard": (7, 6),
        "Very Hard": (9, 8),
        "Killer": (11, 10)
    }
    if difficulty_level in speeds:
        speed_x, speed_y = speeds[difficulty_level]
        ball_velocity[0] = random.choice([-speed_x, speed_x])
        ball_velocity[1] = random.choice([-speed_y, speed_y])
    else:
        ball_velocity[0] = random.choice([-7, 7])
        ball_velocity[1] = random.choice([-6, 6])
    global game_started, countdown_start_time, target_active
    game_started = False
    countdown_start_time = None
    target_active = False

def reset_ball_journey():
    ball.x = WIDTH // 2 - BALL_SIZE // 2
    ball.y = HEIGHT // 2 - BALL_SIZE // 2
    base_speed_x = 7
    base_speed_y = 6
    effective_speed_x = max(1, int(base_speed_x * journey_speed_multiplier))
    effective_speed_y = max(1, int(base_speed_y * journey_speed_multiplier))
    ball_velocity[0] = random.choice([-effective_speed_x, effective_speed_x])
    ball_velocity[1] = random.choice([-effective_speed_y, effective_speed_y])
    global game_started, countdown_start_time
    game_started = False
    countdown_start_time = None

def draw_countdown(value):
    count_text = font.render(str(value), True, WHITE)
    count_rect = count_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(count_text, count_rect)

def show_text_center(text, y_offset=0, font_size=100, color=WHITE):
    temp_font = pygame.font.Font(None, font_size)
    text_surface = temp_font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(text_surface, text_rect)

# ---------------- New Main Menu Using Arrow Navigation ----------------

menu_options = ["Normal", "Wave", "Gravity", "Rival", "Journey", "Records"]
selected_menu_index = 0
menu_font = pygame.font.Font(None, 80)
menu_font_selected = pygame.font.Font(None, 100)
menu_font_selected.set_bold(True)
title_font = pygame.font.Font(None, 120)

def draw_main_menu():
    screen.blit(mainbg, (0, 0))
    title_surface = title_font.render("Advance Pong", True, WHITE)
    title_rect = title_surface.get_rect(center=(WIDTH // 2, 150))
    screen.blit(title_surface, title_rect)
    for index, option in enumerate(menu_options):
        if index == selected_menu_index:
            option_surface = menu_font_selected.render(option, True, (176,224,230))
        else:
            option_surface = menu_font.render(option, True, (200, 200, 200))
        option_rect = option_surface.get_rect(center=(WIDTH // 2, 350 + index * 100))
        screen.blit(option_surface, option_rect)

def draw_difficulty_menu():
    screen.blit(mainbg, (0, 0))
    title_surface = title_font.render("Select Difficulty", True, WHITE)
    title_rect = title_surface.get_rect(center=(WIDTH // 2, 150))
    screen.blit(title_surface, title_rect)
    for i, option in enumerate(difficulty_options):
        if i == selected_difficulty_index:
            option_surface = menu_font_selected.render(option, True, (176,224,230))
        else:
            option_surface = menu_font.render(option, True, (200, 200, 200))
        option_rect = option_surface.get_rect(center=(WIDTH // 2, 350 + i * 100))
        screen.blit(option_surface, option_rect)

# ---------------- Main Game Loop ----------------

record_entered = False  # For Journey mode record entry

running = True
game_over = False
target_win = False

counter = 0
start_time = time.perf_counter()

while running:
    counter += 1
    # ----- Main Menu State -----
    if game_mode is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_menu_index = (selected_menu_index - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_menu_index = (selected_menu_index + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_menu_index == 0:
                        game_mode = "normal"
                        pygame.mixer.music.stop()
                    elif selected_menu_index == 1:
                        game_mode = "wave"
                        pygame.mixer.music.stop()
                    elif selected_menu_index == 2:
                        game_mode = "Gravity"
                        pygame.mixer.music.stop()
                    elif selected_menu_index == 3:
                        game_mode = "rival"
                        pygame.mixer.music.stop()
                    elif selected_menu_index == 4:
                        game_mode = "journey"
                        difficulty = "Journey"  # Bypass difficulty selection.
                        journey_step_index = 0
                        journey_step_points = 0
                        journey_total_points = 0
                        journey_speed_multiplier = 1.0
                        record_entered = False
                        reset_ball_journey()
                        pygame.mixer.music.stop()
                    elif selected_menu_index == 5:
                        # Switch to Records menu.
                        game_mode = "records"
        draw_main_menu()
        pygame.display.flip()
        clock.tick(60)
        continue

    # ----- Records Menu State -----
    if game_mode == "records":
        records_menu()
        game_mode = None  # Return to main menu
        continue

    # ----- Difficulty Selection State (skipped for Journey mode) -----
    if difficulty is None and game_mode != "journey":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_difficulty_index = (selected_difficulty_index - 1) % len(difficulty_options)
                elif event.key == pygame.K_DOWN:
                    selected_difficulty_index = (selected_difficulty_index + 1) % len(difficulty_options)
                elif event.key == pygame.K_RETURN:
                    difficulty = difficulty_options[selected_difficulty_index]
                    reset_ball(difficulty)
        draw_difficulty_menu()
        pygame.display.flip()
        clock.tick(60)
        continue

    # ----- Game Running State -----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # In Journey mode, pressing ESC ends the game.
            if game_mode == "journey" and event.key == pygame.K_ESCAPE:
                game_over = True
            if game_over:
                if event.key == pygame.K_r:
                    game_over = False
                    target_win = False
                    if game_mode == "rival":
                        player_score = 0
                        goaler_score = 0
                    elif game_mode == "journey":
                        journey_step_index = 0
                        journey_step_points = 0
                        journey_total_points = 0
                        journey_speed_multiplier = 1.0
                        record_entered = False
                        reset_ball_journey()
                    else:
                        score = 0
                    if game_mode != "journey":
                        reset_ball(difficulty)
                elif event.key == pygame.K_m:
                    game_over = False
                    target_win = False
                    game_mode = None
                    difficulty = None   # Reset difficulty so that it can be chosen again
                    score = 0
                    player_score = 0
                    goaler_score = 0
                    reset_ball("Easy")
                    pygame.mixer.music.play(-1)
    # Set Game Background.
    if game_mode == "normal":
        game_bg = background1
    elif game_mode == "wave":
        game_bg = background2
    elif game_mode == "Gravity":
        game_bg = background3
    elif game_mode == "rival":
        game_bg = background4
    elif game_mode == "journey":
        game_bg = background1  # Fixed background in Journey mode

    # ----- Countdown Before Game Starts -----
    if not game_started:
        if countdown_start_time is None:
            countdown_start_time = pygame.time.get_ticks()
        elapsed = (pygame.time.get_ticks() - countdown_start_time) / 1000
        countdown_value = 3 - int(elapsed)
        screen.blit(game_bg, (0, 0))
        draw_capsule_paddle(screen, WHITE, paddle)
        if game_mode == "rival":
            pygame.draw.rect(screen, WHITE, goaler)
        else:
            pygame.draw.rect(screen, WHITE, wall)
        if countdown_value > 0:
            draw_countdown(countdown_value)
            pygame.display.flip()
            clock.tick(60)
            continue
        else:
            game_started = True

    # ----- Target Activation for Non-rival Modes (ignored in Journey mode) -----
    if game_mode not in ["rival", "journey"] and score >= 10 and not target_active:
        target_active = True
        target_center = (random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100))
        target_size = 60
        target_points = [
            (target_center[0], target_center[1] - target_size // 2),
            (target_center[0] + target_size // 2, target_center[1]),
            (target_center[0], target_center[1] + target_size // 2),
            (target_center[0] - target_size // 2, target_center[1])
        ]
        target_rect = pygame.Rect(target_center[0] - target_size // 2,
                                  target_center[1] - target_size // 2,
                                  target_size, target_size)
    
    # ----- Loss Condition: Ball crosses x = 0 (for all non-rival modes) -----
    if game_mode not in ["rival"] and ball.left <= 0:
        game_over = True

    # ----- Journey Mode Record Entry -----
    if game_mode == "journey" and game_over and not record_entered:
        qualifies = False
        if len(records_list) < 3:
            qualifies = True
        else:
            lowest_score = records_list[-1][1]
            if journey_total_points > lowest_score:
                qualifies = True
        if qualifies:
            player_name = get_player_name()
            records_list.append((player_name, journey_total_points))
            records_list.sort(key=lambda x: x[1], reverse=True)
            records_list = records_list[:3]
            save_records(records_list)
        record_entered = True

    # ----- Game Over Screen -----
    if game_over:
        screen.blit(game_bg, (0, 0))
        if game_mode == "rival":
            if player_score > goaler_score:
                result = "You Win!"
            elif player_score < goaler_score:
                result = "You Lose!"
            else:
                result = "Draw!"
            show_text_center("Game Over!", -150)
            show_text_center(f"Player: {player_score}   Goaler: {goaler_score}", -50)
            show_text_center(result, 50)
        elif game_mode == "journey":
            show_text_center("Game Over!", -150)
            show_text_center(f"Record: {journey_total_points}", -50)
        else:
            if target_win:
                show_text_center("You Win by Hitting the Target!", -100)
            else:
                show_text_center("Game Over!", -100)
                show_text_center(f"Score: {score}", 0)
        show_text_center("Press R to Restart", 150, font_size=80)
        show_text_center("Press M for Main Menu", 250, font_size=80)
        pygame.display.flip()
        clock.tick(60)
        continue

    # ----- Update Background -----
    screen.blit(game_bg, (0, 0))
    
    # ----- Update Ball Rotation -----
    ball_rotation_angle = (ball_rotation_angle + 5) % 360
    rotated_ball_image = pygame.transform.rotate(ball_image, ball_rotation_angle)
    ball_rect = rotated_ball_image.get_rect(center=ball.center)
    
    # ----- Player Paddle Movement -----
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and paddle.top > 0:
        paddle.y -= 7
    if keys[pygame.K_DOWN] and paddle.bottom < HEIGHT:
        paddle.y += 7
    if game_mode == "rival":
        if keys[pygame.K_h]:
            goaler_speed += 0.2
        if keys[pygame.K_l]:
            goaler_speed = max(1, goaler_speed - 0.2)
    
    # ----- Update Ball Movement -----
    if game_mode == "journey":
        current_underlying = journey_modes[journey_step_index]
        if current_underlying == "normal":
            ball.x = int(update_ball_x(ball.x, ball_velocity[0]))
            ball.y = int(update_ball_y(ball.y, ball_velocity[1]))
        elif current_underlying == "wave":
            ball.x = int(update_ball_x(ball.x, ball_velocity[0]))
            ball.y = int(update_ball_y(ball.y, ball_velocity[1]))
            wave_offset = calculate_wave_offset(ball.x)
            ball.y = int(ball.y + (wave_offset - calculate_wave_offset(ball.x - ball_velocity[0])))
        elif current_underlying == "Gravity":
            ball.x = int(update_ball_x(ball.x, ball_velocity[0]))
            ball.y = int(update_ball_y(ball.y, ball_velocity[1]))
            ball_velocity[1] = apply_gravity(ball_velocity[1])
    elif game_mode in ("normal", "rival"):
        ball.x = int(update_ball_x(ball.x, ball_velocity[0]))
        ball.y = int(update_ball_y(ball.y, ball_velocity[1]))
    elif game_mode == "wave":
        ball.x = int(update_ball_x(ball.x, ball_velocity[0]))
        ball.y = int(update_ball_y(ball.y, ball_velocity[1]))
        wave_offset = calculate_wave_offset(ball.x)
        ball.y = int(ball.y + (wave_offset - calculate_wave_offset(ball.x - ball_velocity[0])))
    elif game_mode == "Gravity":
        ball.x = int(update_ball_x(ball.x, ball_velocity[0]))
        ball.y = int(update_ball_y(ball.y, ball_velocity[1]))
        ball_velocity[1] = apply_gravity(ball_velocity[1])
    
    # ----- Ball Collision with Top/Bottom -----
    if ball.top < 0:
        ball.top = 0
        ball_velocity[1] = -ball_velocity[1]
        collision_sound.play()
    if ball.bottom > HEIGHT:
        ball.bottom = HEIGHT
        ball_velocity[1] = -ball_velocity[1]
        collision_sound.play()
    
    # ----- Ball Collision with Paddle -----
    if ball.colliderect(paddle):
        relative_intersect = (paddle.centery - ball.centery) / (PADDLE_HEIGHT / 2)
        ball_velocity[1] = -relative_intersect * 10
        ball_velocity[0] = -ball_velocity[0]
        ball.x += 17
        collision_sound.play()
        if game_mode == "journey":
            journey_step_points += 1
            journey_total_points += 1
            if journey_step_points >= 3:
                journey_step_points = 0
                journey_step_index = (journey_step_index + 1) % 3
                if journey_step_index == 0:
                    journey_speed_multiplier += 0.2
        else:
            if game_mode != "rival" and not target_active:
                score += 1
            elif game_mode == "rival":
                score += 1
    
    # ----- Right-Side Collisions -----
    if game_mode in ("normal", "wave", "Gravity") or game_mode == "journey":
        if ball.colliderect(wall):
            ball_velocity[0] = -ball_velocity[0]
            collision_sound.play()
    elif game_mode == "rival":
        if ball.centery > goaler.centery:
            goaler.y += int(goaler_speed)
        elif ball.centery < goaler.centery:
            goaler.y -= int(goaler_speed)
        if goaler.top < 0:
            goaler.top = 0
        if goaler.bottom > HEIGHT:
            goaler.bottom = HEIGHT
        if ball.colliderect(goaler):
            ball_velocity[0] = -abs(ball_velocity[0])
            ball.x = goaler.x - ball.width
            collision_sound.play()
        if ball.right < 0:
            goaler_score += 1
            if goaler_score < WIN_SCORE:
                reset_ball(difficulty)
            else:
                game_over = True
        elif ball.left > WIDTH:
            player_score += 1
            if player_score < WIN_SCORE:
                reset_ball(difficulty)
            else:
                game_over = True
        if player_score >= WIN_SCORE or goaler_score >= WIN_SCORE:
            game_over = True
    
    # ----- Draw Game Objects -----
    draw_capsule_paddle(screen, WHITE, paddle)
    if game_mode == "rival":
        pygame.draw.rect(screen, WHITE, goaler)
    else:
        pygame.draw.rect(screen, WHITE, wall)
    screen.blit(rotated_ball_image, ball_rect)
    
    # ----- Draw Target (if active) -----
    if game_mode not in ["rival", "journey"] and target_active and target_rect:
        pygame.draw.polygon(screen, RED, target_points)
        if paddle.colliderect(target_rect) or ball.colliderect(target_rect):
            target_win = True
            game_over = True

    # ----- Draw Scoreboard at Top Center -----
    if game_mode == "rival":
        score_str = f"Player: {player_score}   Goaler: {goaler_score}"
    elif game_mode == "journey":
        current_mode_display = journey_modes[journey_step_index].capitalize()
        score_str = f"Record: {journey_total_points}   Mode: {current_mode_display}"
    else:
        score_str = str(score)
    score_text = font.render(score_str, True, WHITE)
    score_rect = score_text.get_rect(midtop=(WIDTH // 2, 20))
    screen.blit(score_text, score_rect)
    
    pygame.display.flip()
    clock.tick(60)

end_time = time.perf_counter()
elapsed_time = end_time - start_time
average_frame_time = elapsed_time / counter
print(f"average: {average_frame_time} seconds for each frame")

pygame.quit()
