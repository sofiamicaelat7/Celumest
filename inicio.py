import wx


class InicioPanel(wx.Panel):

    def __init__(self, parent, principal):

        super().__init__(parent)

        self.principal = principal

        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.AddStretchSpacer()

        try:

            imagen = wx.Image("fondo.png")

            imagen = imagen.Scale(
                500,
                300,
                wx.IMAGE_QUALITY_HIGH
            )

            logo = wx.StaticBitmap(
                self,
                bitmap=wx.Bitmap(imagen)
            )

            sizer.Add(
                logo,
                0,
                wx.ALIGN_CENTER | wx.ALL,
                10
            )

        except:
            pass

        titulo = wx.StaticText(
            self,
            label="CELUMEST"
        )

        fuente = titulo.GetFont()
        fuente.PointSize = 18
        fuente.MakeBold()

        titulo.SetFont(fuente)

        sizer.Add(
            titulo,
            0,
            wx.ALIGN_CENTER | wx.ALL,
            10
        )

        botones = wx.BoxSizer(wx.HORIZONTAL)

        btn_stock = wx.Button(
            self,
            label="Stock",
            size=(200, 60)
        )

        btn_venta = wx.Button(
            self,
            label="Ventas",
            size=(200, 60)
        )

        btn_stock.Bind(
            wx.EVT_BUTTON,
            lambda evt:
            self.principal.mostrar_sistema("Stock")
        )

        btn_venta.Bind(
            wx.EVT_BUTTON,
            lambda evt:
            self.principal.mostrar_sistema("Venta")
        )

        botones.Add(
            btn_stock,
            0,
            wx.ALL,
            10
        )

        botones.Add(
            btn_venta,
            0,
            wx.ALL,
            10
        )

        sizer.Add(
            botones,
            0,
            wx.ALIGN_CENTER
        )

        sizer.AddStretchSpacer()

        self.SetSizer(sizer)