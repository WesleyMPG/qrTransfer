from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image as kImage
from PIL import Image
from io import BytesIO
from utils import get_program_dir


Window.size = (400, 500)

kv = Builder.load_string("""
#:kivy 1.11.0

<QrFrame>
    BoxLayout:
        orientation: 'vertical'
        size: root.width, root.height
        Label:
            id: txt
            text: "DON"
            font_size: 22
            size_hint: (1, .2)
            canvas.before:
                Color:
                    rgba: 1, .4, .4, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
        Image:
            id: img
            size_hint: (1, .8)

""")


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
        return QrFrame(self._code)


def window(code, at_close=None):
    QrApp(code).run()
    if at_close: at_close()


if __name__ == '__main__':
    img = Image.open('./resources/logo.png')
    QrApp(img).run()
