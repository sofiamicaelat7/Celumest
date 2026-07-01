import wx

class NuevaVentaPanel(wx.Panel):
    def __init__(self,parent,principal_app):
        super().__init__(parent)
        self.principal_app = principal_app
        self.carrito = []
        principal = wx.BoxSizer(wx.VERTICAL)
        titulo = wx.StaticText(self,label="Elija los productos")
        principal.Add(titulo,0,wx.ALL,10)
        self.productos = wx.ComboBox(self,style=wx.CB_READONLY)
        principal.Add(self.productos,0,wx.EXPAND | wx.ALL,10)
        principal.Add(wx.StaticText(self,label="Cantidad"),0,wx.LEFT | wx.RIGHT,10)
        self.cantidad = wx.SpinCtrl(self,min=1,max=1000)
        principal.Add(self.cantidad,0,wx.EXPAND | wx.ALL,10)
        btn_agregar = wx.Button(self,label="Agregar al carrito")
        btn_agregar.Bind(wx.EVT_BUTTON,self.agregar_carrito)
        principal.Add(btn_agregar,0,wx.ALL,10)
        self.lista = wx.ListBox(self)
        principal.Add(self.lista,1,wx.EXPAND | wx.ALL,10)
        self.lbl_total = wx.StaticText(self,label="TOTAL: $0")
        principal.Add(self.lbl_total,0,wx.ALL,10)
        botones = wx.BoxSizer(wx.HORIZONTAL)
        btn_finalizar = wx.Button(self,label="Finalizar Compra")
        btn_finalizar.Bind(wx.EVT_BUTTON,self.finalizar_compra)
        btn_cancelar = wx.Button(self,label="Cancelar")
        btn_cancelar.Bind(wx.EVT_BUTTON,self.cancelar_venta)
        botones.Add(btn_finalizar,0,wx.RIGHT,10)
        botones.Add(btn_cancelar,0)
        principal.Add(botones,0,wx.ALL,10)
        self.SetSizer(principal)
        self.cargar_productos()

    def cargar_productos(self):
        self.productos.Clear()
        for producto in self.principal_app.inventario.obtener_todos():
            if not producto.vendible:
                continue
            texto = (f"{producto.marca} "f"{producto.modelo} "f"{producto.memoria} "f"{producto.ram}")
            self.productos.Append(texto)
        if self.productos.GetCount():
            self.productos.SetSelection(0)

    def agregar_carrito(self, event):
        indice = self.productos.GetSelection()
        if indice == wx.NOT_FOUND:
            wx.MessageBox("Seleccione un producto")
            return
        
        producto = None

        contador = -1

        for p in self.principal_app.inventario.obtener_todos():
            if not p.vendible:
                continue
            contador += 1
            
            if contador == indice:
                producto = p
                break

        if producto is None:
            return

        cantidad = self.cantidad.GetValue()

        if cantidad > producto.cantidad:
            wx.MessageBox("No hay stock suficiente")
            return

        self.carrito.append({"producto": producto,"cantidad": cantidad})
        self.lista.Append(f"{producto.marca} "f"{producto.modelo} "f"x{cantidad}")
        self.actualizar_total()

    def actualizar_total(self):
        total = 0
        for item in self.carrito:
            total += (item["producto"].precio* item["cantidad"])
        self.lbl_total.SetLabel(f"TOTAL: ${total:,.0f}")

    def cancelar_venta(self, event):
        self.carrito.clear()
        self.lista.Clear()
        self.actualizar_total()

    def finalizar_compra(self, event):
        if not self.carrito:
            wx.MessageBox("No hay productos en el carrito")
            return

        for item in self.carrito:
            producto = item["producto"]
            cantidad = item["cantidad"]
            producto.cantidad -= cantidad

        self.principal_app.inventario.guardar()
        wx.MessageBox("Venta realizada correctamente")
        self.carrito.clear()
        self.lista.Clear()
        self.actualizar_total()
        self.cargar_productos()