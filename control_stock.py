import wx

from modelo import Telefono

class ControlStockPanel(wx.Panel):
    def __init__(self, parent, principal_app):
        super().__init__(parent)
        self.principal_app = principal_app
        principal = wx.BoxSizer(wx.VERTICAL)

# TITULO
        titulo = wx.StaticText(self,label="Control de Stock")
        fuente = titulo.GetFont()
        fuente.PointSize += 4
        fuente.MakeBold()
        titulo.SetFont(fuente)
        principal.Add(titulo,0,wx.ALL,10)

        # BUSQUEDA
        busqueda = wx.BoxSizer(wx.HORIZONTAL)
        busqueda.Add(wx.StaticText(self,label="Buscar"),0,wx.ALIGN_CENTER_VERTICAL | wx.RIGHT,5)
        self.txt_busqueda = wx.TextCtrl(self)
        busqueda.Add(self.txt_busqueda,1)
        principal.Add(busqueda,0,wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM,10)

        # FILTROS
        filtros = wx.BoxSizer(wx.HORIZONTAL)
        filtros.Add(wx.StaticText(self,label="Marca"),0,wx.ALIGN_CENTER_VERTICAL | wx.RIGHT,5)
        self.filtro_marca = wx.ComboBox(self,style=wx.CB_READONLY)
        filtros.Add(self.filtro_marca,0,wx.RIGHT,15)
        filtros.Add(wx.StaticText(self,label="Modelo"),0,wx.ALIGN_CENTER_VERTICAL | wx.RIGHT,5)
        self.filtro_modelo = wx.ComboBox(self,style=wx.CB_READONLY)
        filtros.Add(self.filtro_modelo,0,wx.RIGHT,15)
        filtros.Add(wx.StaticText(self,label="Color"),0,wx.ALIGN_CENTER_VERTICAL | wx.RIGHT,5)
        self.filtro_color = wx.ComboBox(self,style=wx.CB_READONLY)
        filtros.Add(self.filtro_color,0,wx.RIGHT,15)
        btn_filtrar = wx.Button(self,label="Filtrar")
        btn_filtrar.Bind(wx.EVT_BUTTON,self.actualizar_tabla)
        filtros.Add(btn_filtrar)
        principal.Add(filtros,0,wx.ALL,10)

        # RESUMEN
        self.lbl_resumen = wx.StaticText(self,label="")
        principal.Add(self.lbl_resumen,0,wx.LEFT | wx.RIGHT | wx.BOTTOM,10)

        # TABLA
        self.lista = wx.ListCtrl(self,style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        columnas = [("Marca", 120),("Modelo", 120),("Color", 100),("Memoria", 100),("RAM", 100),("Cantidad", 80),("Precio", 100),("Vendible", 80)]
        for i, (texto, ancho) in enumerate(columnas):
            self.lista.InsertColumn(i,texto,width=ancho)
        principal.Add(self.lista,1,wx.EXPAND | wx.ALL,10)

        # BOTONES
        botones = wx.BoxSizer(wx.HORIZONTAL)
        btn_actualizar = wx.Button(self,label="Actualizar")
        btn_actualizar.Bind(wx.EVT_BUTTON,self.actualizar_tabla)
        botones.Add(btn_actualizar,0,wx.RIGHT,10)
        btn_eliminar = wx.Button(self,label="Eliminar")
        btn_eliminar.Bind(wx.EVT_BUTTON,self.eliminar_producto)
        botones.Add(btn_eliminar,0,wx.RIGHT,10)
        btn_modificar = wx.Button(self,label="Modificar")
        btn_modificar.Bind(wx.EVT_BUTTON,self.modificar_producto)
        botones.Add(btn_modificar,0)
        principal.Add(botones,0,wx.ALL,10)
        self.SetSizer(principal)
        self.filtro_marca.Bind(wx.EVT_COMBOBOX,self.actualizar_modelos)
        self.filtro_modelo.Bind(wx.EVT_COMBOBOX,self.actualizar_colores)
        self.cargar_filtros()
        self.actualizar_tabla()

    # FILTROS
    def cargar_filtros(self):
        self.filtro_marca.Clear()
        self.filtro_marca.Append("Todos")
        marcas = set()
        for producto in self.principal_app.inventario.obtener_todos():
            marcas.add(producto.marca)
        for marca in sorted(marcas):
            self.filtro_marca.Append(marca)
        self.filtro_marca.SetSelection(0)
        self.actualizar_modelos()

    def actualizar_modelos(self, event=None):
        marca = self.filtro_marca.GetValue()
        self.filtro_modelo.Clear()
        self.filtro_modelo.Append("Todos")
        modelos = set()
        for producto in self.principal_app.inventario.obtener_todos():
            if marca == "Todos" or producto.marca == marca:
                modelos.add(producto.modelo)
        for modelo in sorted(modelos):
            self.filtro_modelo.Append(modelo)
        self.filtro_modelo.SetSelection(0)
        self.actualizar_colores()

    def actualizar_colores(self, event=None):
        marca = self.filtro_marca.GetValue()
        modelo = self.filtro_modelo.GetValue()
        self.filtro_color.Clear()
        self.filtro_color.Append("Todos")
        colores = set()
        for producto in self.principal_app.inventario.obtener_todos():
            if marca != "Todos" and producto.marca != marca:
                continue
            if modelo != "Todos" and producto.modelo != modelo:
                continue
            colores.add(producto.color)
        for color in sorted(colores):
            self.filtro_color.Append(color)
        self.filtro_color.SetSelection(0)

    # TABLA
    def actualizar_tabla(self, event=None):
        self.lista.DeleteAllItems()
        marca = self.filtro_marca.GetValue()
        modelo = self.filtro_modelo.GetValue()
        color = self.filtro_color.GetValue()
        texto = (self.txt_busqueda.GetValue().lower().strip())
        total_productos = 0
        total_unidades = 0
        valor_total = 0

        for producto in self.principal_app.inventario.obtener_todos():
            if texto:
                contenido = (f"{producto.marca} "f"{producto.modelo} "f"{producto.color}").lower()
                if texto not in contenido:
                    continue
            if marca != "Todos" and marca and producto.marca != marca:
                continue
            if modelo != "Todos" and modelo and producto.modelo != modelo:
                continue
            if color != "Todos" and color and producto.color != color:
                continue
            total_productos += 1
            total_unidades += producto.cantidad
            valor_total += producto.precio * producto.cantidad
            fila = self.lista.InsertItem(self.lista.GetItemCount(),producto.marca)
            self.lista.SetItem(fila, 1, producto.modelo)
            self.lista.SetItem(fila, 2, producto.color)
            self.lista.SetItem(fila, 3, producto.memoria)
            self.lista.SetItem(fila, 4, producto.ram)
            self.lista.SetItem(fila, 5, str(producto.cantidad))
            self.lista.SetItem(fila, 6, str(producto.precio))
            self.lista.SetItem(fila,7,"Si" if producto.vendible else "No")
        self.lbl_resumen.SetLabel(f"Productos: {total_productos} | "f"Unidades: {total_unidades} | "f"Valor Inventario: ${valor_total:,.0f}")

    # MODIFICAR
    def modificar_producto(self, event):
        fila = self.lista.GetFirstSelected()
        if fila == -1:
            wx.MessageBox("Seleccione un producto")
            return

        marca = self.lista.GetItemText(fila, 0)
        modelo = self.lista.GetItemText(fila, 1)
        color = self.lista.GetItemText(fila, 2)
        producto_encontrado = None
        for producto in self.principal_app.inventario.obtener_todos():
            if (producto.marca == marca and producto.modelo == modelo and producto.color == color):
                producto_encontrado = producto
                break
        if not producto_encontrado:
            return
        dlg = wx.TextEntryDialog(self,"Nueva cantidad",value=str(producto_encontrado.cantidad))
        if dlg.ShowModal() == wx.ID_OK:
            try:
                producto_encontrado.cantidad = int(dlg.GetValue())
            except:
                wx.MessageBox("Cantidad inválida")

        dlg.Destroy()
        dlg = wx.TextEntryDialog(self,"Nuevo precio",value=str(producto_encontrado.precio))
        if dlg.ShowModal() == wx.ID_OK:
            try:
                producto_encontrado.precio = float(dlg.GetValue())
            except:
                wx.MessageBox("Precio inválido")
        dlg.Destroy()
        self.principal_app.inventario.guardar()
        self.actualizar_tabla()
        wx.MessageBox("Producto actualizado")

    # ELIMINAR
    def eliminar_producto(self, event):
        fila = self.lista.GetFirstSelected()
        if fila == -1:
            wx.MessageBox("Seleccione un producto")
            return

        marca = self.lista.GetItemText(fila, 0)
        modelo = self.lista.GetItemText(fila, 1)
        color = self.lista.GetItemText(fila, 2)
        respuesta = wx.MessageBox(f"¿Eliminar {marca} {modelo}?","Confirmar",wx.YES_NO | wx.ICON_QUESTION)
        if respuesta != wx.YES:
            return
        for producto in self.principal_app.inventario.obtener_todos():
            if (producto.marca == marca and producto.modelo == modelo and producto.color == color):
                self.principal_app.inventario.eliminar(producto)
                break
        self.cargar_filtros()
        self.actualizar_tabla()
        wx.MessageBox("Producto eliminado")