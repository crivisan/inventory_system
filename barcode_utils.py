import barcode
from barcode.writer import ImageWriter
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BARCODE_DIR = Path("./data/barcodes")
BARCODE_DIR.mkdir(parents=True, exist_ok=True)

def generate_barcode(code: str, label_text: str = ""):
    barcode_class = barcode.get_barcode_class("code128")
    my_code = barcode_class(code, writer=ImageWriter())
    filename = BARCODE_DIR / f"{code}.png"
    my_code.save(filename.with_suffix(""))

    if label_text:
        # add small text below barcode
        img = Image.open(filename)
        W, H = img.size
        new_img = Image.new("RGB", (W, H + 40), "white")
        new_img.paste(img, (0, 0))
        draw = ImageDraw.Draw(new_img)
        try:
            font = ImageFont.truetype("arial.ttf", 16)
        except:
            font = ImageFont.load_default()
        # Compute text width safely
        try:
            w_text = draw.textlength(label_text, font=font)
        except AttributeError:
            # Fallback for older Pillow versions
            w_text, _ = draw.textsize(label_text, font=font)

        draw.text(((W - w_text) / 2, H + 10), label_text, fill="black", font=font)

        new_img.save(filename)
    return filename
