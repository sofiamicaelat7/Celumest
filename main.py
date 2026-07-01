import wx
import wx.aui as aui
import wx.adv

from modelo import Inventario
from catalogo import Catalogo
from stock import StockPanel
from venta import VentaPanel

class VentanaPrincipal(wx.Frame):
    def __init__(self):
        super().__init__(None,title="Celumest",size=(1200, 700))

        # DATOS COMPARTIDOS
        self.inventario = Inventario()
        self.catalogo = Catalogo()
        panel = wx.Panel(self)

        # LOGO
        imagen = wx.Image("celumest.png",wx.BITMAP_TYPE_ANY)
        imagen = imagen.Scale(80,80,wx.IMAGE_QUALITY_HIGH)
        logo = wx.StaticBitmap(panel,bitmap=wx.Bitmap(imagen))

        # BOTONES
        btn_stock = wx.Button(panel,label="Stock")
        btn_venta = wx.Button(panel,label="Venta")
        btn_stock.Bind(wx.EVT_BUTTON,lambda evt: self.abrir("Stock"))
        btn_venta.Bind(wx.EVT_BUTTON,lambda evt: self.abrir("Venta"))

        # CABECERA
        cabecera = wx.BoxSizer(wx.HORIZONTAL)
        cabecera.Add(logo,0,wx.ALL | wx.ALIGN_CENTER_VERTICAL,10)
        cabecera.AddSpacer(20)
        cabecera.Add(btn_stock,1,wx.ALL | wx.ALIGN_CENTER_VERTICAL,5)
        cabecera.Add(btn_venta,1,wx.ALL | wx.ALIGN_CENTER_VERTICAL,5)

        # NOTEBOOK
        self.notebook = aui.AuiNotebook(panel,style=aui.AUI_NB_CLOSE_ON_ALL_TABS|aui.AUI_NB_TAB_MOVE)

        # LAYOUT
        principal = wx.BoxSizer(wx.VERTICAL)
        principal.Add(cabecera,0,wx.EXPAND)
        principal.Add(self.notebook,1,wx.EXPAND | wx.ALL,5)
        panel.SetSizer(principal)

        # MENU ABOUT
        barra = wx.MenuBar()
        menu_ayuda = wx.Menu()
        item_about = menu_ayuda.Append(wx.ID_ABOUT,"Acerca de")
        self.Bind(wx.EVT_MENU,self.mostrar_about,item_about)
        barra.Append(menu_ayuda,"Ayuda")
        self.SetMenuBar(barra)
        self.Centre()

    # ABOUT
    def mostrar_about(self, event):
        info = wx.adv.AboutDialogInfo()
        info.SetName("Celumest")
        info.SetDescription(
            "Sistema de gestión de stock y ventas de teléfonos celulares.\n\n"
            "Materia: Programación Orientada a Objetos\n"
            "Profesor: Javier Castrillo")
        info.SetDevelopers(["Maidana Angel","Martinez Melanie","Torres Sofia","Donato Diaz Cardozo"])
        wx.adv.AboutBox(info)

    # VERIFICAR PESTAÑA
    def existe(self, nombre):
        for i in range(self.notebook.GetPageCount()):
            if (self.notebook.GetPageText(i)== nombre):
                self.notebook.SetSelection(i)
                return True
        return False

    # ABRIR PESTAÑA
    def abrir(self, nombre):
        if self.existe(nombre):
            return
        if nombre == "Stock":
            pagina = StockPanel(self.notebook,self)
        else:
            pagina = VentaPanel(self.notebook,self)
        self.notebook.AddPage(pagina,nombre,True)

if __name__ == "__main__":
    app = wx.App()
    imagen = wx.Image("celumest.png")
    imagen = imagen.Scale(1200,700,wx.IMAGE_QUALITY_HIGH)
    bitmap = wx.Bitmap(imagen)
    splash = wx.adv.SplashScreen(bitmap,wx.adv.SPLASH_CENTRE_ON_SCREEN|wx.adv.SPLASH_TIMEOUT,3000,None,-1)
    wx.Yield()
    wx.MilliSleep(3000)
    ventana = VentanaPrincipal()
    ventana.Show()
    app.MainLoop()