import barcode
from barcode.writer import ImageWriter
from pathlib import Path

BARCODE_DIR = Path("./data/barcodes")
BARCODE_DIR.mkdir(parents=True, exist_ok=True)

def generate_barcode(code: str):
    """Generate a Code128 barcode image and save it to /data/barcodes/"""
    barcode_class = barcode.get_barcode_class('code128')
    my_code = barcode_class(code, writer=ImageWriter())
    filename = BARCODE_DIR / f"{code}.png"
    my_code.save(filename.with_suffix(''))
    return filename
