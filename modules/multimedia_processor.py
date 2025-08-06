import PyPDF2
from PIL import Image
import pytesseract
import cv2
import os
from config import TESSERACT_CMD

pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

class MultimediaProcessor:
    def __init__(self):
        if not os.path.exists(pytesseract.pytesseract.tesseract_cmd):
            print(f"Warning: Tesseract-OCR executable not found at {pytesseract.pytesseract.tesseract_cmd}. OCR functionality may not work.")

    def read_pdf(self, file_path):
        """Reads text from a PDF file."""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text += page.extract_text() or ""
            return text
        except FileNotFoundError:
            return f"Error: PDF file not found at {file_path}"
        except Exception as e:
            return f"Error reading PDF: {e}"

    def analyze_image_ocr(self, image_path):
        """Extracts text from an image using OCR."""
        try:
            if not os.path.exists(pytesseract.pytesseract.tesseract_cmd):
                return "OCR not configured. Please set TESSERACT_CMD in config.py to your Tesseract executable path."
            img_cv = cv2.imread(image_path)
            if img_cv is None:
                return f"Error: Could not load image from {image_path}. Check file path and format."
            gray_img = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            _, binary_img = cv2.threshold(gray_img, 150, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            pil_img = Image.fromarray(binary_img)
            text = pytesseract.image_to_string(pil_img, lang='eng+ara')
            if not text.strip():
                return "No text detected in the image. Ensure text is clear and image quality is good."
            return text
        except FileNotFoundError:
            return f"Error: Image file not found at {image_path}"
        except pytesseract.TesseractNotFoundError:
            return "Tesseract executable not found. Please install Tesseract-OCR and set its path in config.py."
        except Exception as e:
            return f"Error analyzing image with OCR: {e}"