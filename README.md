# Soulnake 🐍
SoulSnake es un juego creado por estudiantes de Ingenieria civil Informatica de la UACh, y el estudiante del Domus Mater Marcos Vargas, mente maestra del juego.

---

# Información de modulos 📦
## Globales 🌐:
Main.py: Lanzador del juego

Config.py: Variables globales (tamaño de pantalla y tiles, fps, colores(puede ser funcionalidad futura))

## Data/Modules:
Window.py 🖼: Clase donde se define la pantalla pygame, su caracteristicas y el bucle de ejecucion (no tocar todo, solo la parte que dice "self.set_scene(Test.Test(self))").

	Scene
    + __init__(): El constructor e inicializador de la clase. Se define la pantalla de pygame y derivados
    + set_scene(scene): Metodo para cambiar de ventanas (o escenas)
		- scene: Se ingresa una clase tipo Scene 
	+ events(): Metodo que maneja los eventos de pygame, como el salir de pygame y los eventos de cada escena
	+ update(): Maneja las actualizaciones de objetos de cada escena antes de dibujarlos 
	+ draw(): Dibuja los objetos que tuvieron algun cambio en la etapa de update()
	+ loop(): Maneja el bucle para que el juego funcione

## Data/Modules/Scene:
Scene.py 🎞: Esqueleto de una escena a simples palabras
	
    Scene
	+ __init__(game): El constructor e inicializador de la clase hija, se ejecuta cuando se llame a una clase tipo scene. 
		- game: parametro donde se aloja la pantalla pygame (modulo Window.py)
	+ events(event): Maneja los eventos locales (Las escenas hijas)
		- event: define el tipo de evento que pygame identifica
	+ update(): Maneja las actualizaciones de objetos locales
	+ draw(screen): Maneja los dibujos de los objetos locales previamente actualizados

/Scenes/ 🎞🎞🎞: Carpetas que almacena las escenas (clases tipo scene)

## Data/Modules/Services:
MapGen.py 🗺: Modulo encargado a la generacion de las casillas de juego, el jugador, enemigos, items, etc.
	
    MapGen
	+ __init__(): Constructor e inicializador del mapa
    + gen_map(), gen_enemies(), gen_items(), gen_player(), gen_obst(): Generadores del mapa

## Data/Modules/Services:
Blocks.py: Modulos de bloques y estructuras en general

    Tile: Bloque tile donde dibuja un sprite o una forma de color
        + x, y: posicion en pantalla
        + w, h: tamaño (w: ancho, h: alto)
        + color: se ingresa el color de una forma en (r, g, b)
        + form: se ingresa el tipo de forma con el id correspondiente (mirar modulo)
        + file_path: en caso de tener una imagen para el tile, se crea un tile como imagen

---

# Archivo releases 🔄
Las notas de actualizaciones del proyecto se guardaran en el archivo releases, este contendra los cambios del proyecto.