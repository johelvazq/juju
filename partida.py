import pygame
import random
from graficos import (
    dibujar_pantalla_palabra,
    dibujar_pantalla_ronda,
    dibujar_pantalla_votacion,
    mostrar_mensaje_centrado,
)

PALABRAS_TEMATICAS = {
    "Cine": [("Matrix", "Película de ciencia ficción"), ("Titanic", "Barco y romance")],
    "Deportes": [("Fútbol", "Balón y once jugadores"), ("Tenis", "Raqueta y pista")],
    "Series": [("Breaking Bad", "Profesor de química"), ("Friends", "Grupo en Nueva York")],
    "Videojuegos": [("Minecraft", "Bloques y construcción"), ("Mario", "Fontanero italiano")],
}


def seleccionar_palabra(tematica, palabra_libre):
    if tematica == "Libre":
        palabra = palabra_libre if palabra_libre.strip() else "PALABRA"
        pista = "Pista libre"
        return palabra, pista

    lista = PALABRAS_TEMATICAS.get(tematica, [])
    if not lista:
        return "PALABRA", "Pista genérica"
    return random.choice(lista)


def asignar_impostores(num_jugadores, num_impostores):
    indices = list(range(num_jugadores))
    random.shuffle(indices)
    return set(indices[:num_impostores])


def mostrar_palabras_a_jugadores(ventana, num_jugadores, impostores, palabra, pista):
    reloj = pygame.time.Clock()
    jugador_actual = 0
    mostrando = True

    while mostrando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                jugador_actual += 1
                if jugador_actual >= num_jugadores:
                    mostrando = False

        if jugador_actual < num_jugadores:
            es_impostor = jugador_actual in impostores
            dibujar_pantalla_palabra(ventana, jugador_actual, es_impostor, palabra, pista)
            pygame.display.flip()

        reloj.tick(60)

    return True


def jugar_ronda(ventana, tiempo_ronda):
    reloj = pygame.time.Clock()
    inicio = pygame.time.get_ticks()
    votacion_anticipada = False
    corriendo = True

    while corriendo:
        ahora = pygame.time.get_ticks()
        tiempo_restante = tiempo_ronda - (ahora - inicio) / 1000

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False, True
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_v:
                    votacion_anticipada = True
                    corriendo = False

        if tiempo_restante <= 0:
            corriendo = False

        dibujar_pantalla_ronda(ventana, max(0, tiempo_restante))
        pygame.display.flip()
        reloj.tick(60)

    return True, votacion_anticipada


def fase_votacion(ventana, num_jugadores):
    reloj = pygame.time.Clock()
    votos = {}
    jugador_que_vota = 0

    while jugador_que_vota < num_jugadores:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return None, True
            if evento.type == pygame.KEYDOWN:
                # teclas 1..9
                if pygame.K_1 <= evento.key <= pygame.K_9:
                    voto = evento.key - pygame.K_1  # 0-based
                    if 0 <= voto < num_jugadores:
                        votos[voto] = votos.get(voto, 0) + 1
                        jugador_que_vota += 1

        dibujar_pantalla_votacion(ventana, num_jugadores, votos, jugador_que_vota)
        pygame.display.flip()
        reloj.tick(60)

    expulsado = max(votos, key=votos.get)
    return expulsado, False


def comprobar_victoria(impostores, num_jugadores):
    num_impostores = len(impostores)
    num_civiles = num_jugadores - num_impostores

    if num_impostores == 0:
        return "Todos los impostores fueron expulsados. ¡Ganan los civiles!"
    if num_impostores >= num_civiles:
        return "Los impostores igualan o superan a los civiles. ¡Ganan los impostores!"
    return None


def jugar_partida(ventana, config):
    fuente = pygame.font.SysFont(None, 32)
    num_jugadores = config["num_jugadores"]
    num_impostores = config["num_impostores"]
    tiempo_ronda = config["tiempo_ronda"]

    impostores = asignar_impostores(num_jugadores, num_impostores)
    palabra, pista = seleccionar_palabra(config["tematica"], config["palabra_libre"])

    juego_terminado = False
    resultado_final = "Partida cancelada"

    while not juego_terminado:
        seguir = mostrar_palabras_a_jugadores(ventana, num_jugadores, impostores, palabra, pista)
        if not seguir:
            return "Partida cancelada"

        seguir, _ = jugar_ronda(ventana, tiempo_ronda)
        if not seguir:
            return "Partida cancelada"

        expulsado, cancelado = fase_votacion(ventana, num_jugadores)
        if cancelado or expulsado is None:
            return "Partida cancelada"

        if expulsado in impostores:
            impostores.remove(expulsado)
            mensaje = f"Jugador {expulsado + 1} era impostor"
        else:
            mensaje = f"Jugador {expulsado + 1} NO era impostor"

        mostrar_mensaje_centrado(
            ventana,
            fuente,
            mensaje,
            (255, 255, 255),
            (0, 0, 0),
            2000,
        )

        resultado = comprobar_victoria(impostores, num_jugadores)
        if resultado:
            resultado_final = resultado
            juego_terminado = True

    return resultado_final
