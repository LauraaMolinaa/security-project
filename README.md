# Encryption Demonstrations

This repository provides examples of different encryption and embedding techniques. Currently, two main methods are showcased:

1. **Vigenère Cipher + ASCII Art Steganography**
2. **RSA Asymmetric Encryption (with OAEP Padding)**

We also mention two additional encryption methods commonly used in practice:

3. **AES (Advanced Encryption Standard) - Symmetric Key Encryption**
4. **ECIES (Elliptic Curve Integrated Encryption Scheme) - Asymmetric Key Encryption**

Though the code examples focus on the first two, the README describes all four to give a broader perspective.

## 1. Vigenère Cipher + ASCII Art Embedding

### Overview
This method uses a **Vigenère cipher** to encrypt plaintext using a key, producing a ciphertext of readable ASCII characters. It then hides the ciphertext by converting it into binary form and embedding these bits into ASCII art. Spaces in the ASCII art are replaced with special symbols (`#` for `1` and `*` for `0`) to conceal the encrypted message in plain sight.

### How It Works
- **Encryption:**
  - **Vigenère Cipher:** Uses a repeating key to shift each character of the plaintext within a 95-character ASCII printable range.
  - **Steganography in ASCII Art:** After encryption, the ciphertext is turned into binary. ASCII art generated using `pyfiglet` provides a canvas. Spaces in the art are replaced with `#` and `*` to represent the binary data.

- **Decryption:**
  - **Extract Binary:** Recovers bits from `#` and `*` characters in the provided ASCII art.
  - **Reassemble Encrypted Message:** Converts binary back to the ciphertext.
  - **Vigenère Decryption:** Applies the same key to revert the ciphertext to the original plaintext.

### Use Cases
- **Stealth:** Embed sensitive information in innocuous-looking ASCII art.
- **Fun & Educational:** Great way to learn about classic ciphers and steganography.

## 2. RSA Encryption (with OAEP Padding)

### Overview
**RSA** is an asymmetric encryption method that uses a pair of keys:
- A **public key** for encryption (shared openly).
- A **private key** for decryption (kept secret).

**OAEP (Optimal Asymmetric Encryption Padding)** adds security and randomness to RSA, preventing certain attacks.

### How It Works
- **Key Generation:**  
  - Generates an RSA private key and derives a corresponding public key.
- **Encryption with Public Key:**  
  - Uses the public key and OAEP padding (with SHA-256) to encrypt the plaintext.
  - Produces ciphertext that only the holder of the corresponding private key can decrypt.
- **Decryption with Private Key:**  
  - The private key is used to decrypt the ciphertext, recovering the original plaintext.

### Use Cases
- **Secure Data Transmission:**  
  - Share a public key widely and accept encrypted messages from anyone, decrypting them with your private key.
- **Key Exchange in Larger Systems:**  
  - Often used to securely exchange symmetric keys in larger protocols.

## 3. AES (Advanced Encryption Standard) - Symmetric Key Encryption

Though not implemented in the given code, AES is a widely used symmetric cipher that:
- Uses the **same key** for encryption and decryption.
- Efficient and ideal for encrypting large amounts of data once the key is securely shared.

### Use Cases
- **Data-at-Rest Protection:** Encrypt files, databases, and backups.
- **Performance-Sensitive Environments:** Fast and secure encryption with small keys.

## 4. ECIES (Elliptic Curve Integrated Encryption Scheme)

Also not implemented in the provided code, ECIES is an asymmetric encryption method using elliptic curve cryptography. It:
- Provides strong security with smaller key sizes than RSA.
- Often used in modern secure messaging and low-resource environments.

### Use Cases
- **Mobile and IoT Devices:** Lightweight keys and faster operations.
- **Secure Communication Protocols:** Building blocks for advanced cryptographic protocols.

## Getting Started

### Prerequisites
- **Python 3.6+**
- **Dependencies:**  
  - For Vigenère & ASCII Art: `pyfiglet`
  - For RSA: `cryptography` library
- Install by running:
  ```bash
  pip install pyfiglet cryptography
  ```

### Running the Vigenère + ASCII Art Example
- **Encryption:**
  1. Run the script.
  2. Select encryption mode (`e`).
  3. Enter your plaintext and a key.
  4. The program outputs the ASCII art with the hidden message.

- **Decryption:**
  1. Run the script.
  2. Select decryption mode (`d`).
  3. Paste the ASCII art and enter the key.
  4. The program outputs the recovered plaintext.

### Running the RSA Example (Flask Endpoint)
- A Flask endpoint takes in a plaintext message and returns:
  - **Ciphertext** (Base64-encoded)
  - **Generated Private Key** (PEM)
  - **Public Key** (PEM)
- Another endpoint takes the ciphertext and private key to decrypt back to plaintext.

### Example Commands
- **Encrypt:**
  ```bash
  curl -X POST -H "Content-Type: application/json" \
  -d '{"message":"Hello RSA!"}' \
  http://localhost:5000/encrypt
  ```
- **Decrypt:**
  ```bash
  curl -X POST -H "Content-Type: application/json" \
  -d '{"ciphertext":"<base64>", "private_key":"<pem-key>"}' \
  http://localhost:5000/decrypt
  ```

*(Replace `<base64>` and `<pem-key>` with the values returned during encryption.)*

## Contributing
- Feel free to fork this repository and add other encryption schemes or improve the existing code.
- Issues and pull requests are welcome.

## License
This project is licensed under the [MIT License](LICENSE).

---




Useful commands:

install from requirements.txt: \
  pip install -r requirements.txt

Write to requirements.txt:\
  pip freeze > requirements.txt
