import json
import os

class Producto:

    def __init__(self,marca,modelo,color,precio,cantidad,vendible=True):
        self.marca = marca
        self.modelo = modelo
        self.color = color
        self.precio = precio
        self.cantidad = cantidad
        self.vendible = vendible

    def to_dict(self):
        return {"tipo": self.__class__.__name__,"marca": self.marca,"modelo": self.modelo,"color": self.color,"precio": self.precio,"cantidad": self.cantidad,"vendible": self.vendible}


class Telefono(Producto):

    def __init__(self,marca,modelo,color,precio,cantidad,memoria,ram,vendible=True):
        super().__init__(marca,modelo,color,precio,cantidad,vendible)
        self.memoria = memoria
        self.ram = ram

    def to_dict(self):
        datos = super().to_dict()
        datos["memoria"] = self.memoria
        datos["ram"] = self.ram
        return datos


class Accesorio(Producto):
    pass

class Audio(Producto):
    pass

class Otro(Producto):
    pass


class Inventario:
    ARCHIVO = "inventario.json"
    def __init__(self):
        self.productos = []
        self.cargar()

    def agregar(self, producto):
        existente = self.buscar(producto)
        if existente:
            existente.cantidad += producto.cantidad
        else:
            self.productos.append(producto)
        self.guardar()

    def eliminar(self, producto):
        if producto in self.productos:
            self.productos.remove(producto)
            self.guardar()

    def buscar(self, producto):

        for p in self.productos:
            if type(p) != type(producto):
                continue
            if (p.marca == producto.marca and p.modelo == producto.modelo and p.color == producto.color and p.vendible == producto.vendible):
                if isinstance(producto, Telefono):
                    if (p.memoria == producto.memoria and p.ram == producto.ram ):
                        return p

                else:

                    return p

        return None

    def obtener_todos(self):
        return self.productos

    def guardar(self):

        datos = []

        for producto in self.productos:
            datos.append(producto.to_dict())

        with open(self.ARCHIVO,"w",encoding="utf-8") as archivo:
            json.dump(datos,archivo,indent=4,ensure_ascii=False)

    def cargar(self):

        if not os.path.exists(self.ARCHIVO):
            return

        with open(self.ARCHIVO,"r",encoding="utf-8") as archivo:
            datos = json.load(archivo)

        for item in datos:

            tipo = item.get("tipo","Telefono")
            if tipo == "Telefono":
                producto = Telefono(item["marca"],item["modelo"],item["color"],item["precio"],item["cantidad"],item["memoria"],item["ram"],item["vendible"])

            elif tipo == "Accesorio":
                producto = Accesorio(item["marca"],item["modelo"],item["color"],item["precio"],item["cantidad"],item["vendible"])

            elif tipo == "Audio":
                producto = Audio(item["marca"],item["modelo"],item["color"],item["precio"],item["cantidad"],item["vendible"])

            else:
                producto = Otro(item["marca"],item["modelo"],item["color"],item["precio"],item["cantidad"],item["vendible"])
            self.productos.append(producto)