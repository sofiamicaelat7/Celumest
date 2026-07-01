import json
import os

class Catalogo:
    ARCHIVO = "catalogos.json"
    def __init__(self):
        self.marcas = []
        self.modelos = {}
        self.colores = []
        self.memorias = []
        self.rams = []
        self.cargar()

    def cargar(self):
        if not os.path.exists(self.ARCHIVO):
            self.marcas = ["Samsung","Motorola","Xiaomi"]
            self.modelos = {"Samsung": ["A55", "A35"],"Motorola": ["G84"],"Xiaomi": ["Redmi Note 13"]}
            self.colores = ["Negro","Blanco","Azul"]
            self.memorias = ["64 GB","128 GB","256 GB"]
            self.rams = ["4 GB","6 GB","8 GB"]
            self.guardar()
            return

        with open(self.ARCHIVO,"r",encoding="utf-8") as archivo:
            datos = json.load(archivo)
        self.marcas = datos["marcas"]
        self.modelos = datos["modelos"]
        self.colores = datos["colores"]
        self.memorias = datos["memorias"]
        self.rams = datos["rams"]

    def guardar(self):
        datos = {"marcas": self.marcas,"modelos": self.modelos,"colores": self.colores,"memorias": self.memorias,"rams": self.rams}
        with open(self.ARCHIVO,"w",encoding="utf-8") as archivo:
            json.dump(datos,archivo,indent=4,ensure_ascii=False)

    # MARCAS
    def agregar_marca(self, marca):
        marca = marca.strip()
        if (marca and marca not in self.marcas):
            self.marcas.append(marca)
            self.modelos[marca] = []
            self.guardar()

    # MODELOS
    def agregar_modelo(self, marca, modelo):
        modelo = modelo.strip()
        if not modelo:
            return
        if marca not in self.modelos:
            self.modelos[marca] = []
        if modelo not in self.modelos[marca]:
            self.modelos[marca].append(modelo)
            self.guardar()

    # COLORES
    def agregar_color(self, color):
        color = color.strip()
        if (color and color not in self.colores):
            self.colores.append(color)
            self.guardar()

    # MEMORIAS
    def agregar_memoria(self, memoria):
        memoria = memoria.strip()
        if (memoria and memoria not in self.memorias):
            self.memorias.append(memoria)
            self.guardar()

    # RAM
    def agregar_ram(self, ram):
        ram = ram.strip()
        if (ram and ram not in self.rams):
            self.rams.append(ram)
            self.guardar()