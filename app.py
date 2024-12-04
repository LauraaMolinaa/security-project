from flask import Flask, render_template, request, jsonify, send_file
from scripts.vigenere import encrypt_to_ascii_art, decrypt_from_ascii_art
import os
import os
from werkzeug.utils import secure_filename
from scripts.stegano import encode_message, decode_message, generate_image


UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/image-operation', methods=['POST'])
def image_operation():
    action = request.form.get("action")
    file = request.files.get("file")

    if not file or action != "encrypt":
        return jsonify({"error": "Invalid request"}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
    file.save(filepath)

    try:
        if action == "encrypt":
            # Placeholder for save directory; replace this with your logic
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], "encoded_image.png")
            encode_message(filepath, output_path, "Secret message")
            return jsonify({"message": "Image encoded successfully!", "outputPath": output_path})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/generate-image', methods=['GET'])
def generate_image_endpoint():
    from scripts.stegano import generate_image  # Adjust import path as needed

    # Get the prompt from query parameters or use a default
    prompt = request.args.get("prompt", "A beautiful landscape")
    image_data = generate_image(prompt)

    if image_data is None:
        return jsonify({"error": "Failed to generate image"}), 500

    # Serve the image data as a file
    return send_file(image_data, mimetype='image/png')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json
    message = data.get('message')
    key = data.get('key')
    if not message or not key:
        return jsonify({"error": "Missing message or key"}), 400

    try:
        ascii_art = encrypt_to_ascii_art(message, key)
        return jsonify({"ascii_art": ascii_art})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request. Ensure JSON is sent."}), 400

    ascii_art = data.get('ascii_art')
    key = data.get('key')

    if not ascii_art and not data.get('message'):
        return jsonify({"error": "Missing 'ascii_art' or 'message' in the payload"}), 400
    if not key:
        return jsonify({"error": "Missing 'key' in the payload"}), 400

    try:
        if ascii_art:
            message = decrypt_from_ascii_art(ascii_art, key)
        else:
            message = decrypt_from_ascii_art(data.get('message'), key)

        return jsonify({"message": message})
    except Exception as e:
        return jsonify({"error": f"Decryption failed: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
