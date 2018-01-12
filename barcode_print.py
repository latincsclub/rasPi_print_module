import cups
import barcode
from barcode.writer import ImageWriter
from PIL import Image
from flask import Flask, request, jsonify

conn = cups.Connection()
printers = conn.getPrinters()
printer_name = printers.keys()[0]

app = Flask(__name__)

def mk_barcode_save(barcoded_thing, save_fname):
    code39 = barcode.get_barcode_class('code39')
    encoded_name = code39(barcoded_thing, writer=ImageWriter())
    encoded_name.save('new_file')

def print_file(printer_name, save_fname):
    conn.printFile(printer_name, 'new_file.png', 'Roman Kiosk Server Print', {})


@app.route('/', methods=['GET', 'POST'])
def bar():
    jsonified = request.json
    ting = jsonified['text']
    mk_barcode_save(ting, 'new_file')
    print_file(printer_name, 'new_file.png')
    return 'Thanks!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

