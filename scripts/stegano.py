import os
import requests
from stegano import lsb
from io import BytesIO

def generate_image(prompt):
    """
    Generates an image based on a text prompt using Pollinations.AI.
    Returns the image data as a BytesIO object.
    """
    # Construct API URL, replacing spaces with '%20' for URL compatibility
    api_url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}"
    try:
        # Send GET request to the Pollinations.AI API
        response = requests.get(api_url, stream=True)
        if response.status_code == 200:
            # Return the image data as a BytesIO object
            image_data = BytesIO(response.content)
            return image_data
        else:
            print(f"Failed to generate image. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Pollinations.AI: {e}")
        return None

# Function to encode a secret message into an image
def encode_message(input_image_path, output_image_path, secret_message):
    """
    Encodes a secret message into an image using the Stegano library.
    Saves the new image with the hidden message.
    """
    try:
        # Use Stegano's LSB method to hide the message
        secret_image = lsb.hide(input_image_path, secret_message)
        # Save the modified image to the specified path
        secret_image.save(output_image_path)
        print(f"Message encoded and saved as '{output_image_path}'")
    except Exception as e:
        print(f"Error during encoding: {e}")

# Function to decode a secret message from an image
def decode_message(image_path):
    """
    Decodes a hidden message from an image using the Stegano library.
    Prints the decoded message if found.
    """
    try:
        # Extract the hidden message from the image
        secret_message = lsb.reveal(image_path)
        if secret_message:
            print(f"Decoded message: {secret_message}")
        else:
            print("No hidden message found in the image.")
    except Exception as e:
        print(f"Error during decoding: {e}")

# Main function with user interaction
def main():
    """
    Main program logic for encoding or decoding messages in images.
    Provides options to generate images, encode messages, or decode messages.
    """
    # Ask the user if they want to encode or decode a message
    choice = input("Do you want to encode or decode a message? (Enter 'encode' or 'decode'): ").strip().lower()
    
    if choice == 'encode':
        # Check if the user wants to generate an image or use an existing one
        use_generated_image = input("Do you want to generate an image using a text prompt? (yes/no): ").strip().lower()
        if use_generated_image == 'yes':
            # Prompt the user to enter a description for image generation
            prompt = input("Enter a text prompt to generate the image: ").strip()
            input_image_path = generate_image(prompt)
            if not input_image_path:  # Ensure the image was successfully generated
                print("Image generation failed. Exiting.")
                return
        else:
            # Ask the user to provide the path to an existing image
            input_image_path = input("Enter the path to the image you want to use: ").strip()
            if not os.path.isfile(input_image_path):  # Validate the file path
                print("Invalid image path. Exiting.")
                return
        
        # Ask the user for a directory to save the new image
        output_directory = input("Enter the directory to save the encoded image: ").strip()
        if not os.path.isdir(output_directory):  # Validate the directory path
            print("Invalid directory path. Exiting.")
            return
        # Define the full path for the output image
        output_image_path = os.path.join(output_directory, 'encoded_image.png')
        
        # Ask the user to enter the secret message
        secret_message = input("Enter the secret message to hide: ").strip()
        # Encode the message into the image
        encode_message(input_image_path, output_image_path, secret_message)
    
    elif choice == 'decode':
        # Ask the user to provide the path to the image for decoding
        image_path = input("Enter the path of the image to decode: ").strip()
        if not os.path.isfile(image_path):  # Validate the file path
            print("Invalid image path. Exiting.")
            return
        # Decode and display the hidden message
        decode_message(image_path)
    
    else:
        print("Invalid choice. Please enter 'encode' or 'decode'.")

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
