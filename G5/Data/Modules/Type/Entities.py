import pygame
import random

from G5.Data.Modules.Type.SpriteSheet import SpriteSheet
import Config


OFFSET_X = 288
OFFSET_Y = 96

def angulo_desde_direccion(direccion):
    """Convierte una dirección (dx,dy) en grados de rotación para el sprite."""
    dx, dy = direccion
    if (dx, dy) == (1, 0): return 0
    if (dx, dy) == (-1, 0): return 180
    if (dx, dy) == (0, -1): return 90
    if (dx, dy) == (0, 1): return -90
    return 0


class Entities:
    def __init__(self, pos: tuple, size: tuple, color: tuple, spd: float, hp: int, dmg: int, spr: str = None):
        self.pos = pos
        self.w = size[0]
        self.h = size[1]
        self.spr = spr
        self.spd = spd
        self.hp = hp
        self.dmg = dmg


class Bullet(Entities):
    """
    Proyectil disparado por un enemigo/jefe. Viaja en línea recta en píxeles
    (no salta de tile en tile), así que ya es "suave" por naturaleza.
    """
    def __init__(self, pos_pixel, direccion, velocidad=3, dmg=1, spr=None, color=(255, 60, 60)):
        super().__init__(pos_pixel, (16, 16), color, velocidad, 1, dmg, spr)
        self.pos_visual = [float(pos_pixel[0]) + 8, float(pos_pixel[1]) + 8]
        self.direccion = direccion
        self.velocidad = velocidad
        self.dmg = dmg
        self.color = color
        try:
            self.surf = SpriteSheet(spr).get_spr(0, 0, 32, 32)
            self.use_sprite = True
        except Exception:
            self.surf = None
            self.use_sprite = False

    def update(self):
        self.pos_visual[0] += self.direccion[0] * self.velocidad
        self.pos_visual[1] += self.direccion[1] * self.velocidad

    def fuera_de_mapa(self):
        x, y = self.pos_visual
        return (x < OFFSET_X - 20 or y < OFFSET_Y - 20 or
                x > OFFSET_X + 15 * 32 + 20 or y > OFFSET_Y + 15 * 32 + 20)

    def colisiona_con(self, px_centro, py_centro, radio=16):
        dx = self.pos_visual[0] - px_centro
        dy = self.pos_visual[1] - py_centro
        return (dx * dx + dy * dy) ** 0.5 < radio

    def draw(self, screen):
        x, y = self.pos_visual
        if self.use_sprite:
            rotado = pygame.transform.rotate(self.surf, angulo_desde_direccion(self.direccion))
            rect = rotado.get_rect(center=(int(x), int(y)))
            screen.blit(rotado, rect)
        else:
            pygame.draw.circle(screen, self.color, (int(x), int(y)), 6)


class Enemy(Entities):
    def __init__(self, pos: tuple, size: tuple, color: tuple, spd: float, hp: int, dmg: int, spr: str = None):
        super().__init__(pos, size, color, spd, hp, dmg, spr)
        self.color = color
        try:
            self.surf = SpriteSheet(spr).get_spr(0, 0, 32, 32)
            self.use_sprite = True
        except Exception:
            self.surf = None
            self.use_sprite = False

        self.pos_logica = ((pos[0] - OFFSET_X) // 32, (pos[1] - OFFSET_Y) // 32)

        # ── Movimiento suavizado (igual que el jugador) ────────────────────
        self.pos_visual = [float(pos[0]), float(pos[1])]
        self.pos_destino = [float(pos[0]), float(pos[1])]

        # ── IA de movimiento aleatorio ───────────────────────────────────────
        self.direccion = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        self.ultimo_movimiento = pygame.time.get_ticks()
        self.espera_movimiento = 6000

        # ── Disparo ───────────────────────────────────────────────────────────
        self.ultimo_disparo = 0
        self.cooldown_disparo = 2000  # ruta opcional al sprite de la flecha/bala

    def lerp(self, a, b, t):
        return a + (b - a) * t

    def update_visual(self):
        self.pos_visual[0] = self.lerp(self.pos_visual[0], self.pos_destino[0], 0.15)
        self.pos_visual[1] = self.lerp(self.pos_visual[1], self.pos_destino[1], 0.15)

    def elegir_movimiento(self, tablero):
        col, fila = self.pos_logica
        direcciones = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        random.shuffle(direcciones)

        for d_col, d_fila in direcciones:
            nueva_col, nueva_fila = col + d_col, fila + d_fila
            if 0 <= nueva_col < 15 and 0 <= nueva_fila < 15 and tablero[nueva_fila][nueva_col] == 0:
                tablero[fila][col] = 0
                tablero[nueva_fila][nueva_col] = 2
                self.pos_logica = (nueva_col, nueva_fila)
                self.direccion = (d_col, d_fila)
                self.pos_destino = [float(nueva_col * 32 + OFFSET_X), float(nueva_fila * 32 + OFFSET_Y)]
                return

        self.direccion = random.choice(direcciones)

    def actualizar(self, tablero, ahora):
        if ahora - self.ultimo_movimiento >= self.espera_movimiento:
            self.elegir_movimiento(tablero)
            self.ultimo_movimiento = ahora

    def apuntando_a(self, tablero, pos_jugador, cola_jugador):
        col, fila = self.pos_logica
        d_col, d_fila = self.direccion
        col += d_col
        fila += d_fila

        while 0 <= col < 15 and 0 <= fila < 15:
            if (col, fila) == pos_jugador or (col, fila) in cola_jugador:
                return True
            valor = tablero[fila][col]
            if valor == 3 or valor == 2:
                return False
            col += d_col
            fila += d_fila
        return False

    def draw(self, screen):
        px, py = self.pos_visual
        if self.use_sprite:
            rotado = pygame.transform.rotate(self.surf, angulo_desde_direccion(self.direccion))
            rect = rotado.get_rect(center=(int(px) + 16, int(py) + 16))
            screen.blit(rotado, rect)
        else:
            pygame.draw.rect(screen, self.color, (int(px), int(py), self.w, self.h))
            pygame.draw.rect(screen, (0, 0, 0), (int(px), int(py), self.w, self.h), 2)


class Boss(Enemy):
    """
    Jefe final: se mueve random igual que un Enemy normal (hereda actualizar()
    y elegir_movimiento()), pero reemplaza el disparo simple por un patrón
    de ataques en fases.
    """
    def __init__(self, pos, spr=None):
        super().__init__(pos, (32, 32), (180, 20, 20), 0, 10, 3, spr)
        self.fase_jefe = "reposo"
        self.contador_ataques = 0
        self.ultimo_cambio = pygame.time.get_ticks()
        self.duracion_reposo = 9000   # 9s de descanso por ciclo
        self.duracion_alerta = 2000    # 1s de aviso antes de disparar
        self.duracion_pausa = 1200      # pausa corta entre ataques rápidos
        self.velocidad_bala = 6
        self.hp = 20

    def actualizar_jefe(self, ahora, map_gen, pos_jugador, cola_jugador, jugador):
        transcurrido = ahora - self.ultimo_cambio
        eventos = []

        if self.fase_jefe == "reposo":
            if transcurrido >= self.duracion_reposo:
                self.fase_jefe = "alerta"
                self.ultimo_cambio = ahora
                eventos.append("¡El jefe se prepara para atacar!")

        elif self.fase_jefe == "alerta":
            if transcurrido >= self.duracion_alerta:
                self.contador_ataques += 1
                if self.contador_ataques % 5 == 0:
                    eventos += self._ataque_cargado(map_gen, pos_jugador, cola_jugador, jugador)
                    self.fase_jefe = "reposo"
                else:
                    self._ataque_cruz(map_gen)
                    self.fase_jefe = "cooldown_corto"
                self.ultimo_cambio = ahora

        elif self.fase_jefe == "cooldown_corto":
            if transcurrido >= self.duracion_pausa:
                self.fase_jefe = "alerta"
                self.ultimo_cambio = ahora
                eventos.append("¡El jefe ataca de nuevo!")

        return eventos
    
    def _atacado(self, fueAtacado=False):
        if fueAtacado:
            self.hp -= 1

    def _ataque_cruz(self, map_gen):
        """Ataque rápido: 4 balas en cruz (arriba, abajo, izq, der)."""
        print("ataque rapido")
        col, fila = self.pos_logica
        origen = (col * 32 + OFFSET_X, fila * 32 + OFFSET_Y)
        temp = pygame.mixer.Sound("G5/Data/Sounds/fireball.mp3")
        temp.set_volume(Config.sfx)
        temp.play()
        for direccion in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (-1, 0), (1, 0)]:
            map_gen.bullets.append(Bullet(origen, direccion, self.velocidad_bala, 1, "G5/Data/Sprites/bola de fuego.png"))

    def _ataque_cargado(self, map_gen, pos_jugador, cola_jugador, jugador):
        """Ataque cargado (cada 5to ataque): cruces de fuego en celdas random."""
        print("ataque cargado")
        celdas = random.sample([(c, f) for f in range(15) for c in range(15)], 4)
        map_gen.cruces_fuego = [(c, f, pygame.time.get_ticks() + 800) for c, f in celdas]

        temp = pygame.mixer.Sound("G5/Data/Sounds/fireball.mp3")
        temp.set_volume(Config.sfx)
        temp.play()

        eventos = []
        for c, f in celdas:
            if (c, f) == pos_jugador or (c, f) in cola_jugador:
                murio = jugador.recibir_flechazo(map_gen.map, 2)
                eventos.append("¡Te alcanzó una cruz de fuego!")
                if murio:
                    eventos.append("derrota")
        return eventos


class Player(Entities):
    def __init__(self, pos: tuple, size, color, spd, hp, dmg, spr=None,
                 spr_cabeza_sola=None, spr_cabeza=None, spr_torso=None, spr_cola=None):
        super().__init__(pos, size, color, spd, hp, dmg, spr)
        self.color = color
        self.cuchillos = 0

        # ── Sprites por parte del cuerpo (cabeza sola / cabeza / torso / cola) ─
        self.spr_cabeza_sola = self._cargar_sprite(spr_cabeza_sola)
        self.spr_cabeza = self._cargar_sprite(spr_cabeza)
        self.spr_torso = self._cargar_sprite(spr_torso)
        self.spr_cola = self._cargar_sprite(spr_cola)

        self.pos_visual = list(pos)
        self.pos_destino = list(pos)
        self.direccion = (1, 0)  # última dirección movida, para rotar la cabeza

        self.cola = []            # (col, fila) por segmento
        self.cola_direccion = []  # dirección que tenía CADA segmento al crearse (para rotar su sprite)
        self.crecer_en = 0
        self.cola_visual = []

    def _cargar_sprite(self, ruta):
        if not ruta:
            return None
        try:
            return SpriteSheet(ruta).get_spr(0, 0, 32, 32)
        except Exception:
            return None

    def lerp(self, a, b, t):
        return a + (b - a) * t

    def set_destino(self, px, py):
        self.pos_destino[0] = px
        self.pos_destino[1] = py

    def agregar_segmento(self):
        self.crecer_en += 1

    def esta_sprintando(self):
        keys = pygame.key.get_pressed()
        return keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]

    def recibir_flechazo(self, tablero, cantidad=1):
        for _ in range(cantidad):
            if self.cola:
                ultimo_col, ultimo_fila = self.cola.pop()
                if self.cola_direccion:
                    self.cola_direccion.pop()
                tablero[ultimo_fila][ultimo_col] = 0
                self.cola_visual.pop()
                temp = pygame.mixer.Sound("G5\Data\Sounds\death.mp3")
                temp.set_volume(Config.sfx)
                temp.play()
            else:
                return True
        return False

    def cambiar_direccion(self, direccion_actual):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: return (0, -1)
        if keys[pygame.K_s]: return (0, 1)
        if keys[pygame.K_a]: return (-1, 0)
        if keys[pygame.K_d]: return (1, 0)
        return direccion_actual

    def avanzar(self, tablero, direccion, pos_logica, sprintando=False, map_gen=None):
        self.direccion = direccion  # para rotar el sprite de la cabeza

        dir_col, dir_fila = direccion
        ind_actual_col, ind_actual_fila = pos_logica
        ind_nueva_col = ind_actual_col + dir_col
        ind_nueva_fila = ind_actual_fila + dir_fila

        if not (0 <= ind_nueva_col < 15 and 0 <= ind_nueva_fila < 15):
            return "derrota", pos_logica

        pos_elem = tablero[ind_nueva_fila][ind_nueva_col]
        resultado_extra = None

        pos_enemigo = None
        if map_gen:
            pos_enemigo = next(
            (e for e in map_gen.enemies if e.pos_logica == (ind_nueva_col, ind_nueva_fila)),
            None
            )
        
        es_jefe = isinstance(pos_enemigo, Boss)

        if pos_elem == 2:
            if es_jefe:
                return "derrota", pos_logica
            if sprintando and len(self.cola) > 0:
                temp = pygame.mixer.Sound("G5\Data\Sounds\death.mp3")
                temp.set_volume(Config.sfx)
                temp.play()

                if map_gen:
                    map_gen.matar_enemigo(ind_nueva_col, ind_nueva_fila)
                ultimo_col, ultimo_fila = self.cola.pop()
                self.cola_direccion.pop()
                tablero[ultimo_fila][ultimo_col] = 0
                self.cola_visual.pop()
                tablero[ind_nueva_fila][ind_nueva_col] = 0
                pos_elem = 0
                resultado_extra = "enemigo_muerto"
            else:
                return "derrota", pos_logica
        if pos_elem == 6:
            pass 

        if pos_elem == 3:
            return "derrota", pos_logica
        if pos_elem == 5:
            return "derrota", pos_logica

        copa = (pos_elem == 4)
        cuchillo = (pos_elem == 6) 

        self.cola.insert(0, (ind_actual_col, ind_actual_fila))
        self.cola_direccion.insert(0, direccion)
        tablero[ind_actual_fila][ind_actual_col] = 5

        px_cabeza = ind_actual_col * 32 + OFFSET_X
        py_cabeza = ind_actual_fila * 32 + OFFSET_Y
        self.cola_visual.insert(0, [float(px_cabeza), float(py_cabeza)])

        if self.crecer_en > 0:
            self.crecer_en -= 1
        else:
            if self.cola:
                ultimo_col, ultimo_fila = self.cola.pop()
                self.cola_direccion.pop()
                tablero[ultimo_fila][ultimo_col] = 0
                self.cola_visual.pop()

        tablero[ind_nueva_fila][ind_nueva_col] = 1

        if copa:
            self.agregar_segmento()
            return "copa", (ind_nueva_col, ind_nueva_fila)
        if cuchillo:
            self.cuchillos += 1
            return "cuchillo", (ind_nueva_col, ind_nueva_fila)
        if resultado_extra:
            return resultado_extra, (ind_nueva_col, ind_nueva_fila)
        return "ok", (ind_nueva_col, ind_nueva_fila)

    def update_visual(self):
        VELOCIDAD_LERP = 0.2
        self.pos_visual[0] = self.lerp(self.pos_visual[0], self.pos_destino[0], VELOCIDAD_LERP)
        self.pos_visual[1] = self.lerp(self.pos_visual[1], self.pos_destino[1], VELOCIDAD_LERP)
        for i, (col, fila) in enumerate(self.cola):
            self.cola_visual[i][0] = self.lerp(self.cola_visual[i][0], col * 32 + OFFSET_X, VELOCIDAD_LERP)
            self.cola_visual[i][1] = self.lerp(self.cola_visual[i][1], fila * 32 + OFFSET_Y, VELOCIDAD_LERP)

    def _dibujar_parte(self, screen, pos_visual, sprite, direccion, es_cabeza):
        px, py = pos_visual
        tam = self.w
        if sprite is not None:
            rotado = pygame.transform.rotate(sprite, angulo_desde_direccion(direccion))
            rect = rotado.get_rect(center=(int(px) + tam // 2, int(py) + tam // 2))
            screen.blit(rotado, rect)
        else:
            color = self.color if es_cabeza else (
                max(0, self.color[0] - 40), max(0, self.color[1] - 40), max(0, self.color[2] - 40)
            )
            pygame.draw.rect(screen, color, (int(px), int(py), tam, tam))
            pygame.draw.rect(screen, (0, 0, 0), (int(px), int(py), tam, tam), 2)

    def draw(self, screen):
        n = len(self.cola)
        for i in range(n - 1, -1, -1):
            es_ultimo = (i == n - 1)
            sprite_base = self.spr_cola if es_ultimo else self.spr_torso
            self._dibujar_parte(screen, self.cola_visual[i], sprite_base, self.cola_direccion[i], es_cabeza=False)

        sprite_cabeza = self.spr_cabeza_sola if n == 0 else self.spr_cabeza
        self._dibujar_parte(screen, self.pos_visual, sprite_cabeza, self.direccion, es_cabeza=True)