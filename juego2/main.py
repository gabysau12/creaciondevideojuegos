import pygame
import random
import os

# Clase para manejar el personaje principal, Alex
class Alex:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 5  
        self.is_jumping = False
        self.is_crouching = False
        self.jump_height = 20
        self.gravity = 1
        self.current_frame = 0 
        self.action = "idle"
        self.load_sprites()

    def load_sprites(self):
        try:
            self.run_frames = [pygame.image.load(os.path.join('assets', 'characters', 'run', f'frame_{i}.png')) for i in range(1, 4)]
            self.idle_frames = [pygame.image.load(os.path.join('assets', 'characters', 'idle', f'frame_{i}.png')) for i in range(1, 2)]
            self.jump_frames = [pygame.image.load(os.path.join('assets', 'characters', 'jump', f'frame_{i}.png')) for i in range(1, 3)]
            self.crouch_frames = [pygame.image.load(os.path.join('assets', 'characters', 'crouch', f'frame_{i}.png')) for i in range(1, 2)]
        except Exception as e:
            print(f"Error cargando sprites: {e}")

    def update(self, keys):
        if keys[pygame.K_RIGHT]:
            self.x += self.vel
            self.action = "run"
        elif keys[pygame.K_DOWN]:
            self.is_crouching = True
            self.action = "crouch"
        elif keys[pygame.K_SPACE] and not self.is_jumping:
            self.is_jumping = True
            self.action = "jump"
        else:
            self.action = "idle"
            self.is_crouching = False

        if self.is_jumping:
            self.y -= self.jump_height
            self.jump_height -= self.gravity
            if self.jump_height < -20:
                self.is_jumping = False
                self.jump_height = 20

        self.current_frame = (self.current_frame + 1) % len(getattr(self, f"{self.action}_frames"))

    def draw(self, screen):
        frame = getattr(self, f"{self.action}_frames")[self.current_frame]
        screen.blit(frame, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 50, 50)


class Obstacle:
    def __init__(self, x, y, img_path):
        self.rect = pygame.Rect(x, y, 100, 100)
        try:
            self.image = pygame.image.load(img_path)
            self.image = pygame.transform.scale(self.image, (100, 100))
        except Exception as e:
            print(f"Error cargando obstáculo {img_path}: {e}")
            self.image = pygame.Surface((100, 100))  # Superficie vacía en caso de error

    def move(self, speed):
        self.rect.x -= speed

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Level:
    def __init__(self, background_img, repetitions):
        try:
            self.background = pygame.image.load(background_img)
            self.background = pygame.transform.scale(self.background, (800, 600))
        except Exception as e:
            print(f"Error cargando fondo {background_img}: {e}")
            self.background = pygame.Surface((800, 600))  # Superficie vacía en caso de error
        self.repetitions = repetitions
        self.obstacles = []
        self.background_x = 0
        pygame.time.set_timer(pygame.USEREVENT, 3000)

    def generate_obstacle(self):
        x = 800
        y = 500

        if current_level == 0:
            img_path = random.choice([
                os.path.join('assets', 'obstacles', 'barrier.png'),
                os.path.join('assets', 'obstacles', 'bird.png')
            ])
            if 'bird.png' in img_path:
                y = 350
        elif current_level == 1:
            img_path = random.choice([
                os.path.join('assets', 'obstacles', 'puddle.png'),
                os.path.join('assets', 'obstacles', 'branch.png'),
                os.path.join('assets', 'obstacles', 'bird.png')
            ])
            if 'bird.png' in img_path:
                y = 350
        elif current_level == 2:
            img_path = random.choice([
                os.path.join('assets', 'obstacles', 'box.png'),
                os.path.join('assets', 'obstacles', 'bird.png')
            ])
            if 'bird.png' in img_path:
                y = 350
        else:
            img_path = random.choice([
                os.path.join('assets', 'obstacles', 'barrier.png'),
                os.path.join('assets', 'obstacles', 'bird.png'),
                os.path.join('assets', 'obstacles', 'puddle.png'),
                os.path.join('assets', 'obstacles', 'branch.png'),
                os.path.join('assets', 'obstacles', 'box.png')
            ])
            if 'bird.png' in img_path:
                y = 350

        obstacle = Obstacle(x, y, img_path)
        self.obstacles.append(obstacle)

    def update(self, speed):
        for obstacle in self.obstacles[:]:
            obstacle.move(speed)
            if obstacle.rect.x < -100:
                self.obstacles.remove(obstacle)
        self.background_x -= speed
        if self.background_x < -800:
            self.background_x = 0

    def draw(self, screen):
        for i in range(self.repetitions):
            screen.blit(self.background, (i * 800 + self.background_x, 0))
        for obstacle in self.obstacles:
            obstacle.draw(screen)


def check_collision(alex, obstacles):
    for obstacle in obstacles:
        if alex.get_rect().colliderect(obstacle.rect):
            return True
    return False


# Función para mostrar la pantalla de "Game Over"
def show_game_over(screen):
    font = pygame.font.Font(None, 80)
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    restart_text = font.render("Presiona R para reiniciar", True, (255, 255, 255))

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(game_over_text, (200, 250))
        screen.blit(restart_text, (100, 350))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return  # Regresa para reiniciar el juego

        pygame.display.flip()


# Función para la pantalla de inicio
def show_start_screen(screen):
    font = pygame.font.Font(None, 50)
    start_text = font.render('Start', True, (255, 255, 255))
    exit_text = font.render('Exit', True, (255, 255, 255))

    start_button = pygame.Rect(474, 250, 200, 60)
    exit_button = pygame.Rect(474, 350, 200, 60)

    try:
        start_screen_image = pygame.image.load(os.path.join('assets', 'backgrounds', 'start_screen_image.png'))
        start_screen_image = pygame.transform.scale(start_screen_image, (800, 600))
    except Exception as e:
        print(f"Error cargando imagen de pantalla de inicio: {e}")
        start_screen_image = pygame.Surface((800, 600))  # Superficie vacía en caso de error

    running = True
    while running:
        screen.fill((135, 206, 250))
        screen.blit(start_screen_image, (0, 0))

        pygame.draw.rect(screen, (0, 0, 255), start_button)
        pygame.draw.rect(screen, (0, 0, 255), exit_button)

        screen.blit(start_text, (start_button.x + 60, start_button.y + 10))
        screen.blit(exit_text, (exit_button.x + 60, exit_button.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if start_button.collidepoint(mouse_pos):
                    return
                elif exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    exit()

        pygame.display.flip()


# Función para mostrar la pantalla de selección de niveles con botones semitransparentes
def show_level_selection(screen, unlocked_levels):
    font = pygame.font.Font(None, 50)
    level_buttons = []

    # Crear botones para cada nivel
    for i in range(4):
        x = 300
        y = 150 + i * 100
        text = f'Nivel {i + 1}'
        level_buttons.append((pygame.Rect(x, y, 200, 60), text, i <= unlocked_levels))

    running = True
    while running:
        screen.fill((0, 0, 0))

        for rect, text, unlocked in level_buttons:
            # Crear una superficie con transparencia para cada botón
            button_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            if unlocked:
                # Botones desbloqueados en amarillo con 50% de transparencia
                button_surface.fill((255, 255, 0, 128))  # Amarillo con transparencia
            else:
                # Botones bloqueados en gris con 50% de transparencia
                button_surface.fill((128, 128, 128, 128))  # Gris con transparencia

            # Dibujar el botón con transparencia en la pantalla
            screen.blit(button_surface, (rect.x, rect.y))

            # Renderizar el texto del botón
            level_text = font.render(text, True, (255, 255, 255))
            screen.blit(level_text, (rect.x + 50, rect.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for rect, text, unlocked in level_buttons:
                    if rect.collidepoint(mouse_pos) and unlocked:
                        return level_buttons.index((rect, text, unlocked))

        pygame.display.flip()


def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("El Camino de Alex")
    clock = pygame.time.Clock()

    global current_level
    levels = [
        Level(os.path.join('assets', 'backgrounds', 'city.png'), 6),     # Repeat 6 times
        Level(os.path.join('assets', 'backgrounds', 'park.png'), 8),     # Repeat 8 times
        Level(os.path.join('assets', 'backgrounds', 'market.png'), 10),  # Repeat 10 times
        Level(os.path.join('assets', 'backgrounds', 'plaza.png'), 12)    # Repeat 12 times
    ]

    unlocked_levels = 0  # Niveles desbloqueados

    show_start_screen(screen)  # Mostrar pantalla de inicio

    while True:
        # Pantalla de selección de niveles
        current_level = show_level_selection(screen, unlocked_levels)
        alex = Alex(100, 450)

        finish_line = pygame.Rect(800, 200, 5, 400)  # Línea de meta en el borde derecho

        running = True
        while running:
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.USEREVENT:
                    levels[current_level].generate_obstacle()

            alex.update(keys)
            levels[current_level].update(5)

            # Verificar colisiones
            if check_collision(alex, levels[current_level].obstacles):
                print("¡Alex ha perdido!")
                show_game_over(screen)
                running = False  # Salir del ciclo actual para volver a la selección de niveles
                break

            # Comprobar si Alex cruza la línea de meta
            if alex.x > finish_line.x:
                unlocked_levels = current_level + 1 if current_level + 1 > unlocked_levels else unlocked_levels
                print("¡Felicidades! Has cruzado la meta.")
                running = False  # Terminar el nivel
                break

            screen.fill((135, 206, 250))
            levels[current_level].draw(screen)
            alex.draw(screen)
            pygame.draw.rect(screen, (255, 0, 0), finish_line)  # Dibuja la línea de meta
            pygame.display.flip()
            clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    game_loop()

