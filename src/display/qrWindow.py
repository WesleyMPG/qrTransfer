def qr_window(code, at_close=None):
    from kivy.app import App
    from kivy.lang import Builder
    from kivy.uix.widget import Widget
    from kivy.core.window import Window
    from kivy.core.image import Image as CoreImage
    from kivy.uix.image import Image as kImage
    from io import BytesIO
    import os.path as ospath

    kv_file = ospath.dirname(ospath.abspath(__file__))
    kv_file = ospath.join(kv_file, 'kvFiles', 'qrWindow.kv')
    Builder.load_file(kv_file)

    def pillImg_to_texture(img):
        img = img.resize((400, 400))
        data = BytesIO()
        img.save(data, format='png')
        data.seek(0)
        kimg_data = BytesIO(data.read())
        return CoreImage(kimg_data, ext='png').texture

    class QrFrame(Widget):
        def __init__(self, code, **kwargs):
            super(QrFrame, self).__init__(**kwargs)
            self.ids.txt.text = "DON'T close this window\n"+ \
                                "until download complete"
            self.ids.img.texture = pillImg_to_texture(code)

    class QrApp(App):
        def __init__(self, code, **kwargs):
            super(QrApp, self).__init__(**kwargs)
            self._code = code

        def build(self):
            Window.clearcolor = (.1, .1, .1, 1)
            self.icon = ospath.join('resources', 'icon.png')
            return QrFrame(self._code)

    Window.size = (400, 500)
    QrApp(code).run()
    if at_close: at_close()


if __name__ == '__main__':
    from PIL import Image
    img = Image.open('../resources/icon.png')
    qr_window(img)
