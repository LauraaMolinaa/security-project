import pyfiglet
import hashlib
import os
import requests
from flask import Flask, request, jsonify, render_template, send_file
from scripts.vigenere import encrypt_to_ascii_art, decrypt_from_ascii_art
from scripts.stegano import generate_image, encode_message, decode_message
from scripts.rsa import rsa_encrypt, rsa_decrypt
from scripts.geo import geo_encryption, geo_decryption
from stegano import lsb
from io import BytesIO

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


# STEGANO ENDPOINTS
@app.route('/stegano/encrypt', methods=['POST'])
def stegano_encrypt():
    secret_message = request.form.get('message')
    prompt = request.form.get('prompt')

    if not secret_message:
        return jsonify({'error': 'Secret message is required'}), 400

    input_image_path = None
    # Check if an image file is uploaded
    if 'image' in request.files:
        image = request.files['image']
        input_image_path = BytesIO(image.read())
    elif prompt:
        # Generate an image from the prompt
        input_image_path = generate_image(prompt)
        if not input_image_path:
            return jsonify({'error': 'Failed to generate image from prompt'}), 400
    else:
        return jsonify({'error': 'Either an image or a prompt is required'}), 400

    # Encode the secret message into the image
    encoded_image = encode_message(input_image_path, secret_message)
    if isinstance(encoded_image, str):
        return jsonify({'error': encoded_image}), 400

    # Return the encoded image to be displayed and optionally saved by the user
    return send_file(encoded_image, mimetype='image/png')


@app.route('/stegano/decrypt', methods=['POST'])
def stegano_decrypt():
    if 'image' not in request.files:
        return jsonify({'error': 'Image is required for decryption'}), 400

    image = request.files['image']
    input_image_path = BytesIO(image.read())

    # Decode the hidden message from the image
    try:
        decoded_message = decode_message(input_image_path)
        return jsonify({'message': decoded_message})
    except Exception as e:
        return jsonify({'error': f'Decryption failed: {str(e)}'}), 500


@app.route('/generate-ai-image', methods=['POST'])
def generate_ai_image():
    data = request.json
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    generated_image = generate_image(prompt)
    if not generated_image:
        return jsonify({'error': 'Failed to generate image'}), 400

    # Return the generated image for the frontend to display
    return send_file(generated_image, mimetype='image/png')


# RSA Endpoints
@app.route('/rsa/encrypt', methods=['POST'])
def rsa_encrypt_endpoint():
    return rsa_encrypt(request)

@app.route('/rsa/decrypt', methods=['POST'])
def rsa_decrypt_endpoint():
    return rsa_decrypt(request)

# GEO endpoints 
@app.route('/geo/encrypt', methods=['POST'])
def geo_encrypt_endpoint():
    return geo_encryption()

@app.route('/geo/decrypt', methods=['POST'])
def geo_decrypt_endpoint():
    return geo_decryption()

if __name__ == '__main__':
    app.run(debug=True)
