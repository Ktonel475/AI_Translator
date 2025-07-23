import os
from pdf2image import convert_from_path
import easyocr
from tqdm import tqdm

class PDFOCR:
    def __init__(self, languages=None):
        self.languages = languages or ['en']
        self.reader = easyocr.Reader(self.languages, gpu=False)

    def extract_text(self, pdf_path: str) -> str:
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"File not found: {pdf_path}")

        images = convert_from_path(pdf_path)
        all_text = []

        print(f"📄 Reading PDF ({len(images)} pages)...")

        for i, img in enumerate(tqdm(images, desc="🔍 OCR in progress", unit="page")):
            results = self.reader.readtext(img)
            page_text = "\n".join([text for _, text, _ in results])
            all_text.append(f"--- Page {i + 1} ---\n{page_text}")

        return "\n\n".join(all_text)
    
def extract_text(pdf_path: str, languages=None) -> str:
    return PDFOCR(languages).extract_text(pdf_path)