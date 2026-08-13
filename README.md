# Pacman - Python

Recreación del clásico **Pacman**, desarrollada en Python con la librería **Pygame**. El mapa, los puntos, Pacman y los fantasmas se dibujan con gráficos generados por código (círculos y rectángulos de colores), sin imágenes externas.

## 🎮 Cómo jugar

| Acción | Tecla |
|---|---|
| Mover | Flechas o `W` `A` `S` `D` |
| Reiniciar (tras game over o victoria) | `R` |
| Salir | Cerrar la ventana |

El objetivo es recorrer el mapa comiendo todos los puntos sin ser tocado por los fantasmas. Cada punto suma 10 al puntaje. El jugador cuenta con 3 vidas; al perderlas todas, termina la partida. Si se comen todos los puntos, se gana el nivel.

## 🛠️ Tecnologías

- Python 3
- Pygame

## ▶️ Cómo correrlo

```bash
pip install pygame
python pacman.py
```

## ✨ Detalles técnicos

- Mapa definido como matriz de texto (paredes, puntos y posición inicial)
- Sistema de movimiento por celdas con detección de colisión contra paredes
- Fantasmas con movimiento semi-aleatorio: intentan mantener su dirección y giran al chocar con una pared
- Sistema de puntaje, vidas y estados de juego (game over / victoria)
- Reinicio de partida sin cerrar la ventana

---

Proyecto de práctica personal, hecho para reforzar lógica de programación, manejo de mapas basados en grillas y movimiento de entidades en Pygame.
