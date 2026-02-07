import pygame
import sys

# --- Инициализация ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Anime Game")
clock = pygame.time.Clock()

# Шрифты
font = pygame.font.SysFont("Arial", 26)
name_font = pygame.font.SysFont("Arial", 30, bold=True)


# --- Функция загрузки персонажа ---
def load_char(filename):
    try:
        img = pygame.image.load(filename).convert_alpha()
        # Масштабируем под экран (высота 550)
        ratio = 550 / img.get_height()
        new_size = (int(img.get_width() * ratio), 550)
        return pygame.transform.scale(img, new_size)
    except:
        # Если файла нет - рисуем розовый квадрат
        surf = pygame.Surface((300, 500))
        surf.fill((255, 100, 200))
        return surf


# Загружаем спрайты (файлы должны быть в папке с проектом)
char_idle = load_char("char_normal.png")
char_angry = load_char("char_angry.png")

# --- Сюжет ---
scenes = {
    "start": {
        "text": "Саки: Привет... Ты чего так смотришь? Мы же договаривались встретиться.",
        "image": char_idle,
        "choices": [
            {"text": "Извини, я засмотрелся на тебя", "next": "sweet"},
            {"text": "Ты опять за старое? Хватит ныть.", "next": "bad"}
        ]
    },
    "sweet": {
        "text": "Саки: *краснеет* Ну... ладно. Только сегодня не опаздывай больше.",
        "image": char_idle,
        "choices": [{"text": "Пойти на свидание", "next": "start"}]
    },
    "bad": {
        "text": "Саки: Что?! Ты совсем обнаглел? Уходи, я не хочу тебя видеть!",
        "image": char_angry,
        "choices": [{"text": "Попросить прощения", "next": "start"}]
    }
}

current_scene = "start"

# --- Основной цикл ---
while True:
    screen.fill((40, 40, 60))  # Фон (темно-синий)
    mouse_pos = pygame.mouse.get_pos()
    data = scenes[current_scene]

    # 1. Рисуем персонажа
    char_rect = data["image"].get_rect(midbottom=(WIDTH // 2, HEIGHT - 50))
    screen.blit(data["image"], char_rect)

    # 2. Окно диалога
    pygame.draw.rect(screen, (20, 20, 20), (50, 420, 700, 150))
    pygame.draw.rect(screen, (255, 255, 255), (50, 420, 700, 150), 2)

    # Текст диалога
    text_surf = font.render(data["text"], True, (255, 255, 255))
    screen.blit(text_surf, (70, 450))

    # 3. Кнопки выбора
    button_rects = []
    for i, choice in enumerate(data["choices"]):
        btn_rect = pygame.Rect(500, 50 + (i * 70), 280, 50)
        button_rects.append((btn_rect, choice["next"]))

        # Эффект наведения
        bg_color = (100, 100, 250) if btn_rect.collidepoint(mouse_pos) else (60, 60, 60)
        pygame.draw.rect(screen, bg_color, btn_rect)
        pygame.draw.rect(screen, (255, 255, 255), btn_rect, 1)

        btn_text = font.render(choice["text"], True, (255, 255, 255))
        screen.blit(btn_text, (btn_rect.x + 10, btn_rect.y + 10))

    # 4. События
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for rect, next_s in button_rects:
                if rect.collidepoint(mouse_pos):
                    current_scene = next_s

    pygame.display.flip()
    clock.tick(60)
    