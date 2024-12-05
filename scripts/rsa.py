import base64
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from flask import jsonify

def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    return private_key, public_key

def rsa_encrypt(request):
    data = request.json
    message = data.get('message')

    if not message:
        return jsonify({'error': 'Message is required for encryption'}), 400

    private_key, public_key = generate_key_pair()

    ciphertext = public_key.encrypt(
        message.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')

    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')

    return jsonify({
        'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
        'private_key': private_key_pem,
        'public_key': public_key_pem
    })

def rsa_decrypt(request):
    data = request.json
    ciphertext = data.get('ciphertext')
    private_key_pem = data.get('private_key')

    if not ciphertext or not private_key_pem:
        return jsonify({'error': 'Ciphertext and private key are required for decryption'}), 400

    private_key = serialization.load_pem_private_key(
        private_key_pem.encode('utf-8'),
        password=None,
    )

    ciphertext_bytes = base64.b64decode(ciphertext)
    plaintext = private_key.decrypt(
        ciphertext_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return jsonify({'plaintext': plaintext.decode('utf-8')})
