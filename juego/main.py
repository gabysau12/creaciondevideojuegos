import pygame
import os
import random

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Animación de Personaje")

# Cargar sprites
def load_images(action):
    images = []
    path = f"sprites/{action}"
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        try:
            img = pygame.image.load(filepath).convert_alpha()
            images.append(img)
        except pygame.error:
            print(f"Error loading image: {filepath}")
    return images

# Cargar fondo de juego
background = pygame.image.load("sprites/background.png").convert()
background = pygame.transform.scale(background, (screen_width, screen_height))

# Cargar fondo de la pantalla de inicio
start_screen_background = pygame.image.load("sprites/start_screen_bg.png").convert()
start_screen_background = pygame.transform.scale(start_screen_background, (screen_width, screen_height))

# Acciones del personaje
idle_sprites = load_images("idle")    
run_sprites = load_images("run")      
jump_sprites = load_images("jump")    
crouch_sprites = load_images("crouch") 

# Verificar si los sprites se cargaron correctamente
if not run_sprites:
    print("Error: No se encontraron sprites de correr.")
    pygame.quit()
    quit()

# Cargar obstáculo
obstacle_image = pygame.image.load("sprites/obstacle.png").convert_alpha()
obstacle_image = pygame.transform.scale(obstacle_image, (30, 30))  # Ajusta el tamaño del obstáculo

# Variables del personaje
current_sprite = 0
action = "idle"
sprites = idle_sprites
is_jumping = False
is_crouching = False
can_jump = True

# Posición del personaje
x = 50
y_ground = screen_height - 150
y = y_ground
x_speed = 5
jump_height = 150
jump_speed = 10
gravity = 0.5
jump_speed_initial = jump_speed

# Posición del fondo
bg_x = 0

# Reloj para controlar la velocidad de fotogramas
clock = pygame.time.Clock()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
AQUA = (0, 255, 255)
BUTTON_COLOR = (0, 153, 204)

# Fuente
small_font = pygame.font.Font(None, 30)
big_font = pygame.font.Font(None, 74)

# Función para dibujar el texto en el botón
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text.upper(), True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Función para la pantalla de inicio
def show_start_screen():
    start_button = pygame.Rect(screen_width // 2 + 70, screen_height // 2 - 50, 200, 50)
    exit_button = pygame.Rect(screen_width // 2 + 70, screen_height // 2 + 50, 200, 50)
    
    while True:
        screen.blit(start_screen_background, (0, 0))  
        pygame.draw.rect(screen, BUTTON_COLOR, start_button)
        draw_text('START', small_font, WHITE, screen, start_button.centerx, start_button.centery)
        pygame.draw.rect(screen, BUTTON_COLOR, exit_button)
        draw_text('EXIT', small_font, WHITE, screen, exit_button.centerx, exit_button.centery)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return  
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    quit()
        
        pygame.display.update()
        clock.tick(30)

# Crear un evento para generar obstáculos
OBSTACLE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(OBSTACLE_EVENT, 5000)  # 5000 ms = 5 segundos

# Ciclo principal del juego
def main_game():
    global x, y, is_jumping, is_crouching, can_jump, bg_x, current_sprite, action, sprites

    running = True
    obstacle_rect = None
    obstacle_x = None

    while running:
        screen.fill(WHITE)

        keys = pygame.key.get_pressed()

        # Manejo de movimiento y acciones
        if keys[pygame.K_RIGHT]:
            x += x_speed
            bg_x -= x_speed * 2  # Mover el fondo más rápido
            if keys[pygame.K_SPACE] and can_jump and y == y_ground:
                action = "jump"
                sprites = jump_sprites
                is_jumping = True
                is_crouching = False
                can_jump = False
            elif keys[pygame.K_DOWN]:
                action = "crouch"
                sprites = crouch_sprites
                is_crouching = True
            else:
                action = "run"
                sprites = run_sprites
        elif keys[pygame.K_DOWN]:
            action = "crouch"
            sprites = crouch_sprites
            is_crouching = True
        elif keys[pygame.K_SPACE] and can_jump:
            action = "jump"
            sprites = jump_sprites
            is_jumping = True
            is_crouching = False
            can_jump = False
        else:
            action = "idle"
            sprites = idle_sprites
            is_crouching = False

        # Lógica del salto
        if is_jumping:
            y -= jump_speed
            if y <= y_ground - jump_height:
                y = y_ground - jump_height
                jump_speed = -jump_speed  # Corrección de indentación
        else:
            if y < y_ground:
                y += gravity
            if y >= y_ground:
                y = y_ground
                is_jumping = False
                can_jump = True  # Reset can_jump to True when landing
                jump_speed = jump_speed_initial

        # Asegurar que el personaje no se salga de la pantalla
        if x < 0:
            x = 0
        if x > screen_width - sprites[0].get_width():
            x = screen_width - sprites[0].get_width()

        if y < 0:
            y = 0
        if y > screen_height - sprites[0].get_height():
            y = screen_height - sprites[0].get_height()

        # Dibujar el fondo
        screen.blit(background, (bg_x, 0))
        screen.blit(background, (bg_x + screen_width, 0))

        # Resetea la posición del fondo si se sale de la pantalla
        if bg_x < -screen_width:
            bg_x = 0

        # Generar obstáculo
        for event in pygame.event.get ():
            if event.type == OBSTACLE_EVENT:
                obstacle_x = screen_width // 2  # Ajusta la posición del obstáculo a la mitad de la pantalla
                obstacle_rect = obstacle_image.get_rect(topleft=(obstacle_x, y - 50))  # Ajusta la altura a la del personaje

        # Dibujar el obstáculo si existe
        if obstacle_rect:
            screen.blit(obstacle_image, obstacle_rect.topleft)

            # Verificar colisión con el obstáculo
            if sprites and obstacle_rect.colliderect(pygame.Rect(x, y, sprites[0].get_width(), sprites[0].get_height())):
                print("Colisión con el obstáculo!")

        # Actualizar el sprite actual
        if action != "idle":
            current_sprite = (current_sprite + 1) % len(sprites)

        # Dibujar el personaje en pantalla
        if sprites:
            if action == "crouch":
                screen.blit(sprites[0], (x, y - sprites[0].get_height()))
            else:
                screen.blit(sprites[current_sprite], (x, y - sprites[current_sprite].get_height()))
        else:
            print("No hay sprites para mostrar.")

        # Actualizar la pantalla
        pygame.display.update()
        clock.tick(30)

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    quit()

# Mostrar pantalla de inicio
show_start_screen()

# Iniciar el juego
main_game()
