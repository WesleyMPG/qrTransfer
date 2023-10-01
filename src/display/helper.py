from io import BytesIO
from kivy.core.image import Image as CoreImage


def pillImg_to_texture(img):
    """Converts a PIL.Image into a kivy texture
    """
    img = img.resize((400, 400))
    data = BytesIO()
    img.save(data, format='png')
    data.seek(0)
    kimg_data = BytesIO(data.read())
    return CoreImage(kimg_data, ext='png').texture
