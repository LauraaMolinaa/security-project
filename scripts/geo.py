
import pip._vendor.requests 
from flask import jsonify
import random
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import os
import ast

def geo_encryption():
  payload = {}
  headers= {
    "apikey": "0kyJpyoUHDRbexeoyYNOuakAo8QzfkmX"
  }

  country_codes_list: list = [
      "ven", "arm", "atg", "bhs", "can", "chn", "dza", "flk", "jam", "ita", "lby", "maf", "mli", "nzl", "pan", "sgp", "slv", "zaf" 
  ]

  country: str = random.choice(country_codes_list)
  
  url = "https://api.apilayer.com/geo/country/code/"+country

  response = pip._vendor.requests.request("GET", url, headers=headers, data = payload)

  if response.status_code >= 400:
    return jsonify({'error': 'An error occured while getting the capital city. Status code:'+response.status_code})
  
  # starting encryption
  response_data = response.json()

  capital = response_data[0].get("capital")

  if capital is None:
    return jsonify({'error': 'Capital city is '+capital}), 404


  secret_data = data_to_ascii(capital)
  
  salt = os.urandom(32)
  secret_data_bytes = secret_data.encode('utf-8') + salt

  # using  a 16 byte key which is equivalent to a 128 bit key 
  key = get_random_bytes(16)
  cipher_encrypt = AES.new(key, AES.MODE_EAX)

  # converting the secret data to bytes 
  ciphertext = cipher_encrypt.encrypt(secret_data_bytes)
  nonce = cipher_encrypt.nonce
  
  return jsonify({
    'ciphertext': str(ciphertext), 
    'nonce': str(nonce), 
    'key': str(key)
  })

def data_to_ascii(capital):
  # turning data to ascii
  secret_data_list: list = [ord(char) for char in capital]
  secret_data: str = ""
  for data in secret_data_list:
    secret_data += str(data)

  return secret_data  

def geo_decryption(request):
  data = request.json
  ciphertext_as_string = data.get('ciphertext')
  nonce_as_string = data.get('nonce')
  key_as_string = data.get('key')

  ciphertext = ast.literal_eval(ciphertext_as_string)
  print("ciphertext", ciphertext)
  key = ast.literal_eval(key_as_string)
  print("key", key)
  nonce = ast.literal_eval(nonce_as_string)
  print("nonce", nonce)
  
  cipher_decrypt = AES.new(key, AES.MODE_EAX, bytes(nonce))
  decrypted_data_salt = cipher_decrypt.decrypt(ciphertext)

  # ignoring salt
  decrypted_data: bytes = ""
  if len(decrypted_data_salt) > 32:
    decrypted_data = decrypted_data_salt[:-32]
  else: 
    return jsonify({'error': 'There are no bytes to decrypt only salt'}), 404
    
  ascii_to_data = decrypted_data.decode('utf-8')

  i = 0
  decrypted_capital: str = ""

  while i < len(ascii_to_data):
    if i + 2 < len(ascii_to_data):
      ascii_nbr: int = int(ascii_to_data[i] + ascii_to_data[i + 1] + ascii_to_data[i + 2])
      if ascii_nbr > ord('z'):
        ascii_nbr = int(str(ascii_to_data[i] + ascii_to_data[i + 1]))
        print(chr(ascii_nbr))
        decrypted_capital += chr(ascii_nbr)
        i = i + 2
        
      else: 
        print(chr(ascii_nbr))
        decrypted_capital += chr(ascii_nbr)
        i = i + 3

    else:
      ascii_nbr = int(ascii_to_data[i] + ascii_to_data[i + 1])
      decrypted_capital += chr(ascii_nbr)
      break

  if decrypted_capital is None:
    return jsonify({'error': 'Data could not be decrypted.'}), 404

  print(decrypted_capital)

  return jsonify({
    'capital': decrypted_capital
  })


