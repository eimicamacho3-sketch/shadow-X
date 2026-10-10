import pygame
import time
import random

pygame.init()

# ============================================================
# CONFIGURACIÓN
# ============================================================

ANCHO = 1270
alto_ventana = 680
dimensiones = (ANCHO, alto_ventana)

ventana = pygame.display.set_mode(dimensiones)
pygame.display.set_caption("Leon K")

clock = pygame.time.Clock()

# ============================================================
# FONDOS
# ============================================================

fondo1 = pygame.transform.scale(
    pygame.image.load("imagenes/escenario_cor.png").convert(),
    dimensiones
)

fondo2 = pygame.transform.scale(
    pygame.image.load("imagenes/escenario_cor (1).png").convert(),
    dimensiones
)

fondo3 = pygame.transform.scale(
    pygame.image.load("imagenes/fotograma2.png").convert(),
    dimensiones
)

fondo4 = pygame.transform.scale(
    pygame.image.load("imagenes/fograma_puente.png").convert(),
    dimensiones
)

fondo5 = pygame.transform.scale(
    pygame.image.load("imagenes/escenario_cor (1).png").convert(),
    dimensiones
)

fondo = [fondo1, fondo2, fondo3, fondo4]

# ============================================================
# FUENTES
# ============================================================

font_salud = pygame.font.SysFont("font", 30, bold=True)
fuente_titulo = pygame.font.SysFont("arial", 76, bold=True)
fuente_subtitulo = pygame.font.SysFont("arial", 38, bold=True)
fuente_texto = pygame.font.SysFont("arial", 27)
fuente_pequena = pygame.font.SysFont("arial", 21)

# ============================================================
# SONIDOS
# ============================================================

pygame.mixer.music.load("sonidos/soundtrack_1.mp3")
pygame.mixer.music.play(-1)

sonido_arma = pygame.mixer.Sound("sonidos/disparo.mp3")

# ============================================================
# COLORES DE LAS PANTALLAS
# ============================================================

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (50, 129, 168)
ROJO = (210, 50, 50)
VERDE = (70, 200, 100)
GRIS = (180, 180, 180)
DORADO = (255, 210, 70)

# ============================================================
# FUNCIONES DE INTERFAZ
# ============================================================

def dibujar_texto_centrado(texto, fuente, color, y):
    superficie_texto = fuente.render(texto, True, color)
    rectangulo = superficie_texto.get_rect(
        center=(ANCHO // 2, y)
    )
    ventana.blit(superficie_texto, rectangulo)


def dibujar_menu():
    ventana.blit(fondo1, (0, 0))

    capa = pygame.Surface(dimensiones, pygame.SRCALPHA)
    capa.fill((0, 0, 0, 175))
    ventana.blit(capa, (0, 0))

    dibujar_texto_centrado(
        "LEON K", fuente_titulo, DORADO, 175
    )

    dibujar_texto_centrado(
        "Aventura y supervivencia",
        fuente_subtitulo,
        BLANCO,
        245
    )

    dibujar_texto_centrado(
        "ENTER - Comenzar partida",
        fuente_texto,
        VERDE,
        370
    )

    dibujar_texto_centrado(
        "W - Saltar       A / D - Moverse",
        fuente_texto,
        BLANCO,
        425
    )

    dibujar_texto_centrado(
        "R - Disparar",
        fuente_texto,
        BLANCO,
        465
    )

    dibujar_texto_centrado(
        "ESC - Salir",
        fuente_pequena,
        GRIS,
        535
    )


def dibujar_game_over():
    ventana.blit(fondo[numeroFondo], (0, 0))

    capa = pygame.Surface(dimensiones, pygame.SRCALPHA)
    capa.fill((0, 0, 0, 205))
    ventana.blit(capa, (0, 0))

    dibujar_texto_centrado(
        "GAME OVER",
        fuente_titulo,
        ROJO,
        220
    )

    dibujar_texto_centrado(
        "Leon K se ha quedado sin vida",
        fuente_subtitulo,
        BLANCO,
        310
    )

    dibujar_texto_centrado(
        "ENTER - Volver a jugar",
        fuente_texto,
        VERDE,
        410
    )

    dibujar_texto_centrado(
        "ESC - Salir",
        fuente_texto,
        BLANCO,
        460
    )


def dibujar_nivel_completado():
    ventana.blit(fondo[numeroFondo], (0, 0))

    capa = pygame.Surface(dimensiones, pygame.SRCALPHA)
    capa.fill((0, 0, 0, 195))
    ventana.blit(capa, (0, 0))

    dibujar_texto_centrado(
        "¡NIVEL COMPLETADO!",
        fuente_titulo,
        DORADO,
        230
    )

    dibujar_texto_centrado(
        "Leon K ha llegado a la puerta",
        fuente_subtitulo,
        BLANCO,
        320
    )

    dibujar_texto_centrado(
        "Has derrotado a Enemy 4",
        fuente_texto,
        VERDE,
        385
    )

    dibujar_texto_centrado(
        "ENTER - Volver al menú",
        fuente_texto,
        BLANCO,
        465
    )

    dibujar_texto_centrado(
        "ESC - Salir",
        fuente_pequena,
        GRIS,
        515
    )


# ============================================================
# CLASE PLAYER
# ============================================================

class player():

    def __init__(
        self,
        x,
        y,
        w,
        h,
        vide,
        image_path,
        animacion_salto=False
    ):

        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image_path = image_path

        self.vida = 100

        # IMAGEN PRINCIPAL

        self.image = pygame.transform.scale(
            pygame.image.load(
                self.image_path
            ).convert_alpha(),
            (w, h)
        )

        self.rect = self.image.get_rect(topleft=(x, y))

        # FÍSICA

        self.vel_y = 0
        self.en_suelo = True
        self.y_suelo = y

        # DIRECCIÓN

        self.direccion = "derecha"

        # ANIMACIÓN DE SALTO

        self.animacion_salto = animacion_salto

        self.frame_inicio_salto = None
        self.frame_ascenso = None
        self.frame_aterrizaje = None

        self.frame_inicio_salto_derecha = None
        self.frame_ascenso_derecha = None
        self.frame_aterrizaje_derecha = None

        self.frame_inicio_salto_izquierda = None
        self.frame_ascenso_izquierda = None
        self.frame_aterrizaje_izquierda = None

        self.frame_salto_actual = self.image

        self.tiempo_inicio_salto = 0
        self.tiempo_aterrizaje = 0

        # CARGAR ANIMACIÓN DE SALTO

        if self.animacion_salto:

            self.frame_inicio_salto = self.cargar_frame(
                "imagenes/start jump.png"
            )

            self.frame_ascenso = self.cargar_frame(
                "imagenes/ascent.png"
            )

            self.frame_aterrizaje = self.cargar_frame(
                "imagenes/aterrizaje.png"
            )

            self.frame_inicio_salto_derecha = (
                self.frame_inicio_salto
            )

            self.frame_ascenso_derecha = (
                self.frame_ascenso
            )

            self.frame_aterrizaje_derecha = (
                self.frame_aterrizaje
            )

            self.frame_inicio_salto_izquierda = (
                pygame.transform.flip(
                    self.frame_inicio_salto, True, False
                )
            )

            self.frame_ascenso_izquierda = (
                pygame.transform.flip(
                    self.frame_ascenso, True, False
                )
            )

            self.frame_aterrizaje_izquierda = (
                pygame.transform.flip(
                    self.frame_aterrizaje, True, False
                )
            )

    # ========================================================
    # CARGAR FRAME
    # ========================================================

    def cargar_frame(self, ruta):

        imagen = pygame.image.load(ruta).convert_alpha()

        escala = min(
            self.w / imagen.get_width(),
            self.h / imagen.get_height()
        )

        nuevo_ancho = int(imagen.get_width() * escala)
        nuevo_alto = int(imagen.get_height() * escala)

        imagen = pygame.transform.smoothscale(
            imagen,
            (nuevo_ancho, nuevo_alto)
        )

        return imagen

    # ========================================================
    # ANIMACIÓN DE SALTO
    # ========================================================

    def actualizar_animacion_salto(self):

        if not self.animacion_salto:
            return

        tiempo_actual = pygame.time.get_ticks()

        if self.direccion == "derecha":

            frame_inicio = self.frame_inicio_salto_derecha
            frame_ascenso = self.frame_ascenso_derecha
            frame_aterrizaje = self.frame_aterrizaje_derecha

        else:

            frame_inicio = self.frame_inicio_salto_izquierda
            frame_ascenso = self.frame_ascenso_izquierda
            frame_aterrizaje = self.frame_aterrizaje_izquierda

        # ATERRIZAJE

        if self.tiempo_aterrizaje > tiempo_actual:
            self.frame_salto_actual = frame_aterrizaje
            return

        # EN EL AIRE

        if not self.en_suelo:

            tiempo_salto = (
                tiempo_actual - self.tiempo_inicio_salto
            )

            if tiempo_salto < 120:
                self.frame_salto_actual = frame_inicio

            elif self.vel_y < 0:
                self.frame_salto_actual = frame_ascenso

            else:
                self.frame_salto_actual = frame_aterrizaje

        else:
            self.frame_salto_actual = self.image

    # ========================================================
    # DIBUJAR PLAYER
    # ========================================================

    def draw(self, camara_x=0):

        if self.animacion_salto:

            self.actualizar_animacion_salto()

            imagen = self.frame_salto_actual

            draw_x = (
                self.rect.x - camara_x
                + (self.rect.width - imagen.get_width()) // 2
            )

            draw_y = (
                self.rect.y
                + self.rect.height
                - imagen.get_height()
            )

            ventana.blit(imagen, (draw_x, draw_y))

        else:

            ventana.blit(
                self.image,
                (self.rect.x - camara_x, self.rect.y)
            )


# ============================================================
# CLASE ENEMIGO
# ============================================================

class enemy(player):

    def __init__(
        self,
        salud,
        habilidad,
        daño,
        x,
        y,
        w,
        h,
        vide,
        image_path
    ):

        super().__init__(
            x, y, w, h, vide, image_path,
            animacion_salto=False
        )

        self.salud = salud
        self.habilidad = habilidad
        self.daño = daño

        self.espera = 4000
        self.tiempo_rociar = 0

    # ATAQUE

    def rociar(self, jugador):

        tiempo_actual = pygame.time.get_ticks()

        if jugador.vida > 0:

            if tiempo_actual - self.tiempo_rociar >= self.espera:

                jugador.vida -= self.daño

                self.tiempo_rociar = pygame.time.get_ticks()

    # PERSEGUIR

    def perseguir(self, jugador):

        distancia = (
            self.rect.centerx - jugador.rect.centerx
        )

        velocidad_enemigo = 3

        if distancia > 50:
            self.rect.x -= velocidad_enemigo

        elif distancia < -50:
            self.rect.x += velocidad_enemigo

        if abs(distancia) <= 80:
            self.rociar(jugador)


# ============================================================
# CLASE NUBE
# ============================================================

class Nube:

    def __init__(self, x, y, escala, velocidad):

        self.x = x
        self.y = y
        self.escala = escala
        self.velocidad = velocidad

        ancho = int(230 * escala)
        alto = int(100 * escala)

        self.surface = pygame.Surface(
            (ancho, alto),
            pygame.SRCALPHA
        )

        color = (255, 255, 255, 100)

        pygame.draw.ellipse(
            self.surface,
            color,
            (
                0,
                int(35 * escala),
                int(130 * escala),
                int(45 * escala)
            )
        )

        pygame.draw.ellipse(
            self.surface,
            color,
            (
                int(45 * escala),
                int(10 * escala),
                int(100 * escala),
                int(65 * escala)
            )
        )

        pygame.draw.ellipse(
            self.surface,
            color,
            (
                int(100 * escala),
                int(25 * escala),
                int(110 * escala),
                int(55 * escala)
            )
        )

    def actualizar(self):

        self.x -= self.velocidad

        if self.x < -self.surface.get_width():

            self.x = ANCHO + random.randint(50, 300)
            self.y = random.randint(30, 250)

    def draw(self):

        ventana.blit(
            self.surface,
            (int(self.x), int(self.y))
        )


# ============================================================
# CLASE NIEVE
# ============================================================

class ParticulaNieve:

    def __init__(self):

        self.reiniciar(
            random.randint(-100, ANCHO + 100),
            random.randint(-alto_ventana, alto_ventana)
        )

    def reiniciar(self, x=None, y=None):

        if x is None:
            self.x = random.randint(-100, ANCHO + 100)
        else:
            self.x = x

        if y is None:
            self.y = random.randint(-100, 0)
        else:
            self.y = y

        self.vel_x = random.uniform(0.7, 2.0)
        self.vel_y = random.uniform(2.0, 5.0)

        self.tamano = random.randint(1, 3)
        self.largo = random.randint(2, 6)
        self.alpha = random.randint(130, 230)

    def actualizar(self):

        self.x += self.vel_x
        self.y += self.vel_y

        if (
            self.y > alto_ventana + 10
            or self.x > ANCHO + 20
        ):

            self.reiniciar(
                random.randint(-120, ANCHO),
                random.randint(-80, -10)
            )

    def draw(self):

        copo = pygame.Surface(
            (self.largo + 6, self.largo + 6),
            pygame.SRCALPHA
        )

        pygame.draw.line(
            copo,
            (255, 255, 255, self.alpha),
            (1, 1),
            (self.largo + 2, self.largo + 2),
            self.tamano
        )

        ventana.blit(copo, (int(self.x), int(self.y)))


# ============================================================
# PARTÍCULAS DE IMPACTO
# ============================================================

class ParticulaImpacto:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        angulo = random.uniform(0, 2 * 3.14159)
        velocidad_particula = random.uniform(2, 7)

        self.vel_x = (
            pygame.math.Vector2(1, 0).rotate(
                angulo * 180 / 3.14159
            ).x * velocidad_particula
        )

        self.vel_y = (
            pygame.math.Vector2(1, 0).rotate(
                angulo * 180 / 3.14159
            ).y * velocidad_particula
        )

        self.vida = random.randint(15, 30)
        self.radio = random.randint(2, 5)

        self.color = random.choice([
            (255, 60, 60),
            (255, 130, 30),
            (255, 220, 80),
            (255, 255, 255)
        ])

    def actualizar(self):

        self.x += self.vel_x
        self.y += self.vel_y

        self.vel_y += 0.2
        self.vida -= 1

    def draw(self):

        if self.vida > 0:

            pygame.draw.circle(
                ventana,
                self.color,
                (int(self.x), int(self.y)),
                self.radio
            )


# ============================================================
# CREAR NIEVE
# ============================================================

particulas_nieve = [
    ParticulaNieve()
    for _ in range(140)
]

# ============================================================
# PERSONAJE PRINCIPAL
# ============================================================

personaje_principal = player(
    500, 280, 250, 200, 5,
    "imagenes/personaje principal 1.png",
    animacion_salto=True
)

# ============================================================
# ENEMIGOS
# ============================================================

enemy1 = enemy(
    500, "rociar", 20,
    300, 280, 100, 200, 100,
    "imagenes/recortes/lysolito(2.0).png"
)

enemy2 = enemy(
    500, "rociar", 20,
    200, 300, 100, 200, 100,
    "imagenes/recortes/zombie_girl.png"
)

enemy3 = enemy(
    500, "rociar", 20,
    100, 300, 100, 200, 100,
    "imagenes/recortes/chef_enemy.png"
)

enemy4 = enemy(
    500, "rociar", 20,
    80, 300, 100, 200, 100,
    "imagenes/recortes/lysolito(2.0).png"
)

# ============================================================
# HUD
# ============================================================

foto_perfil = player(
    25, 25, 100, 100, 5,
    "imagenes/recortes/foto_personaje.png",
    animacion_salto=False
)

vida = player(
    150, 90, 180, 50, 5,
    "imagenes/recortes/vida(1).png",
    animacion_salto=False
)

# ============================================================
# BALA
# ============================================================

bala = player(
    1500, 100, 30, 30, 30,
    "imagenes/recortes/bala(1).png",
    animacion_salto=False
)

# ============================================================
# NUBES
# ============================================================

nubes = [
    Nube(100, 80, 0.8, 0.5),
    Nube(500, 150, 1.2, 0.8),
    Nube(900, 60, 0.7, 0.4),
    Nube(1200, 210, 1.0, 0.6),
    Nube(1500, 100, 1.4, 0.7),
    Nube(1800, 180, 0.9, 0.5),
    Nube(2200, 70, 1.1, 0.6)
]

# ============================================================
# VARIABLES DEL JUEGO
# ============================================================

velocidad = 5
gravedad = 1
fuerza_salto = -30
disparo = 10
bala_velocidad = disparo
disparando = False

# Enemy 4 NO se dibuja ni se activa en el primer escenario.

enemys = [enemy1, enemy2, enemy3]
enemigos_activos = [enemy1]

cont_e = 4
fase_enemigos = 1
escenario_actual = 1

listo_para_segundo_escenario = False
enemy4_derrotado = False

estado_transicion = None
alpha_transicion = 0
numeroFondo = 0

superficie = pygame.Surface(dimensiones)
superficie.fill(NEGRO)
superficie.set_alpha(0)

ANCHO_MUNDO = 6350
camara_x = 0

# ============================================================
# PUERTA DEL SEGUNDO ESCENARIO
# ============================================================

puerta_rect = pygame.Rect(
    ANCHO - 160,
    270,
    90,
    180
)

# ============================================================
# ESTADO DE LAS PANTALLAS
# ============================================================

# menu
# jugando
# game_over
# nivel_completado

estado_pantalla = "menu"

# ============================================================
# REINICIAR PARTIDA
# ============================================================

def reiniciar_partida():

    global enemys
    global enemigos_activos
    global cont_e
    global fase_enemigos
    global escenario_actual
    global listo_para_segundo_escenario
    global enemy4_derrotado
    global estado_transicion
    global alpha_transicion
    global numeroFondo
    global disparando
    global bala
    global bala_velocidad
    global camara_x
    global particulas_impacto
    global puerta_rect
    global vida
    global estado_pantalla

    personaje_principal.rect.x = 500
    personaje_principal.rect.y = 280
    personaje_principal.vida = 100
    personaje_principal.vel_y = 0
    personaje_principal.en_suelo = True
    personaje_principal.direccion = "derecha"
    personaje_principal.tiempo_aterrizaje = 0

    enemy1.rect.x = 300
    enemy1.rect.y = 280
    enemy1.salud = 500
    enemy1.tiempo_rociar = pygame.time.get_ticks()

    enemy2.rect.x = 200
    enemy2.rect.y = 300
    enemy2.salud = 500
    enemy2.tiempo_rociar = pygame.time.get_ticks()

    enemy3.rect.x = 100
    enemy3.rect.y = 300
    enemy3.salud = 500
    enemy3.tiempo_rociar = pygame.time.get_ticks()

    enemy4.rect.x = 850
    enemy4.rect.y = 300
    enemy4.salud = 500
    enemy4.tiempo_rociar = pygame.time.get_ticks()

    enemys = [enemy1, enemy2, enemy3]
    enemigos_activos = [enemy1]

    cont_e = 4
    fase_enemigos = 1
    escenario_actual = 1

    listo_para_segundo_escenario = False
    enemy4_derrotado = False

    estado_transicion = None
    alpha_transicion = 0
    numeroFondo = 0

    disparando = False
    bala = player(
        1500, 100, 30, 30, 30,
        "imagenes/recortes/bala(1).png",
        False
    )

    bala_velocidad = disparo
    camara_x = 0

    particulas_impacto = []

    puerta_rect = pygame.Rect(
        ANCHO - 160, 270, 90, 180
    )

    vida = player(
        150, 90, 180, 50, 5,
        "imagenes/recortes/vida(1).png",
        False
    )

    estado_pantalla = "jugando"


# ============================================================
# LISTA DE PARTÍCULAS DE IMPACTO
# ============================================================

particulas_impacto = []

# ============================================================
# BUCLE PRINCIPAL
# ============================================================

salir = False

while not salir:

    clock.tick(60)

    # ========================================================
    # EVENTOS
    # ========================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            salir = True

        if event.type == pygame.KEYDOWN:

            # -----------------------------------------------
            # MENÚ PRINCIPAL
            # -----------------------------------------------

            if estado_pantalla == "menu":

                if event.key == pygame.K_RETURN:
                    reiniciar_partida()

                elif event.key == pygame.K_ESCAPE:
                    salir = True

            # -----------------------------------------------
            # GAME OVER
            # -----------------------------------------------

            elif estado_pantalla == "game_over":

                if event.key == pygame.K_RETURN:
                    reiniciar_partida()

                elif event.key == pygame.K_ESCAPE:
                    salir = True

            # -----------------------------------------------
            # NIVEL COMPLETADO
            # -----------------------------------------------

            elif estado_pantalla == "nivel_completado":

                if event.key == pygame.K_RETURN:
                    estado_pantalla = "menu"

                elif event.key == pygame.K_ESCAPE:
                    salir = True

            # -----------------------------------------------
            # CONTROLES DURANTE LA PARTIDA
            # -----------------------------------------------

            elif estado_pantalla == "jugando":

                # SALTO

                if (
                    event.key == pygame.K_w
                    and personaje_principal.en_suelo
                ):

                    teclas_salto = pygame.key.get_pressed()

                    if (
                        teclas_salto[pygame.K_d]
                        and not teclas_salto[pygame.K_a]
                    ):
                        personaje_principal.direccion = "derecha"

                    elif (
                        teclas_salto[pygame.K_a]
                        and not teclas_salto[pygame.K_d]
                    ):
                        personaje_principal.direccion = "izquierda"

                    personaje_principal.vel_y = fuerza_salto
                    personaje_principal.en_suelo = False

                    personaje_principal.tiempo_inicio_salto = (
                        pygame.time.get_ticks()
                    )

                # DISPARO

                if event.key == pygame.K_r:

                    teclas_disparo = pygame.key.get_pressed()

                    if (
                        teclas_disparo[pygame.K_d]
                        and not teclas_disparo[pygame.K_a]
                    ):
                        personaje_principal.direccion = "derecha"

                    elif (
                        teclas_disparo[pygame.K_a]
                        and not teclas_disparo[pygame.K_d]
                    ):
                        personaje_principal.direccion = "izquierda"

                    sonido_arma.play()

                    bala_x = (
                        personaje_principal.rect.centerx - 35
                    )

                    bala_y = (
                        personaje_principal.rect.centery - 35
                    )

                    if personaje_principal.direccion == "izquierda":
                        bala_velocidad = -disparo
                    else:
                        bala_velocidad = disparo

                    bala = player(
                        bala_x,
                        bala_y,
                        70,
                        70,
                        40,
                        "imagenes/recortes/bala(1).png",
                        False
                    )

                    if personaje_principal.direccion == "izquierda":

                        bala.image = pygame.transform.flip(
                            bala.image,
                            True,
                            False
                        )

                    disparando = True

    # ========================================================
    # MOSTRAR MENÚ Y NO EJECUTAR LA PARTIDA
    # ========================================================

    if estado_pantalla == "menu":

        dibujar_menu()
        pygame.display.flip()
        continue

    # ========================================================
    # MOSTRAR GAME OVER
    # ========================================================

    if estado_pantalla == "game_over":

        dibujar_game_over()
        pygame.display.flip()
        continue

    # ========================================================
    # MOSTRAR NIVEL COMPLETADO
    # ========================================================

    if estado_pantalla == "nivel_completado":

        dibujar_nivel_completado()
        pygame.display.flip()
        continue

    # ========================================================
    # COMPROBAR SI LEON PERDIÓ TODA SU VIDA
    # ========================================================

    if personaje_principal.vida <= 0:

        personaje_principal.vida = 0
        estado_pantalla = "game_over"

        continue

    # ========================================================
    # DIBUJAR FONDO
    # ========================================================

    ventana.blit(fondo[numeroFondo], (0, 0))

    # ========================================================
    # NUBES
    # ========================================================

    for nube in nubes:

        nube.actualizar()
        nube.draw()

    # ========================================================
    # NIEVE
    # ========================================================

    for particula in particulas_nieve:

        particula.actualizar()
        particula.draw()

    # ========================================================
    # DIBUJAR PUERTA EN EL SEGUNDO ESCENARIO
    # ========================================================

    if escenario_actual == 2:

        # Marco de la puerta

        pygame.draw.rect(
            ventana,
            (90, 50, 25),
            puerta_rect
        )

        # Interior

        pygame.draw.rect(
            ventana,
            (40, 25, 20),
            (
                puerta_rect.x + 10,
                puerta_rect.y + 10,
                puerta_rect.width - 20,
                puerta_rect.height - 10
            )
        )

        # Brillo de la puerta

        pygame.draw.rect(
            ventana,
            DORADO,
            (
                puerta_rect.x + 10,
                puerta_rect.y + 10,
                puerta_rect.width - 20,
                puerta_rect.height - 10
            ),
            3
        )

        # Perilla

        pygame.draw.circle(
            ventana,
            DORADO,
            (
                puerta_rect.right - 22,
                puerta_rect.centery
            ),
            5
        )

        # Indicaciones para el jugador

        if enemy4_derrotado:

            mensaje_puerta = fuente_pequena.render(
                "¡Ve a la puerta!",
                True,
                VERDE
            )

            ventana.blit(
                mensaje_puerta,
                (
                    puerta_rect.x - 65,
                    puerta_rect.y - 35
                )
            )

        else:

            mensaje_puerta = fuente_pequena.render(
                "Derrota a Enemy 4",
                True,
                BLANCO
            )

            ventana.blit(
                mensaje_puerta,
                (
                    puerta_rect.x - 90,
                    puerta_rect.y - 35
                )
            )

    # ========================================================
    # VIDA DEL PERSONAJE
    # ========================================================

    salud_txt = font_salud.render(
        f"Leon K: {personaje_principal.vida}",
        True,
        AZUL
    )

    ventana.blit(salud_txt, (150, 50))

    # ========================================================
    # BARRA DE VIDA
    # ========================================================

    if personaje_principal.vida > 80:

        ruta_vida = "imagenes/recortes/vida(1).png"

    elif personaje_principal.vida > 60:

        ruta_vida = "imagenes/recortes/vida(2).png"

    elif personaje_principal.vida > 40:

        ruta_vida = "imagenes/recortes/vida(3).png"

    elif personaje_principal.vida > 20:

        ruta_vida = "imagenes/recortes/vida(4).png"

    elif personaje_principal.vida > 0:

        ruta_vida = "imagenes/recortes/vida(5).png"

    else:

        ruta_vida = "imagenes/recortes/vida(6).png"

    vida = player(
        150, 90, 180, 50, 5,
        ruta_vida,
        False
    )

    # ========================================================
    # MOVER BALA
    # ========================================================

    if disparando:

        bala.rect.x += bala_velocidad

    # ========================================================
    # COLISIÓN DE BALA CON ENEMIGOS
    # ========================================================

    if disparando:

        for enemigo in enemigos_activos[:]:

            if bala.rect.colliderect(enemigo.rect):

                enemigo.salud -= 100

                print(
                    "Vida del enemigo:",
                    enemigo.salud
                )

                # CREAR PARTÍCULAS EN EL IMPACTO

                for _ in range(18):

                    particulas_impacto.append(
                        ParticulaImpacto(
                            enemigo.rect.centerx,
                            enemigo.rect.centery
                        )
                    )

                disparando = False
                bala.rect.x = 1900
                bala.rect.y = 300

                # ENEMIGO DERROTADO

                if enemigo.salud <= 0:

                    if enemigo in enemys:
                        enemys.remove(enemigo)

                    if enemigo in enemigos_activos:
                        enemigos_activos.remove(enemigo)

                    cont_e -= 1

                    # ---------------------------------------
                    # ENEMY 1 DERROTADO
                    # ---------------------------------------

                    if enemigo is enemy1:

                        fase_enemigos = 2

                        enemigos_activos = [
                            enemigo_restante
                            for enemigo_restante in [enemy2, enemy3]
                            if enemigo_restante in enemys
                        ]

                        print("Enemy 1 derrotado.")
                        print("Enemy 2 y Enemy 3 activados.")

                    # ---------------------------------------
                    # ENEMY 2 Y ENEMY 3 DERROTADOS
                    # ---------------------------------------

                    elif (
                        fase_enemigos == 2
                        and enemy2 not in enemigos_activos
                        and enemy3 not in enemigos_activos
                    ):

                        fase_enemigos = 3

                        enemigos_activos = []

                        listo_para_segundo_escenario = True

                        print("Enemy 2 y Enemy 3 derrotados.")
                        print("Leon puede avanzar al segundo escenario.")

                    # ---------------------------------------
                    # ENEMY 4 DERROTADO
                    # ---------------------------------------

                    elif enemigo is enemy4:

                        fase_enemigos = 4
                        enemigos_activos = []
                        enemy4_derrotado = True

                        print("Enemy 4 derrotado.")
                        print("Leon puede dirigirse a la puerta.")

                break

    # ========================================================
    # COMENZAR TRANSICIÓN AL SEGUNDO ESCENARIO
    # ========================================================

    if (
        escenario_actual == 1
        and listo_para_segundo_escenario
        and personaje_principal.rect.right >= ANCHO - 100
        and estado_transicion is None
    ):

        estado_transicion = "oscureciendo"
        alpha_transicion = 0

        print("Leon llegó al final del primer escenario.")
        print("Iniciando transición...")

    # ========================================================
    # OSCURECER PANTALLA
    # ========================================================

    if estado_transicion == "oscureciendo":

        alpha_transicion += 10

        if alpha_transicion >= 255:

            alpha_transicion = 255

            # CAMBIAR ESCENARIO

            numeroFondo = 1
            escenario_actual = 2

            # COLOCAR LEON AL INICIO

            personaje_principal.rect.x = 50
            personaje_principal.rect.y = (
                personaje_principal.y_suelo
            )

            personaje_principal.vel_y = 0
            personaje_principal.en_suelo = True
            personaje_principal.direccion = "derecha"

            # ACTIVAR ENEMY 4 SOLAMENTE EN EL ESCENARIO 2

            fase_enemigos = 3
            listo_para_segundo_escenario = False

            enemy4.rect.x = 850
            enemy4.rect.y = 300
            enemy4.salud = 500
            enemy4.vida = 100
            enemy4.tiempo_rociar = pygame.time.get_ticks()

            if enemy4 not in enemys:
                enemys.append(enemy4)

            enemigos_activos = [enemy4]

            enemy4_derrotado = False

            # EMPEZAR A ACLARAR

            estado_transicion = "aclarando"

            print("Segundo escenario cargado.")
            print("Enemy 4 activado.")

    # ========================================================
    # ACLARAR PANTALLA
    # ========================================================

    elif estado_transicion == "aclarando":

        alpha_transicion -= 10

        if alpha_transicion <= 0:

            alpha_transicion = 0
            estado_transicion = None

            print("Transición terminada.")
            print("Leon puede seguir avanzando.")

    # ========================================================
    # TECLAS MANTENIDAS
    # ========================================================

    teclas = pygame.key.get_pressed()

    # ========================================================
    # MOVER DERECHA
    # ========================================================

    if teclas[pygame.K_d]:

        personaje_principal.direccion = "derecha"
        personaje_principal.rect.x += velocidad

        if not hasattr(personaje_principal, "imagen_derecha"):

            personaje_principal.imagen_derecha = (
                pygame.transform.scale(
                    pygame.image.load(
                        "imagenes/personaje principal 1.png"
                    ).convert_alpha(),
                    (
                        personaje_principal.w,
                        personaje_principal.h
                    )
                )
            )

        personaje_principal.image = (
            personaje_principal.imagen_derecha
        )

    # ========================================================
    # MOVER IZQUIERDA
    # ========================================================

    if teclas[pygame.K_a]:

        personaje_principal.direccion = "izquierda"
        personaje_principal.rect.x -= velocidad

        if not hasattr(personaje_principal, "imagen_izquierda"):

            personaje_principal.imagen_izquierda = (
                pygame.transform.scale(
                    pygame.image.load(
                        "imagenes/personaje.princp.left.png"
                    ).convert_alpha(),
                    (
                        personaje_principal.w,
                        personaje_principal.h
                    )
                )
            )

        personaje_principal.image = (
            personaje_principal.imagen_izquierda
        )

    # ========================================================
    # LIMITAR AL MUNDO
    # ========================================================

    if personaje_principal.rect.x < 0:
        personaje_principal.rect.x = 0

    if personaje_principal.rect.x > ANCHO_MUNDO - 50:

        personaje_principal.rect.x = ANCHO_MUNDO - 50

    # ========================================================
    # GRAVEDAD
    # ========================================================

    personaje_principal.vel_y += gravedad

    personaje_principal.rect.y += (
        personaje_principal.vel_y
    )

    # ========================================================
    # ATERRIZAJE
    # ========================================================

    if (
        personaje_principal.rect.y
        >= personaje_principal.y_suelo
    ):

        personaje_principal.rect.y = (
            personaje_principal.y_suelo
        )

        if not personaje_principal.en_suelo:

            personaje_principal.tiempo_aterrizaje = (
                pygame.time.get_ticks() + 150
            )

        personaje_principal.vel_y = 0
        personaje_principal.en_suelo = True

    # ========================================================
    # COMPROBAR SI LEON TOCA LA PUERTA
    # ========================================================

    if (
        escenario_actual == 2
        and enemy4_derrotado
        and personaje_principal.rect.colliderect(puerta_rect)
    ):

        estado_pantalla = "nivel_completado"

        print("¡Nivel completado!")
        print("Leon llegó a la puerta después de derrotar a Enemy 4.")

    # ========================================================
    # DIBUJAR PERSONAJE
    # ========================================================

    personaje_principal.draw(camara_x)

    # ========================================================
    # DIBUJAR HUD
    # ========================================================

    foto_perfil.draw()
    vida.draw()

    # ========================================================
    # DIBUJAR ENEMIGOS
    # ========================================================

    for enemigo in enemys:

        enemigo.draw(camara_x)

    # ========================================================
    # MOVER Y ATACAR ENEMIGOS ACTIVOS
    # ========================================================

    for enemigo in enemigos_activos[:]:

        if enemigo in enemys:
            enemigo.perseguir(personaje_principal)

    # ========================================================
    # ACTUALIZAR Y DIBUJAR PARTÍCULAS DE IMPACTO
    # ========================================================

    for particula in particulas_impacto[:]:

        particula.actualizar()
        particula.draw()

        if particula.vida <= 0:
            particulas_impacto.remove(particula)

    # ========================================================
    # DIBUJAR BALA
    # ========================================================

    if disparando:
        bala.draw(camara_x)

    # ========================================================
    # DIBUJAR TRANSICIÓN
    # ========================================================

    if estado_transicion is not None:

        superficie.set_alpha(alpha_transicion)

        ventana.blit(superficie, (0, 0))

    # ========================================================
    # ACTUALIZAR PANTALLA
    # ========================================================

    pygame.display.flip()

# ============================================================
# CERRAR PYGAME
# ============================================================

pygame.quit()