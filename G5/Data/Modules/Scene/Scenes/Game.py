from G5.Data.Modules.Scene.Scene import Scene
from G5.Data.Modules.Type.Entities import Player
from G5.Data.Modules.Services.MapGen import MapGen

import pygame


class Game(Scene):
    # Requisitos para pasar de ronda: {ronda: (enemigos_a_matar, copas_a_consumir)}
    REQUISITOS_RONDA = {
        1: (1, 3),
        2: (2, 4),
        3: (4, 6),
        4: (2, 7),
        5: (4, 8),
    }

    def __init__(self, game):
        super().__init__(game)
        self.game = game

        self.fuente = game.font
        self.volver_txt = self.fuente.render("Presione [ESCAPE] para volver al menu.", True, (255, 255, 255))

        self.map = MapGen()
        self.tab = self.map.map

        pos_inicial = self.map.gen_object(1)[0]
        self.pos_logica = pos_inicial

        px_inicial = (pos_inicial[0] * 32) + 288
        py_inicial =( pos_inicial[1] * 32) + 96
        self.plr = Player((px_inicial, py_inicial), (32, 32), (10, 30, 170), 0, 0, 0,
                   spr_cabeza_sola="G5/Data/Sprites/jugador cabeza s.png",
                   spr_cabeza="G5/Data/Sprites/Jugador cabeza.png",
                   spr_torso="G5/Data/Sprites/Jugador torso.png",
                   spr_cola="G5/Data/Sprites/Jugador cola.png")
        self.plr.pos_visual = [float(px_inicial), float(py_inicial)]
        self.plr.pos_destino = [float(px_inicial), float(py_inicial)]

        self.direccion = (1, 0)

        self.inicio = pygame.time.get_ticks()
        self.tick = 0
        self.intervalo = 200
        self.intervalo_sprint = 100
        self.sprint_inicio = None 

        self.fase = "vista"
        self.txt_vista = self.fuente.render("¡Memoriza el mapa!", True, (255, 255, 255))
        self.txt_countdown = self.fuente.render("El juego empieza en: 3", True, (255, 255, 255))

        self.texto_copa = None
        self.texto_copa_hasta = 0

        # ── RONDAS Y PUNTAJE ─────────────────────────────────────────────────
        self.ronda = 1
        self.enemigos_ronda = 0   # se resetean al pasar de ronda
        self.copas_ronda = 0
        self.enemigos_totales = 0  # cuentan TODA la partida, para el puntaje final
        self.copas_totales = 0

        self.texto_evento = None
        self.texto_evento_hasta = 0

    def _mostrar_evento(self, texto, color=(255, 120, 120), ms=2000):
        self.texto_evento = self.fuente.render(texto, True, color)
        self.texto_evento_hasta = pygame.time.get_ticks() + ms

    def _ir_a_outro(self, gano: int):
        from G5.Data.Modules.Scene.Scenes.Outro import Outro
        puntaje = self.copas_totales * 10 + self.enemigos_totales * 25
        self.game.set_scene(Outro(self.game, gano, self.copas_totales, self.enemigos_totales, puntaje))

    def _revisar_avance_ronda(self):
        requisito = self.REQUISITOS_RONDA.get(self.ronda)
        if requisito is None:
            return

        enemigos_req, copas_req = requisito
        if self.enemigos_ronda >= enemigos_req and self.copas_ronda >= copas_req:
            self.ronda += 1
            self.enemigos_ronda = 0
            self.copas_ronda = 0
            self._mostrar_evento(f"¡Ronda {self.ronda}!", (120, 220, 255), 2500)

            if self.ronda == 2:
                self.map.gen_enemies(2)
            if self.ronda == 3:
                self.map.gen_enemies(4)
            if self.ronda == 4:
                self.map.gen_enemies(3, 2)
            if self.ronda == 5:
                self.map.gen_enemies(5, 2)
            if self.ronda >= 6:
                self.map.gen_object(6)
                self.map.gen_boss()
                self._mostrar_evento("¡Apareció el jefe final!", (255, 60, 60), 3000)

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                from G5.Data.Modules.Scene.Scenes.Menu import Menu
                self.game.set_scene(Menu(self.game))

    def update(self):
        ahora = pygame.time.get_ticks()
        tiempo_pasado = ahora - self.inicio

        if self.fase == "vista":
            if tiempo_pasado >= 3000:
                self.fase = "countdown"
                self.inicio = pygame.time.get_ticks()
            return

        if self.fase == "countdown":
            if tiempo_pasado < 1000:
                self.txt_countdown = self.fuente.render("El juego empieza en: 3", True, (255, 255, 255))
            elif tiempo_pasado < 2000:
                self.txt_countdown = self.fuente.render("El juego empieza en: 2", True, (255, 255, 255))
            elif tiempo_pasado < 3000:
                self.txt_countdown = self.fuente.render("El juego empieza en: 1", True, (255, 255, 255))
            else:
                self.fase = "jugando"
                self.tick = pygame.time.get_ticks()
            return

        self.plr.update_visual()

        cola_set = set(self.plr.cola)
        eventos = self.map.actualizar_enemigos(ahora, self.pos_logica, cola_set, self.plr)
        eventos += self.map.actualizar_balas(self.plr)
        for ev in eventos:
            if ev == "derrota":
                self._ir_a_outro(0)
                return
            self._mostrar_evento(ev)

        # ── Movimiento del jugador (cada 200ms) ──────────────────────────────
        if ahora - self.tick >= self.intervalo:
            shift_apretado = self.plr.esta_sprintando()
            if shift_apretado:
                if self.sprint_inicio is None:
                    self.sprint_inicio = ahora
                    pygame.mixer.Sound("G5\Data\Sounds\sprint.mp3").play()
                sprint_activo = (ahora - self.sprint_inicio) < 4000
            else:
                self.sprint_inicio = None
                sprint_activo = False

            intervalo_actual = self.intervalo_sprint if sprint_activo else self.intervalo

            if ahora - self.tick >= intervalo_actual:
                self.tick = ahora
                self.direccion = self.plr.cambiar_direccion(self.direccion)
                resultado, self.pos_logica = self.plr.avanzar(
                    self.tab, self.direccion, self.pos_logica, sprint_activo, self.map
                )

                if resultado == "derrota":
                    self._ir_a_outro(0)

                elif resultado == "copa":
                    self.copas_ronda += 1
                    self.copas_totales += 1
                    self.texto_copa = self.fuente.render("¡Copa consumida! +1 segmento.", True, (255, 215, 0))
                    self.texto_copa_hasta = ahora + 2000
                    self.map.gen_object(4, 1)
                    self._revisar_avance_ronda()

                elif resultado == "cuchillo":
                    self.texto_copa = self.fuente.render("¡Atacaste al obispo! -1 de vida a tu enemigo.", True, (255, 215, 0))
                    self.texto_copa_hasta = ahora + 2000
                    
                elif resultado == "enemigo_muerto":
                    self.enemigos_ronda += 1
                    self.enemigos_totales += 1
                    self._mostrar_evento("¡Enemigo muerto con sprint!", (120, 255, 120))
                    if self.ronda == 6 and not self.map.enemies:
                        self._ir_a_outro(1)
                    else:
                        self._revisar_avance_ronda()

                elif resultado == "victoria":
                    self._ir_a_outro(1)

            elif resultado == "victoria":
                self._ir_a_outro(1)

    def draw(self, screen):
        screen.fill((139, 153, 160))
        self.map.draw(screen, self.plr)

        if self.fase == "vista":
            overlay = pygame.Surface((15 * 32, 32), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            screen.blit(overlay, (0, 32 * 7 - 4))
            screen.blit(self.txt_vista, (32 * 3, 32 * 7))

        elif self.fase == "countdown":
            overlay = pygame.Surface((15 * 32, 32), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            screen.blit(overlay, (0, 32 * 7 - 4))
            screen.blit(self.txt_countdown, (32 * 3, 32 * 7))

        if self.texto_copa and pygame.time.get_ticks() < self.texto_copa_hasta:
            screen.blit(self.texto_copa, (32 * 2, 32 * 19))

        if self.texto_evento and pygame.time.get_ticks() < self.texto_evento_hasta:
            screen.blit(self.texto_evento, (32 * 2, 32 * 18))

        hud = self.fuente.render(
            f"Ronda {self.ronda}  |  Enemigos: {self.enemigos_ronda}  Copas: {self.copas_ronda}",
            True, (255, 255, 255)
        )
        screen.blit(hud, (32 * 2, 0))

        screen.blit(self.volver_txt, (0, 32 * 20))