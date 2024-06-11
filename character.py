import pygame
import sys
import spacy

def main():
    pygame.init()

    # Definir el laberinto
    maze = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
        [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]

    # Configuración del laberinto
    cell_size = 40
    maze_rows = len(maze)
    maze_cols = len(maze[0])

    # Configura el tamaño de la ventana para que se ajuste al laberinto
    screen_width = maze_cols * cell_size
    screen_height = maze_rows * cell_size
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Carga la imagen del personaje
    character = pygame.image.load('dino.png')
    character = pygame.transform.scale(character, (cell_size, cell_size))
    character_width = character.get_width()
    character_height = character.get_height()   

    # Posición inicial del personaje
    x, y = 0, 7 #0, 7 - 11, 4

    # Carga el modelo de Spacy
    nlp = spacy.load('es_core_news_md')

    # Configura la caja de texto
    base_font = pygame.font.Font(None, 32)
    user_text = ''
    input_rect = pygame.Rect(5, 20, 140, 32)
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('chartreuse4')
    color = color_passive
    active = False

    # Función para dibujar el laberinto
    def draw_maze():
        for row in range(maze_rows):
            for col in range(maze_cols):
                color = (0, 0, 0) if maze[row][col] == 1 else (173, 216, 230)
                pygame.draw.rect(screen, color, pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size))

    # Función para mostrar el cuadro de opciones
    def show_options():
        option_font = pygame.font.Font(None, 50)
        while True:
            screen.fill((255, 255, 255))
            draw_maze()
            screen.blit(character, (x * cell_size, y * cell_size))

            # Dibuja el cuadro de opciones
            option_rect = pygame.Rect(screen_width // 4, screen_height // 3, screen_width // 2, screen_height // 3)
            pygame.draw.rect(screen, (0, 0, 0), option_rect)
            pygame.draw.rect(screen, (255, 255, 255), option_rect, 5)

            # Dibuja la opción de salir
            quit_text = option_font.render('Salir', True, (255, 0, 0))
            quit_rect = quit_text.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(quit_text, quit_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if quit_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        doc = nlp(user_text)

                        # Mueve el personaje de acuerdo al comando
                        for token in doc:
                            text = token.text.lower()  # Convierte el texto a minúsculas
                            if text in ['arriba', 'up'] and y - 1 >= 0 and maze[y - 1][x] == 0:
                                y -= 1
                            elif text in ['abajo', 'down'] and y + 1 < maze_rows and maze[y + 1][x] == 0:
                                y += 1
                            elif text in ['izquierda', 'left'] and x - 1 >= 0 and maze[y][x - 1] == 0:
                                x -= 1
                            elif text in ['derecha', 'right'] and x + 1 < maze_cols and maze[y][x + 1] == 0:
                                x += 1

                        user_text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode

        # Limpia la pantalla y dibuja el laberinto y el personaje
        screen.fill((255, 255, 255))
        draw_maze()
        screen.blit(character, (x * cell_size, y * cell_size))

        # Dibuja la caja de texto
        if active:
            color = color_active
        else:
            color = color_passive
        pygame.draw.rect(screen, color, input_rect, 2)
        text_surface = base_font.render(user_text, True, (255, 255, 255))
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

        # Verifica si el personaje ha pasado el laberinto
        if y == 1 and x == 16:
            font = pygame.font.Font(None, 74)
            text = font.render('Pasaste el laberinto!', True, (0, 255, 0))
            text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
            box_rect = pygame.Rect(text_rect.left - 20, text_rect.top - 20, text_rect.width + 40, text_rect.height + 40)
            pygame.draw.rect(screen, (0, 0, 0), box_rect)
            pygame.draw.rect(screen, (255, 255, 255), box_rect, 5)
            screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.wait(2000)
            show_options()

        # Actualiza la pantalla
        pygame.display.flip()

if __name__ == '__main__':
    main()
