from flask import Flask, render_template, request, jsonify, send_file
import os

from pdf_parser import extract_prices
from excel_handler import read_products, write_prices
from matcher import match_products_to_prices

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs('uploads', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    try:
        pdf_file = request.files['pdf']
        excel_file = request.files['excel']
        price_mode = request.form['price_mode']

        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
        excel_path = os.path.join(app.config['UPLOAD_FOLDER'], excel_file.filename)

        pdf_file.save(pdf_path)
        excel_file.save(excel_path)

        price_data = extract_prices(pdf_path)
        products = read_products(excel_path)

        matched_prices, unmatched = match_products_to_prices(products, price_data)
        write_prices(excel_path, matched_prices, price_mode)

        return jsonify({
            'success': True,
            'matched': len(matched_prices),
            'unmatched': len(unmatched),
            'filename': excel_file.filename
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join('uploads', filename), as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
