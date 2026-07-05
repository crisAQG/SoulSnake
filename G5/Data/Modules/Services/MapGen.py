from G5.Data.Modules.Type.Blocks import Tile
from G5.Data.Modules.Type.Entities import Enemy, Bullet, Boss

import random
import pygame


class MapGen:
    def __init__(self):
        self.map = self.gen_map()
        self.enemies = []
        self.bullets = []
        self.cruces_fuego = []  # (col, fila, expira_en_ms) del ataque cargado del jefe

        self.gen_enemies(4)
        self.gen_object(3, 6)
        self.gen_object(4, 1)

    def gen_map(self):
        return [[0] * 15 for _ in range(15)]

    def gen_object(self, id_elem, cantidad=1):
        colocados = []
        for _ in range(cantidad):
            vacios = [(col, fil) for fil in range(15) for col in range(15) if self.map[fil][col] == 0]
            if not vacios:
                break
            columna, fila = random.choice(vacios)
            self.map[fila][columna] = id_elem
            colocados.append((columna, fila))
        return colocados

    def gen_enemies(self, cantidad=1, type=1):
        colocados = []
        for _ in range(cantidad):
            vacios = [(col, fil) for fil in range(15) for col in range(15) if self.map[fil][col] == 0]
            if not vacios:
                break
            columna, fila = random.choice(vacios)
            self.map[fila][columna] = 2
            enemigo = None
            if type == 1:
                enemigo = Enemy(((columna * 32) + 288, (fila * 32) + 96), (32, 32), (0, 170, 40), 0, 1, 1,
                             "G5/Data/Sprites/enemigo principal.png")
            else:
                enemigo = Enemy(((columna * 32) + 288, (fila * 32) + 96), (32, 32), (0, 170, 40), 0, 1, 2,
                             "G5/Data/Sprites/enemigo 3 1.png")

            self.enemies.append(enemigo)
            colocados.append((columna, fila))
        return colocados

    def gen_boss(self):
        """Limpia enemigos normales y coloca al jefe final."""
        self.enemies = []
        vacios = [(c, f) for f in range(15) for c in range(15) if self.map[f][c] == 0]
        columna, fila = random.choice(vacios)
        self.map[fila][columna] = 2
        jefe = Boss(((columna * 32) + 288, (fila * 32) + 96), "G5/Data/Sprites/cura.png")
        self.enemies.append(jefe)

    def matar_enemigo(self, col, fila):
        if self.map[fila][col] == 2:
            self.map[fila][col] = 0
        self.enemies = [e for e in self.enemies if e.pos_logica != (col, fila)]

    def actualizar_enemigos(self, ahora, pos_jugador, cola_jugador, jugador):
        eventos = []
        for enemigo in self.enemies:
            enemigo.actualizar(self.map, ahora)   # movimiento random c/6s
            enemigo.update_visual()               # suavizado visual

            if isinstance(enemigo, Boss):
                eventos += enemigo.actualizar_jefe(ahora, self, pos_jugador, cola_jugador, jugador)
            else:
                puede_disparar = ahora - enemigo.ultimo_disparo >= enemigo.cooldown_disparo
                if puede_disparar and enemigo.apuntando_a(self.map, pos_jugador, cola_jugador):
                    enemigo.ultimo_disparo = ahora
                    origen = (enemigo.pos_visual[0], enemigo.pos_visual[1])
                    if enemigo.dmg == 1:
                        self.bullets.append(Bullet(origen, enemigo.direccion, 3,
                                                    enemigo.dmg, spr="G5/Data/Sprites/Flecha.png"))
                    else:
                        self.bullets.append(Bullet(origen, enemigo.direccion, 2,
                                                    enemigo.dmg, spr="G5/Data/Sprites/Pocion.png"))

        return eventos

    def actualizar_balas(self, jugador):
        """Mueve las balas, revisa impactos contra el jugador/cola, y las limpia."""
        eventos = []
        vivas = []
        cx, cy = jugador.pos_visual[0] + 16, jugador.pos_visual[1] + 16

        for bala in self.bullets:
            bala.update()
            golpeo = bala.colisiona_con(cx, cy)
            if not golpeo:
                for seg in jugador.cola_visual:
                    if bala.colisiona_con(seg[0] + 16, seg[1] + 16):
                        golpeo = True
                        break

            if golpeo:
                murio = jugador.recibir_flechazo(self.map, bala.dmg)
                eventos.append("¡Una flecha te dio!")
                if murio:
                    eventos.append("derrota")
                continue
            if bala.fuera_de_mapa():
                continue
            vivas.append(bala)

        self.bullets = vivas
        return eventos

    def draw(self, screen, player):
        tam = 32
        for fila in range(15):
            for col in range(15):
                pos_x, pos_y = (col * tam) + 288, (fila * tam) + 96
                valor = self.map[fila][col]

                Tile(pos_x, pos_y, tam, tam, (140, 124, 137), 0, "G5/Data/Sprites/tile.png").draw(screen)

                if valor == 1:
                    player.set_destino(pos_x, pos_y)
                elif valor == 3:
                    Tile(pos_x, pos_y, tam, tam, (10, 10, 10), 0, "G5/Data/Sprites/silla.png").draw(screen)
                elif valor == 4:
                    Tile(pos_x, pos_y, tam, tam, (255, 215, 0), 4, "G5/Data/Sprites/copa.png").draw(screen)
                elif valor == 5:
                    Tile(pos_x, pos_y, tam, tam, (140, 124, 137), 0).draw(screen)

        # Cruces de fuego del ataque cargado (se limpian solas al expirar)
        ahora = pygame.time.get_ticks()
        self.cruces_fuego = [(c, f, exp) for c, f, exp in self.cruces_fuego if exp > ahora]
        for c, f, _ in self.cruces_fuego:
            pygame.draw.rect(screen, (255, 100, 0), (c * 32 + 288, f * 32 + 96, tam, tam))

        for enemigo in self.enemies:
            enemigo.draw(screen)
        for bala in self.bullets:
            bala.draw(screen)

        player.draw(screen)