import pyfiglet
import hashlib

# Helper functions for Vigenère Cipher
def vigenere_encrypt(text, key):
    key = (key * ((len(text) // len(key)) + 1))[:len(text)]
    encrypted = ''.join(
        chr(((ord(t) - 32 + ord(k) - 32) % 95) + 32) for t, k in zip(text, key)
    )
    return encrypted + "~END~"  # Add end marker

def vigenere_decrypt(encrypted_text, key):
    if "~END~" not in encrypted_text:
        return "Error: End marker not found. Possible data corruption."
    encrypted_text = encrypted_text.replace("~END~", "")  # Remove end marker
    key = (key * ((len(encrypted_text) // len(key)) + 1))[:len(encrypted_text)]
    decrypted = ''.join(
        chr(((ord(e) - 32 - (ord(k) - 32)) % 95) + 32) for e, k in zip(encrypted_text, key)
    )
    return decrypted

# Generate ASCII art and dynamically expand until sufficient
def generate_dynamic_ascii_art(message="Secure", required_spaces=0):
    fig = pyfiglet.Figlet(font="block")
    ascii_art = fig.renderText(message)
    while ascii_art.count(" ") < required_spaces:
        ascii_art += fig.renderText("Expand")
    return ascii_art

# Embed encrypted message into ASCII art
def embed_message_into_ascii_art(message, ascii_art):
    binary_data = ''.join(f'{ord(char):08b}' for char in message)
    print(f"[DEBUG] Binary data to embed: {binary_data}")

    embedded_art = []
    binary_index = 0

    for line in ascii_art.splitlines():
        embedded_line = ""
        for char in line:
            if binary_index < len(binary_data) and char == " ":
                # Use '#' for binary 1 and '*' for binary 0
                embedded_line += '#' if binary_data[binary_index] == '1' else '*'
                binary_index += 1
            else:
                embedded_line += char
        embedded_art.append(embedded_line)

    if binary_index < len(binary_data):
        raise ValueError("ASCII art is too small to embed the data.")
    return "\n".join(embedded_art)

# Extract message from ASCII art
def extract_message_from_ascii_art(ascii_art):
    binary_data = ""
    for line in ascii_art.splitlines():
        for char in line:
            if char == '#':
                binary_data += '1'
            elif char == '*':
                binary_data += '0'

    if not binary_data:
        raise ValueError("No hidden message found in ASCII art.")

    # Convert binary to text
    message = ''.join(chr(int(binary_data[i:i + 8], 2)) for i in range(0, len(binary_data), 8))
    return message

# Main encryption function
def encrypt_to_ascii_art(message, key):
    encrypted_message = vigenere_encrypt(message, key)
    binary_data = ''.join(f'{ord(char):08b}' for char in encrypted_message)

    # Generate ASCII art dynamically based on required spaces
    ascii_art = generate_dynamic_ascii_art(required_spaces=len(binary_data))
    return embed_message_into_ascii_art(encrypted_message, ascii_art)

# Main decryption function
def decrypt_from_ascii_art(ascii_art, key):
    extracted_message = extract_message_from_ascii_art(ascii_art)
    return vigenere_decrypt(extracted_message, key)

# Main program
if __name__ == "__main__":
    print("Welcome to the ASCII Art Encryptor/Decryptor!")
    mode = input("Enter 'e' to encrypt or 'd' to decrypt: ").strip().lower()

    if mode == 'e':
        plaintext = input("Enter the message to encrypt: ").strip()
        key = input("Enter the encryption key: ").strip()
        try:
            hidden_art = encrypt_to_ascii_art(plaintext, key)
            print("\nHidden ASCII Art:")
            print(hidden_art)
        except ValueError as e:
            print(f"Error: {e}")

    elif mode == 'd':
        print("Paste the ASCII art below (end input by entering a blank line):")
        ascii_art = ""
        while True:
            line = input()
            if line == "":
                break
            ascii_art += line + "\n"
        key = input("Enter the decryption key: ").strip()
        try:
            decrypted_message = decrypt_from_ascii_art(ascii_art.strip(), key)
            print("\nDecrypted Message:")
            print(decrypted_message)
        except ValueError as e:
            print(f"Error: {e}")

    else:
        print("Invalid option. Please choose 'e' to encrypt or 'd' to decrypt.")
