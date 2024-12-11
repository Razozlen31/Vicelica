
import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Виселица")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Шрифт
font = pygame.font.SysFont('gotic', 51)

# Словари категорий
categories = {
    'Животные': ['кошка', 'собака', 'попугай', 'слон', 'тигр', 'черепаха', 'жираф', 'муравьед'],
    'Природа': ['река', 'океан', 'горы', 'озеро', 'лес', 'водопад', 'джунгли', 'пустыня'],
    'Технологии': ['компьютер', 'интернет', 'телефон', 'гаджет', 'программирование', 'телевизор', 'радио', 'геймпад'],
    'Спорт': ['футбол', 'баскетбол', 'теннис', 'волейбол', 'бокс', 'армрестлинг','бобслей','шахматы'],
    'Искусство': ['гитара', 'пианино', 'скрипка', 'флейта', 'труба', 'кисточка', 'краска', 'моделирование']
}

# Переменная для отслеживания состояния звука
sound_on = True

# Функция для отображения текста на экране
def draw_text(text, x, y):
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (x, y))

# Функция рисования кнопки
def draw_button(text, x, y, width, height, color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    draw_text(text, x + 10, y + 10)

DARK_BROWN = (101, 67, 33)

# Функция для рисования виселицы
def draw_hangman(attempts):
    if attempts >= 1:
        pygame.draw.line(screen, DARK_BROWN, (150, 500), (150, 100), 5)  # Основание
    if attempts >= 2:
        pygame.draw.line(screen, DARK_BROWN, (150, 100), (300, 100), 5)  # Крыша
    if attempts >= 3:
        pygame.draw.line(screen, DARK_BROWN, (300, 100), (300, 200), 5)  # Столб
    if attempts >= 4:
        pygame.draw.circle(screen, BLACK, (300, 220), 20)  # Голова
    if attempts >= 5:
        pygame.draw.line(screen, BLACK, (300, 240), (300, 360), 5)  # Тело
    if attempts >= 6:
        pygame.draw.line(screen, BLACK, (300, 270), (250, 300), 5)  # Левая рука
    if attempts >= 7:
        pygame.draw.line(screen, BLACK, (300, 270), (350, 300), 5)  # Правая рука
    if attempts >= 8:
        pygame.draw.line(screen, BLACK, (300, 360), (250, 400), 5)  # Левая нога
    if attempts >= 9:
        pygame.draw.line(screen, BLACK, (300, 360), (350, 400), 5)  # Правая нога
    if attempts >= 10:
        draw_text("Игра окончена! Вы проиграли.", 200, 50)

# Функция меню выбора категории
def category_menu():
    while True:
        screen.fill(WHITE)
        draw_text("Выберите категорию", 220, 100)

        for i, category in enumerate(categories.keys()):
            draw_button(category, 290, 190 + i * 60, 230, 50, GREEN)

        draw_button("Выход", 290, 200 + len(categories) * 60 + 20, 200, 50, RED)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Корректное завершение
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for i, category in enumerate(categories.keys()):
                    if 290 <= mouse_x <= 520 and (190 + i * 60) <= mouse_y <= (240 + i * 60):
                        game_loop(categories[category])  # Запускаем игру с выбранной категорией
                if 290 <= mouse_x <= 490 and (200 + len(categories) * 60 + 20) <= mouse_y <= (250 + len(categories) * 60 + 20):
                    return False  # Корректное завершение

        pygame.display.update()

# Начальное меню
def main_menu():
    global sound_on
   
    

    # Загрузка фона
    background_image = pygame.image.load('fon.jpg')
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
    
    while True:
        screen.blit(background_image, (0, 0))
        draw_text("Добро пожаловать в Виселицу!", 120, 100)

        draw_button("Начать игру", 275, 250, 230, 60, GREEN)
        draw_button("Выход", 275, 320, 230, 60, RED)


        # Отображение состояния звука
        sound_button_text = "Звук: Включен" if sound_on else "Звук: Выключен"
        sound_text_surface = font.render(sound_button_text, True, BLACK)
        sound_button_width = sound_text_surface.get_width() + 20
        draw_button(sound_button_text, 490, 400, sound_button_width, 60, GREEN if sound_on else RED)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return False  # Конец игры
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 275 <= mouse_x <= 505 and 250 <= mouse_y <= 310:
                    category_menu()  # Переход к выбору категории
                if 275 <= mouse_x <= 505 and 320 <= mouse_y <= 380:
                    pygame.mixer.music.stop()
                    return False  # Конец игры
                if 490 <= mouse_x <= 490 + sound_button_width and 400 <= mouse_y <= 460:
                    toggle_sound()

        pygame.display.update()

# Функция для переключения звука
def toggle_sound():
    global sound_on
    sound_on = not sound_on
    if sound_on:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()

# Игровой цикл
def game_loop(word_list):
    global guessed_letters, wrong_guesses, chosen_word
    guessed_letters = []
    wrong_guesses = 0
    chosen_word = random.choice(word_list)
    max_attempts = 10
    running = True

    while running:
        screen.fill(WHITE)
        draw_hangman(wrong_guesses)
        draw_text(f'Попытки: {wrong_guesses}/{max_attempts}', 280, 450)

        # Отображение загаданного слова
        display_word = ' '.join(letter if letter in guessed_letters else '_' for letter in chosen_word)
        draw_text(display_word, 350, 250)

        # Проверка на выигрыш
        if all(letter in guessed_letters for letter in chosen_word):
            draw_text("Поздравляем! Вы выиграли!", 200, 50)
            pygame.display.update()
            pygame.time.delay(2000)
            return  # Завершение игры и возвращение в меню выбора категории

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha() and len(event.unicode) == 1:
                    letter = event.unicode.lower()
                    if letter not in guessed_letters:
                        guessed_letters.append(letter)
                        if letter not in chosen_word:
                            wrong_guesses += 1
                            if wrong_guesses >= max_attempts:
                                draw_text("Вы проиграли, слово: " + chosen_word, 50, 50)
                                pygame.display.update()
                                pygame.time.delay(2000)
                                return  # Завершение игры и возвращение в меню выбора категории

        pygame.display.update()

# Запускаем начальное меню
if main_menu() is False:
    pygame.quit()
