import pygame
import sys
from graficos import dibujar_menu_principal, mostrar_mensaje_centrado
from partida import jugar_partida

pygame.init()

# Tamaño de la ventana
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego del Impostor")

# Modos de juego: (nombre, tiempo por ronda)
MODOS = [
    ("Rápido", 30),
    ("Normal", 60),
    ("Largo", 120),
]

# Temáticas disponibles
TEMATICAS = ["Cine", "Deportes", "Series", "Videojuegos", "Libre"]


def menu_principal():
    reloj = pygame.time.Clock()

    indice_modo = 0
    indice_tematica = 0
    num_jugadores = 4
    num_impostores = 1
    palabra_libre = ""

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:

                # Salir
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                # Cambiar modo de juego
                if evento.key == pygame.K_RIGHT:
                    indice_modo = (indice_modo + 1) % len(MODOS)
                if evento.key == pygame.K_LEFT:
                    indice_modo = (indice_modo - 1) % len(MODOS)

                # Cambiar número de jugadores
                if evento.key == pygame.K_UP:
                    num_jugadores += 1
                if evento.key == pygame.K_DOWN and num_jugadores > 2:
                    num_jugadores -= 1

                # Cambiar número de impostores
                if evento.key == pygame.K_a:
                    if num_impostores < num_jugadores - 1:
                        num_impostores += 1
                if evento.key == pygame.K_z and num_impostores > 1:
                    num_impostores -= 1

                # Cambiar temática
                if evento.key == pygame.K_s:
                    indice_tematica = (indice_tematica + 1) % len(TEMATICAS)
                if evento.key == pygame.K_x:
                    indice_tematica = (indice_tematica - 1) % len(TEMATICAS)

                # Escribir palabra libre
                if TEMATICAS[indice_tematica] == "Libre":
                    if evento.key == pygame.K_BACKSPACE:
                        palabra_libre = palabra_libre[:-1]
                    else:
                        letra = evento.unicode
                        if letra.isprintable():
                            palabra_libre += letra

                # Iniciar partida
                if evento.key == pygame.K_RETURN:
                    config = {
                        "num_jugadores": num_jugadores,
                        "num_impostores": num_impostores,
                        "tiempo_ronda": MODOS[indice_modo][1],
                        "tematica": TEMATICAS[indice_tematica],
                        "palabra_libre": palabra_libre,
                    }

                    resultado = jugar_partida(ventana, config)

                    fuente = pygame.font.SysFont(None, 40)
                    mostrar_mensaje_centrado(
                        ventana,
                        fuente,
                        resultado,
                        (255, 255, 255),
                        (0, 0, 0),
                        3000,
                    )

        ventana.fill((20, 20, 20))
        dibujar_menu_principal(
            ventana,
            MODOS,
            indice_modo,
            num_jugadores,
            num_impostores,
            TEMATICAS,
            indice_tematica,
            palabra_libre,
        )

        pygame.display.flip()
        reloj.tick(60)


if __name__ == "__main__":
    menu_principal()
