import pygame
import random

pygame.init()
ANCHO, ALTO = 500, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Atrapa las monedas")
reloj = pygame.time.Clock()

try:
    img_moneda = pygame.image.load("moneda.jpg")
    img_moneda = pygame.transform.scale(img_moneda, (20, 20))
    img_powerup = pygame.image.load("powerup.png")
    img_powerup = pygame.transform.scale(img_powerup, (20, 20))
    usar_imagenes = True
except:
    usar_imagenes = False

jugador = pygame.Rect(220, 550, 60, 20)
velocidad = 10

monedas = []
powerups = []

vel_caida = 1
monedas_atrapadas = 0
fallos = 0
max_fallos = 3
jugando = True
nivel_actual = 0

NEGRO = (0, 0, 0)
DORADO = (255, 215, 0)
VERDE = (0, 255, 0)
AZUL = (0, 120, 255)
fuente = pygame.font.SysFont("Arial", 24)

while jugando:
    pantalla.fill(NEGRO)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and jugador.left > 0:
        jugador.x -= velocidad
    if teclas[pygame.K_RIGHT] and jugador.right < ANCHO:
        jugador.x += velocidad

    # Generar monedas aleatorias
    if random.random() < 0.02:
        nueva_moneda = pygame.Rect(random.randint(0, ANCHO - 20), -20, 20, 20)
        monedas.append(nueva_moneda)

    # Generar power-ups aleatorios
    if random.random() < 0.005:
        nuevo_powerup = pygame.Rect(random.randint(0, ANCHO - 20), -20, 20, 20)
        powerups.append(nuevo_powerup)

    # Mover monedas
    for moneda in monedas[:]:
        moneda.y += vel_caida
        if moneda.y > ALTO:
            monedas.remove(moneda)
            fallos += 1
        elif jugador.colliderect(moneda):
            monedas.remove(moneda)
            monedas_atrapadas += 1

            # Aumentar tamaño por cada 20 monedas
            nuevo_nivel = monedas_atrapadas // 20
            if nuevo_nivel > nivel_actual:
                nivel_actual = nuevo_nivel
                jugador.width += 20
                jugador = pygame.Rect(jugador.x, jugador.y, jugador.width, jugador.height)

    # Mover power-ups
    for powerup in powerups[:]:
        powerup.y += vel_caida
        if powerup.y > ALTO:
            powerups.remove(powerup)
        elif jugador.colliderect(powerup):
            powerups.remove(powerup)
            # Efecto del power-up: agrandar barra
            if jugador.width < 200:
                jugador.width += 30
                jugador = pygame.Rect(jugador.x, jugador.y, jugador.width, jugador.height)

    # Dibujar jugador
    pygame.draw.rect(pantalla, AZUL, jugador)

    # Dibujar monedas
    for moneda in monedas:
        if usar_imagenes:
            pantalla.blit(img_moneda, moneda)
        else:
            pygame.draw.ellipse(pantalla, DORADO, moneda)

    # Dibujar power-ups
    for powerup in powerups:
        if usar_imagenes:
            pantalla.blit(img_powerup, powerup)
        else:
            pygame.draw.rect(pantalla, VERDE, powerup)

    # Mostrar texto
    texto = fuente.render(f"Atrapadas: {monedas_atrapadas}   Fallos: {fallos}", True, (255, 255, 255))
    pantalla.blit(texto, (10, 10))

    # Game Over
    if fallos >= max_fallos:
        texto_final = fuente.render("¡Game Over! Presiona R para reiniciar", True, (255, 0, 0))
        pantalla.blit(texto_final, (40, 300))
        pygame.display.flip()

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_r]:
            monedas_atrapadas = 0
            fallos = 0
            jugador = pygame.Rect(220, 550, 60, 20)
            monedas.clear()
            powerups.clear()
            vel_caida = 1
            nivel_actual = 0
        continue

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
