import pygame
import math

from G5.Data.Modules.Type.SpriteSheet import SpriteSheet


class Entities:
    def __init__(self, pos: tuple, size: tuple, color: tuple, spd: float, hp: int, dmg: int, spr: str = None):
        self.pos = pos
        self.w = size[0]
        self.h = size[1]
        self.spr = spr
        self.spd = spd
        self.hp = hp
        self.dmg = dmg


class Enemy(Entities):
    def __init__(self, pos: tuple, size: tuple, color: tuple, spd: float, hp: int, dmg: int, spr: str = None):
        super().__init__(pos, size, color, spd, hp, dmg, spr)
        try:
            self.surf = SpriteSheet(spr).get_spr(0, 0, 32, 32)
            self.rect = self.surf.get_rect(topleft=(pos[0], pos[1]))
            self.use_sprite = True
        except:
            self.surf = pygame.Surface([self.w, self.h])
            self.surf.fill(color)
            self.rect = self.surf.get_rect(topleft=(pos[0], pos[1]))
            self.color = color
            self.use_sprite = False

    def cambiar_direccion(self, direccion_actual):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            return (0, -1)
        if keys[pygame.K_s]:
            return (0, 1)
        if keys[pygame.K_a]:
            return (-1, 0)
        if keys[pygame.K_d]:
            return (1, 0)

        return direccion_actual

    def avanzar(self, tablero, direccion, pos_logica):
        dir_col, dir_fila = direccion
        ind_actual_col, ind_actual_fila = pos_logica

        ind_nueva_col = ind_actual_col + dir_col
        ind_nueva_fila = ind_actual_fila + dir_fila

        # Choque con el borde
        if not (0 <= ind_nueva_col < 15 and 0 <= ind_nueva_fila < 15):
            return "derrota", pos_logica

        pos_elem = tablero[ind_nueva_fila][ind_nueva_col]

        # Choque con enemigo u obstáculo
        if pos_elem == 2 or pos_elem == 3:
            return "derrota", pos_logica

        # Choque con propia cola (id=5)
        if pos_elem == 5:
            return "derrota", pos_logica

        copa = (pos_elem == 4)

        # ── Actualizar la cola en el tablero ─────────────────────────────────
        #
        # La cabeza estaba en (ind_actual_col, ind_actual_fila).
        # Esa posición pasa a ser el primer segmento de cola.
        #
        # Paso 1: insertar la posición vieja de la cabeza al inicio de la cola
        self.cola.insert(0, (ind_actual_col, ind_actual_fila))
        tablero[ind_actual_fila][ind_actual_col] = 5   # marcar como cola en el tablero

        # También insertamos una pos_visual nueva para ese segmento
        # (empieza en la misma posición visual que la cabeza, y de ahí sigue)
        px_cabeza = ind_actual_col * 32
        py_cabeza = ind_actual_fila * 32
        self.cola_visual.insert(0, [float(px_cabeza), float(py_cabeza)])

        # Paso 2: si hay que crecer, no borramos el último segmento
        if self.crecer_en > 0:
            self.crecer_en -= 1
        else:
            # Borrar el último segmento de la cola (la serpiente se mueve)
            if self.cola:
                ultimo_col, ultimo_fila = self.cola.pop()
                tablero[ultimo_fila][ultimo_col] = 0
                self.cola_visual.pop()

        # Paso 3: mover la cabeza a la nueva posición
        tablero[ind_nueva_fila][ind_nueva_col] = 1

        if copa:
            self.agregar_segmento()   # programa crecer 1 tile la próxima vez
            return "copa", (ind_nueva_col, ind_nueva_fila)

        return "ok", (ind_nueva_col, ind_nueva_fila)

    def set_vh(self):
        """Genera los vértices de la forma hexagonal"""
        r = self.w / 2
        vertices = []
        for i in range(6):
            angulo = math.pi / 3 * i
            vx = self.pos[0] + r * math.cos(angulo)
            vy = self.pos[1] + r * math.sin(angulo)
            vertices.append((int(vx + self.w / 2), int(vy + self.w / 2)))
        return vertices

    def draw(self, screen):
        if self.use_sprite:
            screen.blit(self.surf, self.rect)
        else:
            pygame.draw.polygon(screen, self.color, self.set_vh())


class Player(Entities):
    def __init__(self, pos: tuple, size, color, spd, hp, dmg, spr=None):
        super().__init__(pos, size, color, spd, hp, dmg, spr)
        self.color = color
        try:
            self.surf = SpriteSheet(spr).get_spr(0, 0, 32, 32)
            self.rect = self.surf.get_rect(topleft=(pos[0], pos[1]))
            self.use_sprite = True
        except:
            self.surf = pygame.Surface([self.w, self.h])
            self.surf.fill(color)
            self.rect = self.surf.get_rect(topleft=(pos[0], pos[1]))
            self.use_sprite = False

        # ── MOVIMIENTO SUAVIZADO ──────────────────────────────────────────────
        self.pos_visual = list(pos)   # posición en píxeles que se dibuja (se mueve suave)
        self.pos_destino = list(pos)  # posición en píxeles destino (celda actual en el mapa)

        # ── COLA (Snake) ──────────────────────────────────────────────────────
        # cola es una lista de posiciones lógicas (col, fila) que siguen a la cabeza.
        # Empieza vacía; cada copa agrega un segmento al final.
        #
        # Cómo funciona en avanzar():
        #   1. Insertamos la posición actual de la cabeza al INICIO de la cola.
        #   2. Si hay que crecer (crecer_en > 0): no borramos el último segmento.
        #   3. Si no: borramos el último segmento (la serpiente "avanza").
        self.cola = []          # lista de (col, fila) — segmentos de la cola
        self.crecer_en = 0      # cuántos segmentos extra quedan por agregar

        # ── SUAVIZADO DE LA COLA ──────────────────────────────────────────────
        # Cada segmento tiene su propia pos_visual para el lerp, igual que la cabeza.
        # cola_visual[i] = [x, y] en píxeles del segmento i
        self.cola_visual = []

    # ── HELPERS ──────────────────────────────────────────────────────────────

    def lerp(self, a, b, t):
        """
        Interpolación lineal entre a y b con factor t (0.0 → 1.0).
        t=0.2 → avanza el 20% de la distancia que falta cada frame.
        """
        return a + (b - a) * t

    def set_destino(self, px, py):
        """MapGen llama esto cuando detecta la cabeza del jugador en el mapa."""
        self.pos_destino[0] = px
        self.pos_destino[1] = py

    def agregar_segmento(self):
        """Al consumir una copa, programa agregar 1 tile más a la cola."""
        self.crecer_en += 1

    # ── LÓGICA ───────────────────────────────────────────────────────────────

    def cambiar_direccion(self, direccion_actual):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            return (0, -1)
        if keys[pygame.K_s]:
            return (0, 1)
        if keys[pygame.K_a]:
            return (-1, 0)
        if keys[pygame.K_d]:
            return (1, 0)

        return direccion_actual

    def avanzar(self, tablero, direccion, pos_logica):
        dir_col, dir_fila = direccion
        ind_actual_col, ind_actual_fila = pos_logica

        ind_nueva_col = ind_actual_col + dir_col
        ind_nueva_fila = ind_actual_fila + dir_fila

        # Choque con el borde
        if not (0 <= ind_nueva_col < 15 and 0 <= ind_nueva_fila < 15):
            return "derrota", pos_logica

        pos_elem = tablero[ind_nueva_fila][ind_nueva_col]

        # Choque con enemigo u obstáculo
        if pos_elem == 2 or pos_elem == 3:
            return "derrota", pos_logica

        # Choque con propia cola (id=5)
        if pos_elem == 5:
            return "derrota", pos_logica

        copa = (pos_elem == 4)

        # ── Actualizar la cola en el tablero ─────────────────────────────────
        #
        # La cabeza estaba en (ind_actual_col, ind_actual_fila).
        # Esa posición pasa a ser el primer segmento de cola.
        #
        # Paso 1: insertar la posición vieja de la cabeza al inicio de la cola
        self.cola.insert(0, (ind_actual_col, ind_actual_fila))
        tablero[ind_actual_fila][ind_actual_col] = 5   # marcar como cola en el tablero

        # También insertamos una pos_visual nueva para ese segmento
        # (empieza en la misma posición visual que la cabeza, y de ahí sigue)
        px_cabeza = ind_actual_col * 32
        py_cabeza = ind_actual_fila * 32
        self.cola_visual.insert(0, [float(px_cabeza), float(py_cabeza)])

        # Paso 2: si hay que crecer, no borramos el último segmento
        if self.crecer_en > 0:
            self.crecer_en -= 1
        else:
            # Borrar el último segmento de la cola (la serpiente se mueve)
            if self.cola:
                ultimo_col, ultimo_fila = self.cola.pop()
                tablero[ultimo_fila][ultimo_col] = 0
                self.cola_visual.pop()

        # Paso 3: mover la cabeza a la nueva posición
        tablero[ind_nueva_fila][ind_nueva_col] = 1

        if copa:
            self.agregar_segmento()   # programa crecer 1 tile la próxima vez
            return "copa", (ind_nueva_col, ind_nueva_fila)

        return "ok", (ind_nueva_col, ind_nueva_fila)

    # ── ACTUALIZACIÓN VISUAL (llamar cada frame) ──────────────────────────────

    def update_visual(self):
        """
        Mueve pos_visual de la cabeza y de cada segmento de cola hacia su destino.
        Cada segmento sigue al anterior con un pequeño retraso natural por el lerp.
        """
        VELOCIDAD_LERP = 0.2

        # Suavizar la cabeza
        self.pos_visual[0] = self.lerp(self.pos_visual[0], self.pos_destino[0], VELOCIDAD_LERP)
        self.pos_visual[1] = self.lerp(self.pos_visual[1], self.pos_destino[1], VELOCIDAD_LERP)

        # Suavizar cada segmento de cola hacia su posición lógica
        for i, (col, fila) in enumerate(self.cola):
            dest_x = col * 32
            dest_y = fila * 32
            self.cola_visual[i][0] = self.lerp(self.cola_visual[i][0], dest_x, VELOCIDAD_LERP)
            self.cola_visual[i][1] = self.lerp(self.cola_visual[i][1], dest_y, VELOCIDAD_LERP)

    # ── DIBUJO ───────────────────────────────────────────────────────────────

    def _dibujar_segmento(self, screen, px, py, es_cabeza=False):
        """
        Dibuja un único tile de la serpiente (cabeza o cola) en la posición (px, py).
        La cabeza es un poco más brillante para distinguirse.
        """
        tam = self.w   # 32px
        if self.use_sprite:
            screen.blit(self.surf, (int(px), int(py)))
        else:
            color = self.color if es_cabeza else (
                max(0, self.color[0] - 40),
                max(0, self.color[1] - 40),
                max(0, self.color[2] - 40)
            )
            pygame.draw.rect(screen, color, (int(px), int(py), tam, tam))
            # Borde oscuro para que se distingan los segmentos
            pygame.draw.rect(screen, (0, 0, 0), (int(px), int(py), tam, tam), 2)

    def draw(self, screen):
        # Dibujar cola primero (para que quede debajo de la cabeza)
        for seg_visual in self.cola_visual:
            self._dibujar_segmento(screen, seg_visual[0], seg_visual[1], es_cabeza=False)

        # Dibujar cabeza encima
        self._dibujar_segmento(screen, self.pos_visual[0], self.pos_visual[1], es_cabeza=True)