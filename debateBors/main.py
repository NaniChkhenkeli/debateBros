import pygame
import sys
import math
import random
import time
import os
from pygame import gfxdraw
import pyperclip
from debateBors.ai import *

pygame.init()
pygame.font.init()  # you have to call this at the start,
# if you want to use this module.
sideFont = pygame.font.SysFont('Comic Sans MS', 30)
scoresFont = pygame.font.SysFont('Comic Sans MS', 20)
topicFont = pygame.font.SysFont('Aria', 30)
font_main = pygame.font.SysFont('Courier New', 18)
font_status = pygame.font.SysFont('Courier New', 24, bold=True)
title_font = pygame.font.Font(None, 72)
button_font = pygame.font.Font(None, 42)
subtitle_font = pygame.font.Font(None, 36)

# Set up display
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
screen = pygame.display.set_mode((screen_width, screen_height - 100))
pygame.display.set_caption("DebateBros")
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
DARK_BG = (10, 12, 18)
NEON_BLUE = (0, 200, 255)
NEON_GREEN = (50, 255, 150)
NEON_PURPLE = (180, 70, 255)
TEXT_WHITE = (240, 240, 255)
GLOW_EFFECT = (100, 255, 255, 50)
BLACK = (0, 0, 0)
DARK_BLUE = (10, 20, 40)
GOLD = (255, 215, 0)
CRIMSON = (220, 20, 60)
EMERALD = (80, 200, 120)
LIGHT_BLUE = (100, 200, 255)

# Load fonts

awaypixel = 300
text_location = 100
chatHeight = 300

proLogicText = 0
proEvidenceText = 0
proPersuasiveText = 0
proRelevanceText = 0
proScore = 0
proFeedback = ""

conLogicText = 0
conEvidenceText = 0
conPersuasiveText = 0
conRelevanceText = 0
conScore = 0
conFeedback = ""

IMAGE_FOLDER = r"images"
IMAGE_FORMAT = "PNG"
IMAGE_FORMAT2 = "png"
NUM_IMAGES = 7
ATT_IMAGES = 4
FPS = 10
# WIDTH, HEIGHT = 300, 300

# debateBors.display.set_caption("GIF Animation Loop")
characterPath = os.path.join(IMAGE_FOLDER, "character1")
characterPath2 = os.path.join(IMAGE_FOLDER, "character2")
characterPath3 = os.path.join(IMAGE_FOLDER, "attack")

image_files = [os.path.join(characterPath, f"{i}.{IMAGE_FORMAT}") for i in range(1, NUM_IMAGES + 1)]
image_files2 = [os.path.join(characterPath2, f"{i}.{IMAGE_FORMAT2}") for i in range(1, NUM_IMAGES + 1)]
image_files3 = [os.path.join(characterPath3, f"{i}.{IMAGE_FORMAT2}") for i in range(1, ATT_IMAGES + 1)]

images = [pygame.image.load(img) for img in image_files]
images2 = [pygame.image.load(img) for img in image_files2]
images3 = [pygame.image.load(img) for img in image_files3]

images = [pygame.transform.scale(img, (200, 200)) for img in images]
images2 = [pygame.transform.scale(img, (200, 200)) for img in images2]
images3 = [pygame.transform.scale(img, (250, 200)) for img in images3]

images2 = [pygame.transform.flip(img, True, False) for img in images2]

tb_image = pygame.image.load(os.path.join(IMAGE_FOLDER, "table/tb.png"))
robo_image = pygame.image.load(os.path.join(IMAGE_FOLDER, "Sprite-0002.png"))
tb_image2 = pygame.transform.flip(tb_image, True, False)
tb_width = 300
tb_height = 300
tb_image = pygame.transform.scale(tb_image, (tb_width, tb_height))
robo_image = pygame.transform.scale(robo_image, (100, 100))
tb_image2 = pygame.transform.scale(tb_image2, (tb_width, tb_height))
center_position_between_reds = ((awaypixel) + (screen_width - awaypixel)) // 2

table_offset_x = center_position_between_reds
table_offset_y = 400

clock = pygame.time.Clock()
left_position = awaypixel
right_position = screen_width - awaypixel


background_image = pygame.image.load("images/background.png")
bg_width = right_position - left_position
bg_height = screen_height
background_image = pygame.transform.scale(background_image, (bg_width, bg_height))

running = True
TEXTS = {
    "window_title": "NEO-BOT v2.0",
    "initial_greeting": " >> System initialized. How can I assist?",
    "processing": ">> Processing your request...",
    "requirements": ">Not enough words to convince anyone",
    "status_prefix": "STATUS: ",
    "input_prompt": "$ ",
    "responses": [
        ">> Request acknowledged.",
        ">> Analyzing your input...",
        ">> Command received.",
        ">> Working on it...",
        ">> One moment please..."
    ]
}

chat_history = {
    "conversation": [],
    "settings": {
        "max_history": 100,
        "save_file": "chat_history.json"
    }
}

console_chat_history = []


# topicStr = ""


class CyberBot:
    def __init__(self):
        self.state = "idle"
        self.animation_time = 0
        self.eye_glow = 1.0
        self.mouth_open = 0.0
        self.bg_color = (10, 15, 20)
        self.primary = (0, 200, 255)
        self.secondary = (50, 255, 150)
        self.text_color = (240, 240, 240)

    def update(self):
        self.animation_time += 0.05
        if self.state == "talking":
            self.mouth_open = 0.5 + 0.3 * math.sin(self.animation_time * 5)
        else:
            self.mouth_open = 0.0

    def draw(self, surface, position):
        width =robo_image.get_width()
        screen.blit(robo_image, (screen_width//2-width//2, 150))

        # Define bot position
        # bot_x, bot_y = position
        # debateBors.draw.rect(surface, self.primary,
        #                  (bot_x-40, bot_y, 100, 80),
        #                  border_radius=15)
        # # body
        # debateBors.draw.rect(surface, self.secondary,
        #                  (bot_x-50, bot_y + 70, 120, 80),
        #                  border_radius=10)
        # # eyes
        # eye_offset = clock.get_time()
        # debateBors.draw.circle(surface, self.text_color,
        #                    (bot_x + 30 + eye_offset, bot_y + 40), 10)
        # debateBors.draw.circle(surface, self.text_color,
        #                    (bot_x - 10 - eye_offset, bot_y + 40), 10)
        # # antenna
        # debateBors.draw.line(surface, self.primary,
        #                  (bot_x , bot_y),
        #                  (bot_x , bot_y - 30), 3)
        # debateBors.draw.circle(surface, self.secondary,
        #                    (bot_x , bot_y - 40), 10)
        # bot_x, bot_y = position  # Use the passed position for bot_x and bot_y
        # head_rect = debateBors.Rect(bot_x - 60, bot_y - 75, 120, 150)
        # debateBors.draw.ellipse(surface, (40, 45, 60), head_rect)
        #
        # # Eyes
        # debateBors.draw.circle(surface, (255, 255, 255), (bot_x - 25, bot_y - 20), 10)
        # debateBors.draw.circle(surface, (255, 255, 255), (bot_x + 25, bot_y - 20), 10)
        #
        # # Mouth
        # mouth_rect = debateBors.Rect(bot_x - 25, bot_y + 30, 50, 10 + 10 * self.mouth_open)
        # debateBors.draw.ellipse(surface, (200, 50, 100), mouth_rect)


class ChatMessage:
    def __init__(self, text, is_user=False):
        self.text = text
        self.is_user = is_user
        self.time = time.time()
        self.alpha = 0
        self.lines = []
        self._wrap_text()
        self._save_to_history()
        self._print_to_console()

    def _wrap_text(self):
        max_width = 500
        words = self.text.split(' ')
        current_line = ''

        for word in words:
            test_line = current_line + word + ' '
            if font_main.size(test_line)[0] < max_width:
                current_line = test_line
            else:
                self.lines.append(current_line)
                current_line = word + ' '
        self.lines.append(current_line)

    def _save_to_history(self):
        if len(chat_history["conversation"]) >= chat_history["settings"]["max_history"]:
            chat_history["conversation"].pop(0)

        chat_history["conversation"].append({
            "text": self.text,
            "is_user": self.is_user,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })

    def _print_to_console(self):
        prefix = "USER: " if self.is_user else "BOT: "
        console_chat_history.append(prefix + self.text)
        print(prefix + self.text)  # Add this to see messages in console for debugging

    def draw(self, surface, x, y):
        self.alpha = min(self.alpha + 10, 255)
        bubble_color = NEON_PURPLE if self.is_user else (70, 80, 100)
        text_color = TEXT_WHITE

        total_height = 10
        for line in self.lines:
            text_width = font_main.size(line)[0]
            bubble_width = text_width + 30
            bubble_height = 30

            if self.is_user:
                # Position user messages on the right side
                bubble_x = x + 500 - bubble_width
            else:
                # Position bot messages on the left side
                bubble_x = x

            # Create a semitransparent surface for the chat bubble
            s = pygame.Surface((bubble_width, bubble_height), pygame.SRCALPHA)

            # Fill with semi-transparent background
            pygame.draw.rect(s, (*bubble_color[:3], self.alpha // 2),
                             (0, 0, bubble_width, bubble_height), border_radius=15)

            # Draw the border
            pygame.draw.rect(s, (*bubble_color[:3], self.alpha),
                             (0, 0, bubble_width, bubble_height), 2, border_radius=15)

            # Blit the bubble to the main surface
            surface.blit(s, (bubble_x, y + total_height))

            # Render and blit the text
            text_surface = font_main.render(line, True, text_color)
            text_surface.set_alpha(self.alpha)
            surface.blit(text_surface, (bubble_x + 15, y + 8 + total_height))

            total_height += bubble_height + 5

        return total_height


def save_chat_history():
    try:
        with open(chat_history["settings"]["save_file"], "w") as f:
            json.dump(chat_history, f, indent=2)
    except Exception as e:
        print(f"Error saving chat history: {e}")


def load_chat_history():
    try:
        with open(chat_history["settings"]["save_file"], "r") as f:
            data = json.load(f)
            chat_history.update(data)
            for msg in data["conversation"]:
                prefix = "USER: " if msg["is_user"] else "BOT: "
                console_chat_history.append(prefix + msg["text"])
    except FileNotFoundError:
        print("No existing chat history found")
    except Exception as e:
        print(f"Error loading chat history: {e}")


def print_full_chat_history():
    print("\n=== FULL CHAT HISTORY ===")
    for msg in console_chat_history:
        print(msg)


class StartScreen:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("start")

        self.bg_color = (10, 15, 20)
        self.primary = (0, 200, 255)
        self.secondary = (50, 255, 150)
        self.text_color = (240, 240, 240)
        self.input_bg = (30, 35, 40)

        self.title_font = pygame.font.SysFont('Arial', 60, bold=True)
        self.button_font = pygame.font.SysFont('Arial', 36, bold=True)
        self.input_font = pygame.font.SysFont('Arial', 28)

        self.rounds = ""
        self.topic = ""

        self.button_rect = pygame.Rect(self.width // 2 - 120, self.height // 2 + 150, 240, 60)
        self.topic_rect = pygame.Rect(self.width // 2 - 200, self.height // 2 - 100, 400, 50)
        self.rounds_rect = pygame.Rect(self.width // 2 - 200, self.height // 2, 400, 50)

        self.active_topic = False
        self.active_rounds = False

    def draw_rounded_rect(self, surface, rect, color, radius=10, border=0, border_color=None):
        rect = pygame.Rect(rect)
        if border:
            pygame.draw.rect(surface, border_color, rect, border, border_radius=radius)
        pygame.draw.rect(surface, color, rect.inflate(-border * 2, -border * 2), 0, border_radius=radius)

    def draw(self):
        self.screen.fill(self.bg_color)

        title = self.title_font.render("DebateBro", True, self.primary)
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 80))

        self.draw_rounded_rect(self.screen, self.topic_rect, self.input_bg, 10, 2, self.primary)
        topic_label = self.input_font.render("Discussion Topic:", True, self.text_color)
        self.screen.blit(topic_label, (self.topic_rect.x, self.topic_rect.y - 35))

        if not self.topic and not self.active_topic:
            placeholder = self.input_font.render("", True, (100, 100, 120))
            self.screen.blit(placeholder, (self.topic_rect.x + 15, self.topic_rect.y + 15))


        else:

            topic_text = self.input_font.render(self.topic, True, self.text_color)
            self.screen.blit(topic_text, (self.topic_rect.x + 15, self.topic_rect.y + 15))

        # Rounds inpu
        self.draw_rounded_rect(self.screen, self.rounds_rect, self.input_bg, 10, 2, self.primary)
        rounds_label = self.input_font.render("Number of Rounds (1-8):", True, self.text_color)
        self.screen.blit(rounds_label, (self.rounds_rect.x, self.rounds_rect.y - 35))

        if not self.rounds and not self.active_rounds:
            placeholder = self.input_font.render("", True, (100, 100, 120))

            self.screen.blit(placeholder, (self.rounds_rect.x + 15, self.rounds_rect.y + 15))
        else:
            rounds_text = self.input_font.render(str(self.rounds), True, self.text_color)
            self.screen.blit(rounds_text, (self.rounds_rect.x + 15, self.rounds_rect.y + 15))

        # START button
        button_ready = bool(self.topic and self.rounds)
        mouse_pos = pygame.mouse.get_pos()
        button_hover = self.button_rect.collidepoint(mouse_pos)

        button_color = self.secondary if button_ready else (50, 80, 60)
        border_color = (200, 255, 200) if (button_ready and button_hover) else (100, 100, 100)

        self.draw_rounded_rect(self.screen, self.button_rect, button_color, 15, 3, border_color)

        button_text = self.button_font.render("START", True, self.text_color if button_ready else (100, 100, 100))
        self.screen.blit(button_text, (self.button_rect.x + self.button_rect.width // 2 - button_text.get_width() // 2,
                                       self.button_rect.y + self.button_rect.height // 2 - button_text.get_height() // 2))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_rect.collidepoint(event.pos) and self.topic and self.rounds:
                        return self.topic, int(self.rounds)

                    elif self.topic_rect.collidepoint(event.pos):
                        self.active_topic = True
                        self.active_rounds = False

                    elif self.rounds_rect.collidepoint(event.pos):
                        self.active_rounds = True
                        self.active_topic = False
                    else:
                        self.active_topic = False
                        self.active_rounds = False

                if event.type == pygame.KEYDOWN:
                    if self.active_topic:
                        if event.key == pygame.K_RETURN:
                            self.active_topic = False
                        elif event.key == pygame.K_BACKSPACE:
                            self.topic = self.topic[:-1]
                        elif len(self.topic) < 30:
                            self.topic += event.unicode

                    elif self.active_rounds:
                        if event.key == pygame.K_RETURN:
                            self.active_rounds = False
                        elif event.key == pygame.K_BACKSPACE:
                            self.rounds = self.rounds[:-1] if self.rounds else ""
                        elif event.unicode.isdigit():
                            if len(self.rounds) < 1:
                                if 1 <= int(event.unicode) <= 8:
                                    self.rounds += event.unicode

            self.draw()
            pygame.time.Clock().tick(60)


class LoadingScreen:
    def __init__(self, topic, rounds, width, height):
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Debate - Loading")

        self.topic = topic
        self.rounds = rounds
        self.loading_progress = 0
        self.index = 0
        # Colors
        self.bg_color = (10, 15, 20)
        self.primary = (0, 200, 255)
        self.secondary = (50, 255, 150)
        self.text_color = (240, 240, 240)

        # Fonts
        self.title_font = pygame.font.SysFont('Arial', 48, bold=True)
        self.info_font = pygame.font.SysFont('Arial', 24)

        # Back button
        self.back_button = pygame.Rect(50, 50, 120, 50)

        # Loading bar
        self.loading_bar = pygame.Rect(self.width // 2 - 200, self.height - 150, 400, 20)

        # Simple bot icon
        self.bot_rect = pygame.Rect(self.width // 2 - 50, self.height // 2 - 100, 100, 150)

    def draw_bot(self,index):
        # head
        width = images3[index].get_width()
        screen.blit(images3[index], (center_position_between_reds-width//2 , screen_height//2))

    def draw(self):
        self.screen.fill(self.bg_color)

        title = self.title_font.render("DebateBro", True, self.primary)
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 80))

        # Back button
        pygame.draw.rect(self.screen, self.secondary, self.back_button, border_radius=5)
        back_text = self.info_font.render("BACK", True, self.bg_color)
        self.screen.blit(back_text, (self.back_button.x + self.back_button.width // 2 - back_text.get_width() // 2,
                                     self.back_button.y + self.back_button.height // 2 - back_text.get_height() // 2))

        self.index = (self.index + 1) % len(images3)
        self.draw_bot(self.index)

        # Loading bar
        pygame.draw.rect(self.screen, (50, 50, 60), self.loading_bar, border_radius=10)
        progress_width = int(self.loading_bar.width * (self.loading_progress / 100))
        progress_rect = pygame.Rect(self.loading_bar.x, self.loading_bar.y, progress_width, self.loading_bar.height)
        pygame.draw.rect(self.screen, self.secondary, progress_rect, border_radius=10)

        # Loading text
        loading_text = self.info_font.render(f"Loading... {self.loading_progress}%", True, self.text_color)
        self.screen.blit(loading_text, (self.width // 2 - loading_text.get_width() // 2, self.loading_bar.y - 30))
        clock.tick(10)
        pygame.display.flip()

    def update_loading(self):
        if self.loading_progress < 100:
            self.loading_progress += 1
            time.sleep(0.03)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.collidepoint(event.pos):
                        return

            self.update_loading()
            self.draw()
            pygame.time.Clock().tick(60)

            if self.loading_progress >= 100:
                time.sleep(0.5)
                return


try:
    button_hover_sound = pygame.mixer.Sound("button_hover.wav")
    button_click_sound = pygame.mixer.Sound("button_click.wav")
    victory_sound = pygame.mixer.Sound("victory_fanfare.wav")
except:
    # Create silent dummy sounds if files not found
    button_hover_sound = pygame.mixer.Sound(buffer=bytearray(44))
    button_click_sound = pygame.mixer.Sound(buffer=bytearray(44))
    victory_sound = pygame.mixer.Sound(buffer=bytearray(44))


class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 5)
        self.speed = random.uniform(1, 3)
        self.angle = random.uniform(0, math.pi * 2)
        self.lifetime = random.randint(30, 90)
        self.alpha = 255

    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.lifetime -= 1
        self.alpha = int(255 * (self.lifetime / 90))
        return self.lifetime > 0

    def draw(self, surface):
        color_with_alpha = (*self.color[:3], self.alpha)
        pygame.gfxdraw.filled_circle(
            surface,
            int(self.x),
            int(self.y),
            self.size,
            color_with_alpha
        )


class GlowButton:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.glow_alpha = 0
        self.glow_size = 0

    def draw(self, surface):
        # Draw glow effect
        if self.is_hovered:
            self.glow_alpha = min(100, self.glow_alpha + 10)
            self.glow_size = min(20, self.glow_size + 2)
        else:
            self.glow_alpha = max(0, self.glow_alpha - 5)
            self.glow_size = max(0, self.glow_size - 1)

        if self.glow_alpha > 0:
            glow_surf = pygame.Surface((self.rect.width + self.glow_size * 2,
                                        self.rect.height + self.glow_size * 2),
                                       pygame.SRCALPHA)
            pygame.draw.rect(
                glow_surf,
                (*self.hover_color[:3], self.glow_alpha),
                (self.glow_size, self.glow_size, self.rect.width, self.rect.height),
                border_radius=15
            )
            surface.blit(glow_surf, (self.rect.x - self.glow_size, self.rect.y - self.glow_size))

        # Draw button
        button_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(
            surface,
            button_color,
            self.rect,
            border_radius=10
        )

        # Draw border
        border_color = WHITE if self.is_hovered else (*WHITE[:3], 150)
        pygame.draw.rect(
            surface,
            border_color,
            self.rect,
            2,
            border_radius=10
        )

        # Draw text with shadow
        text_surface = button_font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)

        shadow_surface = button_font.render(self.text, True, (*BLACK[:3], 100))
        surface.blit(shadow_surface, (text_rect.x + 2, text_rect.y + 2))
        surface.blit(text_surface, text_rect)

    def check_hover(self, pos):
        was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(pos)
        if self.is_hovered and not was_hovered:
            button_hover_sound.play()

    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pos):
                button_click_sound.play()
                return True
        return False
def wrap_text(text, font, max_width):

    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        # Check the width of the current line + new word
        test_line = current_line + word + " "
        if font.size(test_line)[0] < max_width:
            current_line = test_line  # Add word to line
        else:
            lines.append(current_line.strip())  # Save the line
            current_line = word + " "  # Start new line

    lines.append(current_line.strip())  # Append last line
    return lines



def show_ending_screen(score,victory):
    # Play victory sound
    victory_sound.play()

    # Create particles
    particles = []
    for _ in range(100):
        particles.append(Particle(
            random.randint(0, screen_width),
            random.randint(0, screen_height),
            (random.randint(200, 255), random.randint(100, 200), random.randint(0, 100))
        ))

    # Create buttons
    exit_button = GlowButton(
        screen_width // 2 - 200, screen_height // 2 + 120,
        180, 60, "EXIT", CRIMSON, (255, 100, 100)
    )

    repeat_button = GlowButton(
        screen_width // 2 + 20, screen_height // 2 + 120,
        180, 60, "PLAY AGAIN", EMERALD, (100, 255, 150)
    )

    # Animation variables
    title_y = -100
    subtitle_y = screen_height + 50
    button_y_offset = 100
    animation_speed = 0.5
    stars = [(random.randint(0, screen_width), random.randint(0, screen_height),
              random.randint(1, 3), random.uniform(0.1, 0.5))
             for _ in range(100)]

    running = True
    clock = pygame.time.Clock()

    while running:
        dt = clock.tick(60) / 1000.0
        mouse_pos = pygame.mouse.get_pos()

        # Update animations
        if title_y < screen_height // 2 - 150:
            title_y += (screen_height // 2 - 150 - title_y) * animation_speed * dt * 10
        if subtitle_y > screen_height // 2 - 50:
            subtitle_y -= (subtitle_y - (screen_height // 2 - 50)) * animation_speed * dt * 10
        if button_y_offset > 0:
            button_y_offset -= button_y_offset * animation_speed * dt * 5

        # Update particles
        for particle in particles[:]:
            if not particle.update():
                particles.remove(particle)

        # Add new particles
        if random.random() < 0.3:
            particles.append(Particle(
                random.randint(0, screen_width),
                random.randint(0, screen_height),
                (random.randint(200, 255), random.randint(100, 200), random.randint(0, 100))
            ))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Check button clicks
            if exit_button.is_clicked(mouse_pos, event):
                pygame.quit()
                sys.exit()

            if repeat_button.is_clicked(mouse_pos, event):
                running = False
                return True  # Signal to restart the game

        # Update button hover states
        exit_button.check_hover(mouse_pos)
        repeat_button.check_hover(mouse_pos)

        # Update button positions with animation offset
        exit_button.rect.y = screen_height // 2 + 120 + button_y_offset
        repeat_button.rect.y = screen_height // 2 + 120 + button_y_offset

        # Drawing
        # Gradient background
        for y in range(screen_height):
            color = (
                int(DARK_BLUE[0] + (10 * y / screen_height)),
                int(DARK_BLUE[1] + (30 * y / screen_height)),
                int(DARK_BLUE[2] + (50 * y / screen_height))
            )
            pygame.draw.line(screen, color, (0, y), (screen_width, y))

        # Draw stars
        for x, y, size, brightness in stars:
            alpha = int(255 * brightness)
            color = (255, 255, 255, alpha)
            pygame.gfxdraw.filled_circle(screen, x, y, size, color)

        # Draw particles
        for particle in particles:
            particle.draw(screen)

        # Draw title
        title_surface = title_font.render(victory, True, GOLD)
        title_shadow = title_font.render(victory, True, (*BLACK[:3], 100))
        title_rect = title_surface.get_rect(center=(screen_width // 2, title_y))

        screen.blit(title_shadow, (title_rect.x + 3, title_rect.y + 3))
        screen.blit(title_surface, title_rect)

        # Draw subtitle
        subtitle_text = f"Final Score: {score}"
        subtitle_surface = subtitle_font.render(subtitle_text, True, LIGHT_BLUE)
        subtitle_shadow = subtitle_font.render(subtitle_text, True, (*BLACK[:3], 100))
        subtitle_rect = subtitle_surface.get_rect(center=(screen_width // 2, subtitle_y))

        screen.blit(subtitle_shadow, (subtitle_rect.x + 2, subtitle_rect.y + 2))
        screen.blit(subtitle_surface, subtitle_rect)

        exit_button.draw(screen)
        repeat_button.draw(screen)

        pygame.display.flip()
# Update the UI class to correctly handle score rendering
def copy_to_clipboard(text):
    try:
        if text.strip():
            pyperclip.copy(text)
            return True
        return False
    except Exception as e:
        print(f"Error copying to clipboard: {e}")
        return False
class UI:
    def __init__(self):
        pass

    def drawLines(self):
        pygame.draw.line(screen, RED, (awaypixel, 0), (awaypixel, screen_height))  # Left border
        pygame.draw.line(screen, RED, (screen_width - awaypixel, 0),
                         (screen_width - awaypixel, screen_height))  # Right border
        screen.blit(background_image, (left_position, 100))

    def renderPro(self, isPro):
        proText = sideFont.render('PRO', True, RED if isPro else WHITE)
        screen.blit(proText, (text_location, text_location))

        # Render scores with better formatting
        proLogic = scoresFont.render(f'Logic: {proLogicText}', True, WHITE)
        screen.blit(proLogic, (20, text_location + 150))

        proEvidence = scoresFont.render(f'Evidence: {proEvidenceText}', True, WHITE)
        screen.blit(proEvidence, (20, text_location + 200))

        proPersuasiveness = scoresFont.render(f'Persuasive: {proPersuasiveText}', True, WHITE)
        screen.blit(proPersuasiveness, (20, text_location + 250))

        proRelevance = scoresFont.render(f'Relevance: {proRelevanceText}', True, WHITE)
        screen.blit(proRelevance, (20, text_location + 300))

        # Calculate total score dynamically

        proTotal = scoresFont.render(f'Score: {proScore}', True, WHITE)
        screen.blit(proTotal, (20, text_location + 350))

        if proFeedback:
            # Split feedback into multiple lines if too long
            feedback_words = proFeedback.split()
            lines = []
            current_line = ""
            for word in feedback_words:
                if len(current_line + " " + word) < 30:  # Adjust character limit as needed
                    current_line += " " + word
                else:
                    lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)

                # Render each line
            for i, line in enumerate(lines):
                feedback_text = scoresFont.render(line, True, WHITE)
                screen.blit(feedback_text, (20, text_location + 400 + i * 25))

    def renderCons(self, isPro):
        conText = sideFont.render('CON', True, WHITE if isPro else RED)
        screen.blit(conText, (screen_width - awaypixel + text_location, text_location))

        # Render scores with better formatting
        conLogic = scoresFont.render(f'Logic: {conLogicText}', True, WHITE)
        screen.blit(conLogic, (screen_width - awaypixel + 20, text_location + 150))

        conEvidence = scoresFont.render(f'Evidence: {conEvidenceText}', True, WHITE)
        screen.blit(conEvidence, (screen_width - awaypixel + 20, text_location + 200))

        conPersuasiveness = scoresFont.render(f'Persuasive: {conPersuasiveText}', True, WHITE)
        screen.blit(conPersuasiveness, (screen_width - awaypixel + 20, text_location + 250))

        conRelevance = scoresFont.render(f'Relevance: {conRelevanceText}', True, WHITE)
        screen.blit(conRelevance, (screen_width - awaypixel + 20, text_location + 300))

        # Calculate total score dynamically
        conTotal = scoresFont.render(f'Score: {conScore}', True, WHITE)
        screen.blit(conTotal, (screen_width - awaypixel + 20, text_location + 350))

        if conFeedback:
            # Split feedback into multiple lines if too long
            feedback_words = conFeedback.split()
            lines = []
            current_line = ""
            for word in feedback_words:
                if len(current_line + " " + word) < 30:  # Adjust character limit as needed
                    current_line += " " + word
                else:
                    lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)

            # Render each line
            for i, line in enumerate(lines):
                feedback_text = scoresFont.render(line, True, WHITE)
                screen.blit(feedback_text, (screen_width - awaypixel + 20, text_location + 400 + i * 25))


# Fix for the main function
def debates():
    global index, proLogicText, proEvidenceText, proPersuasiveText, proRelevanceText, proScore, proFeedback
    global conLogicText, conEvidenceText, conPersuasiveText, conRelevanceText, conScore, conFeedback

    topicStr = ""
    isPro = True
    roundStart = False
    judgingState = False
    gameOver = False
    clock = pygame.time.Clock()
    messages = []
    input_text = ""
    bot = CyberBot()
    last_message_time = 0
    ui = UI()

    # AI side
    question_list = []
    q_list_index = 0
    messages.append(ChatMessage(TEXTS["initial_greeting"], False))
    index = 0
    running = True
    pro_arg = ""
    con_arg = ""

    while running:
        if not gameOver:
            current_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if input_text.strip() and roundStart and not judgingState:

                            if len(input_text) < 20:
                                messages.append(ChatMessage(TEXTS["requirements"], False))
                            else:
                                # messages.append(ChatMessage(input_text, True))

                                bot.state = "thinking"
                                last_message_time = current_time
                                if isPro:
                                    pro_arg = input_text
                                    isPro = False
                                    messages.append(ChatMessage("CON's turn to respond", False))
                                else:
                                    con_arg = input_text
                                    judgingState = True
                                    messages.append(ChatMessage("Judging arguments...", False))
                                input_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.key == pygame.K_h and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                        print_full_chat_history()
                    elif event.key == pygame.K_h and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                        print_full_chat_history()
                    elif event.key == pygame.K_c and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                        # Copy last message to clipboard
                        if messages:
                            last_msg = messages[-1].text
                            if copy_to_clipboard(last_msg):
                                messages.append(ChatMessage(TEXTS["clipboard"]["copy_success"], False))
                            else:
                                messages.append(ChatMessage(TEXTS["clipboard"]["copy_fail"], False))
                    else:
                        if len(input_text) < 70:
                            input_text += event.unicode


            # Handle judging state
            if judgingState:
                try:
                    # Show judging message and provide some delay for realism
                    if current_time - last_message_time > 3.0:
                        result = judge(topicStr, question_list[q_list_index], con_arg, pro_arg)
                        # Update scores
                        proLogicText = result['pro_scores']['logic']
                        proEvidenceText = result['pro_scores']['evidence']
                        proPersuasiveText = result['pro_scores']['persuasiveness']
                        proRelevanceText = result['pro_scores']['relevance']
                        round_pro_score = sum([proLogicText, proEvidenceText, proPersuasiveText, proRelevanceText])
                        proScore += round_pro_score
                        proFeedback = result['pro_feedback']

                        # During judging

                        conLogicText = result['con_scores']['logic']
                        conEvidenceText = result['con_scores']['evidence']
                        conPersuasiveText = result['con_scores']['persuasiveness']
                        conRelevanceText = result['con_scores']['relevance']
                        round_con_score = sum([conLogicText, conEvidenceText, conPersuasiveText, conRelevanceText])
                        conScore += round_con_score
                        conFeedback = result['con_feedback']


                        winner = "CON" if conScore > proScore else "CON"
                        messages.append(ChatMessage(f"Round complete! {winner} wins this round!", False))
                        # messages.append(ChatMessage(f"PRO feedback: {result['pro_feedback']}", False))
                        # messages.append(ChatMessage(f"CON feedback: {result['con_feedback']}", False))

                        # Move to next question or end game
                        if q_list_index + 1 < len(question_list):
                            q_list_index += 1
                            messages.append(ChatMessage(f"Next question: {question_list[q_list_index]}", False))
                            topicStr = question_list[q_list_index]
                            isPro = True  # Reset to PRO for next round
                        else:
                            # this is ending phase
                            messages.append(ChatMessage("Debate complete! Thank you for playing!", False))
                            gameOver = True
                            # Could add final score calculation here

                        judgingState = False
                        last_message_time = current_time

                except Exception as e:
                    print(f"Error during judging: {e}")
                    messages.append(ChatMessage("Error occurred during judging. Moving to next round.", False))
                    judgingState = False

            # Handle game start logic
            if not roundStart and not judgingState:
                start_screen = StartScreen(screen_width, screen_height)
                topic, rounds = start_screen.run()

                loading_screen = LoadingScreen(topic, rounds, screen_width, screen_height)
                loading_screen.run()

                if loading_screen.loading_progress >= 100:  # Changed from 20 to ensure full loading
                    try:
                        question_list = create_sub_topic_questions(topic, rounds)
                        # Start with the first question
                        if question_list and len(question_list) > 0:
                            topicStr = question_list[q_list_index]
                            messages.append(ChatMessage(f"Debate topic: {topic}", False))
                            # messages.append(ChatMessage(f"Question: {topicStr}", False))
                            messages.append(ChatMessage("PRO's turn to argue first", False))
                            roundStart = True
                            isPro = True
                        else:
                            messages.append(ChatMessage("Failed to generate questions. Please restart.", False))
                    except Exception as e:
                        print(f"Error starting game: {e}")
                        messages.append(ChatMessage("Error starting game. Please try again.", False))

            # Update bot animation
            screen.blit(background_image, (awaypixel, screen_height))
            bot.update()

            # Handle bot state
            if bot.state == "thinking" and current_time - last_message_time > 1.0:
                bot.state = "talking"
                last_message_time = current_time

            if current_time - last_message_time > 2.0 and bot.state == "talking":
                bot.state = "idle"

            # Draw everything
            screen.fill(DARK_BG)

            # Draw grid
            for x in range(0, screen_width, 40):
                pygame.draw.line(screen, (20, 25, 35), (x, 0), (x, screen_height), 1)
            for y in range(0, screen_height, 40):
                pygame.draw.line(screen, (20, 25, 35), (0, y), (screen_width, y), 1)

            # Draw bot and UI elements

            ui.drawLines()
            bot.draw(screen, (center_position_between_reds, 200))
            # Render topic text
            if roundStart:
                titleText = topicFont.render(f'{topicStr}', True, WHITE)
                text_x = center_position_between_reds - titleText.get_width() // 2
                text_y = 50
                screen.blit(titleText, (text_x, text_y))
                pygame.draw.line(screen, BLUE, (awaypixel, 100), (screen_width - awaypixel, 100))

                # Draw pros and cons
                ui.renderPro(isPro)
                ui.renderCons(isPro)

            # Draw status
            status_text = TEXTS["status_prefix"] + bot.state.upper()
            status_color = NEON_GREEN if bot.state == "idle" else NEON_PURPLE if bot.state == "thinking" else NEON_BLUE
            status_surface = font_status.render(status_text, True, status_color)
            pygame.draw.rect(screen, (20, 25, 35), (50, 50, status_surface.get_width() + 20, 40))
            screen.blit(status_surface, (60, 55))

            # Draw chat area
            pygame.draw.rect(screen, (15, 20, 30),
                             (awaypixel + 10, screen_height - chatHeight, screen_width - 2 * (awaypixel) - 20,
                              chatHeight))

            # Draw animated characters
            screen.blit(images[index], (table_offset_x - awaypixel, table_offset_y))
            screen.blit(tb_image, (table_offset_x - awaypixel, table_offset_y + 10))
            width = images2[index].get_width()
            screen.blit(images2[index], (table_offset_x - width+20 + awaypixel, table_offset_y))
            screen.blit(tb_image2, (table_offset_x, table_offset_y + 10))

            index = (index + 1) % len(images)

            # Draw messages
            y_offset = 50
            for msg in messages[-3:]:  # Show only last 8 messages
                height = msg.draw(screen, center_position_between_reds - 250, screen_height - 250 + y_offset)
                y_offset -= height

            # Draw input box
            if roundStart and not judgingState:
                input_rect = pygame.Rect(awaypixel + 10, screen_height - 200, screen_width - 2 * (awaypixel) - 20, 100)
                pygame.draw.rect(screen, (25, 30, 40), input_rect, border_radius=10)
                pygame.draw.rect(screen, NEON_BLUE, input_rect, 2, border_radius=10)

                prompt = TEXTS["input_prompt"] + input_text

                text_surface = font_main.render(prompt, True, TEXT_WHITE)
                screen.blit(text_surface, (input_rect.x + 15, input_rect.y + 10))

                if time.time() % 1 < 0.5:
                    cursor_x = input_rect.x + 15 + font_main.size(prompt)[0]
                    pygame.draw.line(screen, NEON_BLUE, (cursor_x, input_rect.y + 10),
                                     (cursor_x, input_rect.y + 30), 2)

            pygame.display.flip()
            clock.tick(FPS)
        else:
            score = proScore if proScore > conScore else conScore
            victory = "PRO WINS" if proScore > conScore else "CON WINS"


            restart = show_ending_screen(score, victory)
            if not restart:
                break
            else:
                # global index, proLogicText, proEvidenceText, proPersuasiveText, proRelevanceText, proScore, proFeedback
                # global conLogicText, conEvidenceText, conPersuasiveText, conRelevanceText, conScore, conFeedback

                topicStr = ""
                isPro = True
                roundStart = False
                judgingState = False
                gameOver = False
                clock = pygame.time.Clock()
                messages = []
                input_text = ""
                bot = CyberBot()
                last_message_time = 0
                ui = UI()

                # AI side
                question_list = []
                q_list_index = 0
                messages.append(ChatMessage(TEXTS["initial_greeting"], False))
                index = 0
                running = True
                pro_arg = ""
                con_arg = ""
    save_chat_history()
    pygame.quit()


if __name__ == "__main__":
    debates()
