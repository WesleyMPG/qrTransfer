import wx
from io import BytesIO
# from utils import ROOT_DIR, config
from PIL import Image


# DISPLAY_DIR = ROOT_DIR.joinpath('display')


def pillImg_to_texture(img):
    """Converts a PIL.Image into a kivy texture
    """
    img = img.resize((400, 400))
    data = BytesIO()
    img.save(data, format='png')
    data.seek(0)
    kimg_data = BytesIO(data.read())
    return CoreImage(kimg_data, ext='png').texture

 

class QrApp(wx.Frame):
    def __init__(self, code: Image, *args, **kwargs):
        super(QrApp, self).__init__(*args, **kwargs)
        self._code = code
        self._panel = wx.Panel(self)
        self._text_warning = self._make_text_warning()
        self._sizer = self._create_sizer()
        self._sizer.Add(self._text_warning, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 25))
        self._bitmap = self.static_bitmap_from_pil_image(code)
        self._sizer.Add(self._bitmap)

    def _make_text_warning(self):
        text = wx.StaticText(self._panel, label="Don't Close this window until download complete.")
        font = text.GetFont()
        font.PointSize += 5
        font = font.Bold()
        text.SetFont(font)
        return text

    def _create_sizer(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        self._panel.SetSizer(sizer)
        return sizer

    def static_bitmap_from_pil_image(self, pil_image):
        wx_image = wx.Image(pil_image.size[0], pil_image.size[1])
        wx_image.SetData(pil_image.convert("RGB").tobytes())

        bitmap = wx.Bitmap(wx_image)
        static_bitmap = wx.StaticBitmap(self._panel, wx.ID_ANY, wx.NullBitmap)
        static_bitmap.SetBitmap(bitmap)
        return static_bitmap


def qr_window(code, at_close=None):
    """Displays the qrCode window

    Args:
        code (PILL.Image): the qrCode to be displayed
        at_close (function, optional): A function to be executed
            after window close. Defaults to None.
    """
    QrApp(code).run()
    if at_close: at_close()


if __name__ == '__main__':
    img = Image.open('../resources/icon.png')
    app = wx.App()
    frame = QrApp(img, None, title='QrTransfer')
    frame.Show()
    app.MainLoop()
