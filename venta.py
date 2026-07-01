import wx

from nueva_venta import NuevaVentaPanel

class VentaPanel(wx.Panel):

    def __init__(self, parent, principal_app):
        super().__init__(parent)
        self.principal_app = principal_app
        principal = wx.BoxSizer(wx.HORIZONTAL)

        # MENU
        menu = wx.Panel(self)
        menu_sizer = wx.BoxSizer(wx.VERTICAL)
        opciones = ["Nueva Venta"]

        for opcion in opciones:
            btn = wx.Button(menu,label=opcion)
            btn.Bind(wx.EVT_BUTTON,lambda evt, o=opcion:self.mostrar_panel(o))
            menu_sizer.Add(btn,0,wx.EXPAND | wx.ALL,5)

        menu.SetSizer(menu_sizer)

        # AREA DERECHA
        self.area = wx.Panel(self)
        self.area_sizer = wx.BoxSizer(wx.VERTICAL)
        self.paneles = {"Nueva Venta":NuevaVentaPanel(self.area,principal_app)}
        for panel in self.paneles.values():
            self.area_sizer.Add(panel,1,wx.EXPAND | wx.ALL,5)

            panel.Hide()

        self.area.SetSizer(self.area_sizer)

        principal.Add(menu,0,wx.EXPAND | wx.ALL,5)

        principal.Add(self.area,1,wx.EXPAND | wx.ALL,5)
        self.SetSizer(principal)

        # Mostrar panel inicial
        self.mostrar_panel("Nueva Venta")
    def mostrar_panel(self, nombre):
        for panel in self.paneles.values():
            panel.Hide()
        self.paneles[nombre].Show()
        self.area.Layout()
        self.Layout()