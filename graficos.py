import pygame


def dibujar_texto(surface, texto, fuente, color, x, y):
    img = fuente.render(texto, True, color)
    rect = img.get_rect(topleft=(x, y))
    surface.blit(img, rect)
    return rect


def mostrar_mensaje_centrado(surface, fuente, texto, color_texto, color_fondo, tiempo_ms=2000):
    clock = pygame.time.Clock()
    ancho, alto = surface.get_size()
    img = fuente.render(texto, True, color_texto)
    rect = img.get_rect(center=(ancho // 2, alto // 2))

    inicio = pygame.time.get_ticks()
    mostrando = True
    while mostrando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                mostrando = False

        surface.fill(color_fondo)
        surface.blit(img, rect)
        pygame.display.flip()

        if pygame.time.get_ticks() - inicio >= tiempo_ms:
            mostrando = False

        clock.tick(60)


def dibujar_menu_principal(
    surface,
    modos,
    indice_modo,
    num_jugadores,
    num_impostores,
    tematicas,
    indice_tematica,
    palabra_libre,
):
    ancho, alto = surface.get_size()
    fuente_titulo = pygame.font.SysFont(None, 52)
    fuente = pygame.font.SysFont(None, 28)

    dibujar_texto(surface, "MENÚ PRINCIPAL", fuente_titulo, (255, 255, 255), 40, 30)

    modo_nombre, modo_tiempo = modos[indice_modo]
    dibujar_texto(
        surface,
        f"Modo: {modo_nombre} ({modo_tiempo}s)  [←/→]",
        fuente,
        (220, 220, 220),
        40,
        120,
    )

    dibujar_texto(
        surface,
        f"Jugadores: {num_jugadores}  [↑/↓]",
        fuente,
        (220, 220, 220),
        40,
        160,
    )

    dibujar_texto(
        surface,
        f"Impostores: {num_impostores}  [A/Z]",
        fuente,
        (220, 220, 220),
        40,
        200,
    )

    dibujar_texto(
        surface,
        f"Temática: {tematicas[indice_tematica]}  [S/X]",
        fuente,
        (220, 220, 220),
        40,
        240,
    )

    if tematicas[indice_tematica] == "Libre":
        dibujar_texto(
            surface,
            f"Palabra libre: {palabra_libre}",
            fuente,
            (255, 255, 0),
            40,
            280,
        )

    dibujar_texto(
        surface,
        "ENTER: Iniciar partida",
        fuente,
        (0, 255, 0),
        40,
        alto - 90,
    )
    dibujar_texto(
        surface,
        "ESC: Salir",
        fuente,
        (255, 100, 100),
        40,
        alto - 60,
    )


def dibujar_pantalla_palabra(surface, jugador_actual, es_impostor, palabra, pista):
    surface.fill((10, 10, 40))
    fuente_titulo = pygame.font.SysFont(None, 46)
    fuente = pygame.font.SysFont(None, 30)

    dibujar_texto(
        surface,
        f"Turno del jugador {jugador_actual + 1}",
        fuente_titulo,
        (255, 255, 255),
        40,
        40,
    )

    if es_impostor:
        dibujar_texto(surface, "IMPOSTOR", fuente_titulo, (255, 60, 60), 40, 120)
        dibujar_texto(surface, f"Pista: {pista}", fuente, (255, 255, 0), 40, 180)
    else:
        dibujar_texto(surface, f"Palabra: {palabra}", fuente, (60, 255, 60), 40, 150)

    dibujar_texto(
        surface,
        "Pulsa ESPACIO para ocultar y pasar al siguiente",
        fuente,
        (220, 220, 220),
        40,
        260,
    )


def dibujar_pantalla_ronda(surface, tiempo_restante):
    surface.fill((0, 0, 0))
    fuente = pygame.font.SysFont(None, 40)
    dibujar_texto(
        surface,
        f"Tiempo restante: {int(tiempo_restante)} s",
        fuente,
        (255, 255, 255),
        40,
        40,
    )
    dibujar_texto(
        surface,
        "Pulsa V para votar ahora",
        fuente,
        (255, 255, 0),
        40,
        100,
    )


def dibujar_pantalla_votacion(surface, num_jugadores, votos_actuales, jugador_que_vota):
    surface.fill((40, 0, 0))
    fuente_titulo = pygame.font.SysFont(None, 40)
    fuente = pygame.font.SysFont(None, 28)

    dibujar_texto(
        surface,
        f"Votación - Turno del jugador {jugador_que_vota + 1}",
        fuente_titulo,
        (255, 255, 255),
        40,
        30,
    )

    y = 100
    for i in range(num_jugadores):
        dibujar_texto(
            surface,
            f"[{i + 1}] Jugador {i + 1} - votos: {votos_actuales.get(i, 0)}",
            fuente,
            (230, 230, 230),
            40,
            y,
        )
        y += 30

    dibujar_texto(
        surface,
        "Pulsa número (1..N) para votar",
        fuente,
        (255, 255, 0),
        40,
        y + 20,
    )
