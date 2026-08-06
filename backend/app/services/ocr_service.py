import cv2
import re

from paddleocr import PaddleOCR


class OCRService:

    def __init__(self):

        self.ocr = PaddleOCR(
            use_angle_cls=True,
            lang="en",
            show_log=False,
        )

    def read_plate(self, plate_crop):

        if plate_crop is None:
            return None

        image = self.preprocess(plate_crop)

        result = self.ocr.ocr(image)

        if not result:
            return None

        text = ""

        for line in result:

            if line is None:
                continue

            for item in line:

                if item is None:
                    continue

                text += item[1][0] + " "

        text = text.strip()

        text = self.clean_text(text)

        if len(text) < 3:
            return None

        return text

    def preprocess(self, image):

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY,
        )

        gray = cv2.resize(
            gray,
            None,
            fx=2,
            fy=2,
            interpolation=cv2.INTER_CUBIC,
        )

        gray = cv2.GaussianBlur(
            gray,
            (3, 3),
            0,
        )

        _, thresh = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU,
        )

        return thresh

    def clean_text(self, text):

        text = text.upper()

        text = re.sub(
            r"[^A-Z0-9]",
            "",
            text,
        )

        return text