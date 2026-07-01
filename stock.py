import wx

from formularios import FormularioTelefono
from control_stock import ControlStockPanel


class StockPanel(wx.Panel):

    def __init__(self, parent, principal_app):
        super().__init__(parent)
        self.principal_app = principal_app
        principal = wx.BoxSizer(wx.HORIZONTAL)

        # MENU IZQUIERDO
        menu = wx.Panel(self)
        menu_sizer = wx.BoxSizer(wx.VERTICAL)
        opciones = ["Ingreso Venta","Ingreso No Venta","Control Stock"]

        for opcion in opciones:
            btn = wx.Button(menu,label=opcion)
            btn.Bind(wx.EVT_BUTTON,lambda evt,o=opcion:self.mostrar_panel(o))
            menu_sizer.Add(btn,0,wx.EXPAND | wx.ALL,5)
        menu.SetSizer(menu_sizer)

        # AREA DERECHA
        self.area = wx.Panel(self)
        self.area_sizer = wx.BoxSizer(wx.VERTICAL)

        # FORMULARIO VENDIBLE
        scroll_vendible = wx.ScrolledWindow(self.area)
        scroll_vendible.SetScrollRate(10,10)
        form_vendible = FormularioTelefono(scroll_vendible,principal_app,True)
        sizer_vendible = wx.BoxSizer(wx.VERTICAL)
        sizer_vendible.Add(form_vendible,1,wx.EXPAND | wx.ALL,5)
        scroll_vendible.SetSizer(sizer_vendible)

        # FORMULARIO NO VENDIBLE
        scroll_no_vendible = wx.ScrolledWindow(self.area)
        scroll_no_vendible.SetScrollRate(10,10)
        form_no_vendible = FormularioTelefono(scroll_no_vendible,principal_app,False)
        sizer_no_vendible = wx.BoxSizer(wx.VERTICAL)
        sizer_no_vendible.Add(form_no_vendible,1,wx.EXPAND | wx.ALL,5)
        scroll_no_vendible.SetSizer(sizer_no_vendible)

        # CONTROL STOCK
        control_stock = ControlStockPanel(self.area,principal_app)
        self.paneles = {"Ingreso Venta":scroll_vendible,"Ingreso No Venta":scroll_no_vendible,"Control Stock":control_stock}

        for panel in self.paneles.values():
            self.area_sizer.Add(panel,1,wx.EXPAND | wx.ALL,5)
            panel.Hide()

        self.area.SetSizer(self.area_sizer)
        principal.Add(menu,0,wx.EXPAND | wx.ALL,5)
        principal.Add(self.area,1,wx.EXPAND | wx.ALL,5)
        self.SetSizer(principal)
        self.mostrar_panel("Ingreso Venta")

    # MOSTRAR PANEL
    def mostrar_panel(self, nombre):
        for panel in self.paneles.values():
            panel.Hide()
        self.paneles[nombre].Show()
        self.area.Layout()
        self.Layout()

    # RECREAR FORMULARIOS
    def recrear_formulario(self, vendible):
        if vendible:
            viejo = self.paneles["Ingreso Venta"]
            self.area_sizer.Detach(viejo)
            viejo.Destroy()
            scroll = wx.ScrolledWindow(self.area)
            scroll.SetScrollRate(10,10)
            formulario = FormularioTelefono(scroll,self.principal_app,True)
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(formulario,1,wx.EXPAND | wx.ALL,5)
            scroll.SetSizer(sizer)
            self.paneles["Ingreso Venta"] = scroll
            self.area_sizer.Insert(0,scroll,1,wx.EXPAND | wx.ALL,5)
            self.mostrar_panel("Ingreso Venta")

        else:
            viejo = self.paneles["Ingreso No Venta"]
            self.area_sizer.Detach(viejo)
            viejo.Destroy()
            scroll = wx.ScrolledWindow(self.area)
            scroll.SetScrollRate(10,10)
            formulario = FormularioTelefono(scroll,self.principal_app,False)
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(formulario,1,wx.EXPAND | wx.ALL,5)
            scroll.SetSizer(sizer)
            self.paneles["Ingreso No Venta"] = scroll
            self.area_sizer.Insert(1,scroll,1,wx.EXPAND | wx.ALL,5)
            self.mostrar_panel("Ingreso No Venta")