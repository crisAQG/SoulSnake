from G5.Data.Modules.Scene.Scene import Scene
from G5.Data.Modules.Type.Entities import Player
from G5.Data.Modules.Services.MapGen import MapGen

import pygame


class Game(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.game = game

        self.fuente = game.font
        self.volver_txt = self.fuente.render("Presione [ESCAPE] para volver al menu.", True, (255, 255, 255))

        self.map = MapGen()
        self.tab = self.map.map

        pos_inicial = self.map.gen_object(1)[0]  # coloca al jugador y devuelve (col, fila)
        self.pos_logica = pos_inicial

        # Calculamos la posición en píxeles para que pos_visual empiece ya centrada
        px_inicial = pos_inicial[0] * 32
        py_inicial = pos_inicial[1] * 32
        self.plr = Player((px_inicial, py_inicial), (32, 32), (10, 30, 170), 0, 0, 0)

        # Sincronizamos pos_visual y pos_destino desde el inicio
        self.plr.pos_visual = [float(px_inicial), float(py_inicial)]
        self.plr.pos_destino = [float(px_inicial), float(py_inicial)]

        self.direccion = (1, 0)   # empieza moviéndose a la derecha

        # Guardamos el momento en que arrancó la escena
        self.inicio = pygame.time.get_ticks()

        # Temporizador lógico: la grilla avanza cada 200ms
        self.tick = 0
        self.intervalo = 200

        # ── FASES DEL JUEGO ───────────────────────────────────────────────────
        # "vista"      → se muestra el mapa durante 3 segundos (jugador no se mueve)
        # "countdown"  → cuenta regresiva 3, 2, 1 (otros 3 segundos)
        # "jugando"    → partida en curso
        self.fase = "vista"

        self.txt_vista     = self.fuente.render("¡Memoriza el mapa!", True, (255, 255, 255))
        self.txt_countdown = self.fuente.render("El juego empieza en: 3", True, (255, 255, 255))

        # Texto de copa (aparece brevemente al consumir una)
        self.texto_copa = None
        self.texto_copa_hasta = 0

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                from G5.Data.Modules.Scene.Scenes.Menu import Menu
                self.game.set_scene(Menu(self.game))

    def update(self):
        ahora = pygame.time.get_ticks()
        tiempo_pasado = ahora - self.inicio   # ms desde que arrancó la escena

        # ── Fase 1: vista del mapa (0 – 3 000 ms) ────────────────────────────
        if self.fase == "vista":
            if tiempo_pasado >= 3000:
                # Pasamos a la cuenta regresiva y reiniciamos el reloj
                self.fase = "countdown"
                self.inicio = pygame.time.get_ticks()
            return   # el jugador no se mueve todavía

        # ── Fase 2: cuenta regresiva (0 – 3 000 ms desde el cambio de fase) ──
        if self.fase == "countdown":
            if tiempo_pasado < 1000:
                self.txt_countdown = self.fuente.render("El juego empieza en: 3", True, (255, 255, 255))
            elif tiempo_pasado < 2000:
                self.txt_countdown = self.fuente.render("El juego empieza en: 2", True, (255, 255, 255))
            elif tiempo_pasado < 3000:
                self.txt_countdown = self.fuente.render("El juego empieza en: 1", True, (255, 255, 255))
            else:
                self.fase = "jugando"
                self.tick = pygame.time.get_ticks()   # reseteamos el tick para que no salte
            return   # el jugador todavía no se mueve

        # ── Fase 3: juego en curso ────────────────────────────────────────────

        # Suavizado visual (60 veces por segundo)
        self.plr.update_visual()

        # Lógica de la grilla (cada 200ms)
        if ahora - self.tick >= self.intervalo:
            self.tick = ahora
            self.direccion = self.plr.cambiar_direccion(self.direccion)
            resultado, self.pos_logica = self.plr.avanzar(self.tab, self.direccion, self.pos_logica)

            if resultado == "derrota":
                from G5.Data.Modules.Scene.Scenes.Outro import Outro
                self.game.set_scene(Outro(self.game, 0))

            elif resultado == "copa":
                self.texto_copa = self.fuente.render("¡Copa consumida! +1 segmento.", True, (255, 215, 0))
                self.texto_copa_hasta = ahora + 2000
                self.map.gen_object(4, 1)   # nueva copa en el mapa

            elif resultado == "victoria":
                from G5.Data.Modules.Scene.Scenes.Outro import Outro
                self.game.set_scene(Outro(self.game, 1))

    def draw(self, screen):
        screen.fill((139, 153, 160))

        # El mapa se dibuja en las tres fases (incluyendo al jugador)
        self.map.draw(screen, self.plr)

        # ── Texto superpuesto según la fase ───────────────────────────────────
        if self.fase == "vista":
            # Fondo semitransparente para que el texto se lea bien
            overlay = pygame.Surface((15 * 32, 32), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            screen.blit(overlay, (0, 32 * 7 - 4))
            screen.blit(self.txt_vista, (32 * 3, 32 * 7))

        elif self.fase == "countdown":
            overlay = pygame.Surface((15 * 32, 32), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            screen.blit(overlay, (0, 32 * 7 - 4))
            screen.blit(self.txt_countdown, (32 * 3, 32 * 7))

        # Texto de copa (si está activo)
        if self.texto_copa and pygame.time.get_ticks() < self.texto_copa_hasta:
            screen.blit(self.texto_copa, (32 * 2, 32 * 19))

        screen.blit(self.volver_txt, (0, 32 * 20))