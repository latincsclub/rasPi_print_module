from reportlab.pdfgen import canvas
from PIL import Image
import barcode
from barcode.writer import ImageWriter
from flask import Flask, request
from flask_cors import CORS
import cups

conn = cups.Connection()
printers = conn.getPrinters()
printer_name = printers.keys()[0]

app = Flask(__name__)
CORS(app)


def print_file(printer_name):
    conn.printFile(printer_name, "ting.pdf", "Roman Kiosk Server Print", {})


@app.route("/", methods=["GET", "POST"])
def foo():
    jsonified = request.json
    jsonified["total"] = "$" + str(jsonified["total"])
    ordered_items = []
    for key in jsonified:
        if jsonified[key] != 0:
            ordered_items.append(key + ": " + str(jsonified[key]))

    c = canvas.Canvas("ting.pdf", pagesize=(288, 144))
    c.setFont("Helvetica", 10, leading=None)
    c.drawCentredString(144, 117, "ROMAN KIOSK MOBILE ORDER")
    c.setFont("Helvetica", 5, leading=None)
    for i in range(len(ordered_items)):
        xcoord = 17
        ycoord = (117 - 5) - ((10 * (i + 1)))
        c.drawString(17, ycoord, ordered_items[i])

    code39 = barcode.get_barcode_class('code39')
    encoded_name = code39("boi", writer=ImageWriter())
    encoded_name.save("new_file")

    barcode_png = Image.open("new_file.png")
    cropped_barcode = barcode_png.crop((0, 0, barcode_png.size[0], barcode_png.size[1]*.7))
    resized_cropped_barcode = cropped_barcode.thumbnail((72, 72))
    cropped_barcode.save("resized_new_file.png")

    c.drawImage("resized_new_file.png", 108, 0, width=None, height=None)
    c.save()

    print_file(printer_name)

    return "hello"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
