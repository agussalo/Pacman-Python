import pygame
import sys

pygame.init()

# --- Configuración ---
TAM = 24  # tamaño de cada celda
FPS = 10

# Mapa: 1 = pared, 0 = camino con punto, 2 = camino vacío, 3 = posición inicial pacman
MAPA = [
    "1111111111111111111111",
    "1000000000110000000001",
    "1011110111110111101101",
    "1000000000000000000001",
    "1011101101110111011101",
    "1000100000110000010001",
    "1110111011111011101111",
    "1000000110330011000001",
    "1011111011111011111101",
    "1000000000000000000001",
    "1011011111001111101101",
    "1000010000000000010001",
    "1111111111111111111111",
]

FILAS = len(MAPA)
COLUMNAS = len(MAPA[0])
ANCHO = COLUMNAS * TAM
ALTO = FILAS * TAM

NEGRO = (0, 0, 0)
AZUL = (33, 33, 222)
AMARILLO = (255, 255, 0)
BLANCO = (255, 255, 255)
ROJO = (220, 30, 30)

pantalla = pygame.display.set_mode((ANCHO, ALTO + 40))
pygame.display.set_caption("Pacman")
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("arial", 26, bold=True)


def cargar_mapa():
    puntos = set()
    paredes = set()
    inicio = (1, 1)
    for f, fila in enumerate(MAPA):
        for c, val in enumerate(fila):
            if val == "1":
                paredes.add((f, c))
            elif val == "0":
                puntos.add((f, c))
            elif val == "3":
                inicio = (f, c)
    return paredes, puntos, inicio


class Fantasma:
    def __init__(self, fila, col, color):
        self.fila = fila
        self.col = col
        self.color = color
        self.dir = (0, 1)

    def mover(self, paredes):
        opciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        # intenta seguir en la misma dirección si puede
        df, dc = self.dir
        nf, nc = self.fila + df, self.col + dc
        if (nf, nc) in paredes or not (0 <= nf < FILAS and 0 <= nc < COLUMNAS):
            import random
            random.shuffle(opciones)
            for d in opciones:
                nf, nc = self.fila + d[0], self.col + d[1]
                if (nf, nc) not in paredes and 0 <= nf < FILAS and 0 <= nc < COLUMNAS:
                    self.dir = d
                    break
            nf, nc = self.fila + self.dir[0], self.col + self.dir[1]
        self.fila, self.col = nf, nc

    def dibujar(self):
        x = self.col * TAM + TAM // 2
        y = self.fila * TAM + TAM // 2
        pygame.draw.circle(pantalla, self.color, (x, y), TAM // 2 - 2)


def dibujar_mapa(paredes, puntos):
    pantalla.fill(NEGRO)
    for (f, c) in paredes:
        pygame.draw.rect(pantalla, AZUL, (c * TAM, f * TAM, TAM, TAM))
    for (f, c) in puntos:
        x = c * TAM + TAM // 2
        y = f * TAM + TAM // 2
        pygame.draw.circle(pantalla, BLANCO, (x, y), 3)


def dibujar_pacman(fila, col):
    x = col * TAM + TAM // 2
    y = fila * TAM + TAM // 2
    pygame.draw.circle(pantalla, AMARILLO, (x, y), TAM // 2 - 2)


def main():
    paredes, puntos, (fila, col) = cargar_mapa()
    direccion = (0, 0)
    siguiente_dir = (0, 0)
    fantasmas = [Fantasma(7, 10, ROJO), Fantasma(7, 12, (255, 140, 200))]
    puntaje = 0
    vidas = 3
    game_over = False
    gano = False

    contador_fantasma = 0

    while True:
        reloj.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_LEFT, pygame.K_a):
                    siguiente_dir = (0, -1)
                elif evento.key in (pygame.K_RIGHT, pygame.K_d):
                    siguiente_dir = (0, 1)
                elif evento.key in (pygame.K_UP, pygame.K_w):
                    siguiente_dir = (-1, 0)
                elif evento.key in (pygame.K_DOWN, pygame.K_s):
                    siguiente_dir = (1, 0)
                elif evento.key == pygame.K_r and (game_over or gano):
                    main()
                    return

        if not game_over and not gano:
            # intenta girar si es posible
            nf, nc = fila + siguiente_dir[0], col + siguiente_dir[1]
            if (nf, nc) not in paredes and 0 <= nf < FILAS and 0 <= nc < COLUMNAS:
                direccion = siguiente_dir

            nf, nc = fila + direccion[0], col + direccion[1]
            if (nf, nc) not in paredes and 0 <= nf < FILAS and 0 <= nc < COLUMNAS:
                fila, col = nf, nc

            if (fila, col) in puntos:
                puntos.remove((fila, col))
                puntaje += 10

            if not puntos:
                gano = True

            contador_fantasma += 1
            if contador_fantasma >= 2:
                contador_fantasma = 0
                for fan in fantasmas:
                    fan.mover(paredes)

            for fan in fantasmas:
                if fan.fila == fila and fan.col == col:
                    vidas -= 1
                    fila, col = cargar_mapa()[2]
                    direccion = (0, 0)
                    siguiente_dir = (0, 0)
                    if vidas <= 0:
                        game_over = True

        dibujar_mapa(paredes, puntos)
        dibujar_pacman(fila, col)
        for fan in fantasmas:
            fan.dibujar()

        texto = fuente.render(f"Puntaje: {puntaje}   Vidas: {vidas}", True, BLANCO)
        pantalla.blit(texto, (10, ALTO + 5))

        if game_over:
            msg = fuente.render("GAME OVER - Presioná R", True, ROJO)
            pantalla.blit(msg, (ANCHO // 2 - msg.get_width() // 2, ALTO // 2))
        elif gano:
            msg = fuente.render("¡GANASTE! - Presioná R", True, AMARILLO)
            pantalla.blit(msg, (ANCHO // 2 - msg.get_width() // 2, ALTO // 2))

        pygame.display.flip()


if __name__ == "__main__":
    main()