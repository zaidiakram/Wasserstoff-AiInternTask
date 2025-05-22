from paddleocr import PaddleOCR
import numpy as np
from concurrent.futures import ThreadPoolExecutor

class DocumentExtractor:
    def __init__(self):
        self.ocr = PaddleOCR(
            use_angle_cls=True,
            lang='en',
            rec_algorithm='SVTR_LCNet',
            enable_mkldnn=True
        )
        self.executor = ThreadPoolExecutor(max_workers=4)

    async def extract_text(self, file_bytes: bytes) -> dict:
        """Unified extraction for both text and OCR"""
        try:
            # Try direct text extraction first
            text = self._extract_text(file_bytes)
            if len(text.strip()) < 50:
                # Fallback to OCR if text seems empty
                return await self._extract_with_ocr(file_bytes)
            return {'text': text, 'method': 'direct'}
        except Exception:
            return await self._extract_with_ocr(file_bytes)

    async def _extract_with_ocr(self, file_bytes: bytes) -> dict:
        """PaddleOCR-specific extraction"""
        images = self._convert_to_images(file_bytes)
        texts = []
        for img in images:
            result = await self._run_ocr(img)
            texts.append("\n".join([line[1][0] for line in result[0]]))
        return {
            'text': "\n\n".join(texts),
            'method': 'paddle_ocr',
            'pages': len(images)
        }