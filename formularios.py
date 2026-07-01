import wx

from modelo import Telefono

class FormularioTelefono(wx.Panel):
    def __init__(self, parent, principal_app, vendible):
        super().__init__(parent)
        self.principal_app = principal_app
        self.vendible = vendible
        catalogo = principal_app.catalogo
        principal = wx.BoxSizer(wx.VERTICAL)

        # MARCA
        principal.Add(wx.StaticText(self, label="Marca"))
        fila_marca = wx.BoxSizer(wx.HORIZONTAL)
        self.marca = wx.ComboBox(self,choices=catalogo.marcas,style=wx.CB_READONLY)
        self.marca.Bind(wx.EVT_COMBOBOX,self.actualizar_modelos)
        btn_marca = wx.Button(self,label="+",size=(40, -1))
        btn_marca.Bind(wx.EVT_BUTTON,self.nueva_marca)
        fila_marca.Add(self.marca,1,wx.RIGHT,5)
        fila_marca.Add(btn_marca)
        principal.Add(fila_marca,0,wx.EXPAND | wx.ALL,5)

        # MODELO
        principal.Add(wx.StaticText(self, label="Modelo"))
        fila_modelo = wx.BoxSizer(wx.HORIZONTAL)
        self.modelo = wx.ComboBox(self,choices=[],style=wx.CB_READONLY)
        btn_modelo = wx.Button(self,label="+",size=(40, -1))
        btn_modelo.Bind(wx.EVT_BUTTON,self.nuevo_modelo)
        fila_modelo.Add(self.modelo,1,wx.RIGHT,5)
        fila_modelo.Add(btn_modelo)
        principal.Add(fila_modelo,0,wx.EXPAND | wx.ALL,5)

        # COLOR
        principal.Add(wx.StaticText(self, label="Color"))
        fila_color = wx.BoxSizer(wx.HORIZONTAL)
        self.color = wx.ComboBox(self,choices=catalogo.colores,style=wx.CB_READONLY)
        btn_color = wx.Button(self,label="+",size=(40, -1))
        btn_color.Bind(wx.EVT_BUTTON,self.nuevo_color)
        fila_color.Add(self.color,1,wx.RIGHT,5)
        fila_color.Add(btn_color)
        principal.Add(fila_color,0,wx.EXPAND | wx.ALL,5)

        # MEMORIA
        principal.Add(wx.StaticText(self, label="Memoria"))
        fila_memoria = wx.BoxSizer(wx.HORIZONTAL)
        self.memoria = wx.ComboBox(self,choices=catalogo.memorias,style=wx.CB_READONLY)
        btn_memoria = wx.Button(self,label="+",size=(40, -1))
        btn_memoria.Bind(wx.EVT_BUTTON,self.nueva_memoria)
        fila_memoria.Add(self.memoria,1,wx.RIGHT,5)
        fila_memoria.Add(btn_memoria)
        principal.Add(fila_memoria,0,wx.EXPAND | wx.ALL,5)

        # RAM
        principal.Add(wx.StaticText(self, label="RAM"))
        fila_ram = wx.BoxSizer(wx.HORIZONTAL)
        self.ram = wx.ComboBox(self,choices=catalogo.rams,style=wx.CB_READONLY)
        btn_ram = wx.Button(self,label="+",size=(40, -1))
        btn_ram.Bind(wx.EVT_BUTTON,self.nueva_ram)
        fila_ram.Add(self.ram,1,wx.RIGHT,5)
        fila_ram.Add(btn_ram)
        principal.Add(fila_ram,0,wx.EXPAND | wx.ALL,5)

        # PRECIO
        principal.Add(wx.StaticText(self, label="Precio"))
        self.precio = wx.SpinCtrlDouble(self,min=0,max=100000000)
        principal.Add(self.precio,0,wx.EXPAND | wx.ALL,5)

        # CANTIDAD
        principal.Add(wx.StaticText(self, label="Cantidad"))
        self.cantidad = wx.SpinCtrl(self,min=1,max=10000)
        principal.Add(self.cantidad,0,wx.EXPAND | wx.ALL,5)
        btn_guardar = wx.Button(self,label="Guardar")
        btn_guardar.Bind(wx.EVT_BUTTON,self.guardar)
        principal.Add(btn_guardar,0,wx.ALL,10)
        self.SetSizer(principal)

    # CATALOGO
    def actualizar_modelos(self, event):
        marca = self.marca.GetValue()
        modelos = self.principal_app.catalogo.modelos.get(marca,[])
        self.modelo.Clear()
        self.modelo.AppendItems(modelos)

    def nueva_marca(self, event):
        dlg = wx.TextEntryDialog(self,"Ingrese el nombre de la nueva marca:","Agregar Marca")

        if dlg.ShowModal() == wx.ID_OK:
            marca = dlg.GetValue().strip()

            if marca:
                self.principal_app.catalogo.agregar_marca(marca)
                self.marca.Append(marca)
                self.marca.SetValue(marca)

        dlg.Destroy()

    def nuevo_modelo(self, event):
        marca = self.marca.GetValue()

        if not marca:
            wx.MessageBox("Seleccione una marca","Marca requerida")
            return

        dlg = wx.TextEntryDialog(self,f"Ingrese el nuevo modelo para {marca}:","Agregar Modelo")

        if dlg.ShowModal() == wx.ID_OK:
            modelo = dlg.GetValue().strip()

            if modelo:
                self.principal_app.catalogo.agregar_modelo(marca,modelo)
                self.actualizar_modelos(None)
                self.modelo.SetValue(modelo)
        dlg.Destroy()

    def nuevo_color(self, event):
        self.agregar_catalogo("Ingrese el nuevo color:","Agregar Color",self.principal_app.catalogo.agregar_color,self.color)

    def nueva_memoria(self, event):
        self.agregar_catalogo("Ingrese la nueva memoria:","Agregar Memoria",self.principal_app.catalogo.agregar_memoria,self.memoria)

    def nueva_ram(self, event):
        self.agregar_catalogo("Ingrese la nueva RAM:","Agregar RAM",self.principal_app.catalogo.agregar_ram,self.ram)

    def agregar_catalogo(self,mensaje,titulo,metodo,combo):
        dlg = wx.TextEntryDialog(self,mensaje,titulo)

        if dlg.ShowModal() == wx.ID_OK:
            valor = dlg.GetValue().strip()

            if valor:
                metodo(valor)
                combo.Append(valor)
                combo.SetValue(valor)
        dlg.Destroy()

    # LIMPIAR
    def limpiar_formulario(self):
        self.marca.SetSelection(wx.NOT_FOUND)
        self.modelo.Clear()
        self.modelo.SetSelection(wx.NOT_FOUND)
        self.color.SetSelection(wx.NOT_FOUND)
        self.memoria.SetSelection(wx.NOT_FOUND)
        self.ram.SetSelection(wx.NOT_FOUND)
        self.precio.SetValue(0)
        self.cantidad.SetValue(1)
        self.Refresh()
        self.Update()

    # GUARDAR
    def guardar(self, event):

        producto = Telefono(
            self.marca.GetValue(),
            self.modelo.GetValue(),
            self.color.GetValue(),
            self.precio.GetValue(),
            self.cantidad.GetValue(),
            self.memoria.GetValue(),
            self.ram.GetValue(),
            self.vendible)

        self.principal_app.inventario.agregar(producto)
        wx.MessageBox("Producto guardado correctamente","Alta de Producto")

        self.limpiar_formulario()