import paddleocr
from PIL import Image

def extract_text_from_image(image: Image.Image):
    ocr = paddleocr.OCR()
    result = ocr.ocr(image)
    return result
