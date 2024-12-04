from flask import Flask, request, jsonify, render_template
import pyfiglet
import hashlib
from scripts.vigenere import encrypt_to_ascii_art, decrypt_from_ascii_art

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# VIGINERE CIPHER ENDPOINTS
@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json
    message = data.get('message')
    key = data.get('key')

    if not message or not key:
        return jsonify({'error': 'Message and key are required'}), 400

    try:
        ascii_art = encrypt_to_ascii_art(message, key)
        return jsonify({'ascii_art': ascii_art})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    ascii_art = data.get('ascii_art')
    key = data.get('key')

    if not ascii_art or not key:
        return jsonify({'error': 'ASCII art and key are required'}), 400

    try:
        decrypted_message = decrypt_from_ascii_art(ascii_art, key)
        return jsonify({'decrypted_message': decrypted_message})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
