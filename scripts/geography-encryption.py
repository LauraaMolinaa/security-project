# api key TAAV7tfSDQX6liwJzxA1YeC05176YZpt

import pip._vendor.requests 
from flask import jsonify
import random
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import os

def main(request = None):
  payload = {}
  headers= {
    "apikey": "0kyJpyoUHDRbexeoyYNOuakAo8QzfkmX"
  }

  country_codes_list: list = [
      "ven", "can", "dza", "arm", "bhs", "bgr", "chn", "flk", "gum", "ita", "lby", "mli", "nzl", "png", "zaf" 
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
    return jsonify({'error': 'Capital city is '+capital+'and Country is '+country}), 404

  # adding more to capital to make key longer
  data_to_ascii: str = capital

  # turning data to ascii
  secret_data_list: list = [ord(char) for char in data_to_ascii]
  secret_data: str = ""
  for data in secret_data_list:
    secret_data += str(data)
  
  salt = os.urandom(32)
  secret_data_bytes = secret_data.encode('utf-8') + salt

  # using  a 16 byte key which is equivalent to a 128 bit key 
  key = get_random_bytes(16)
  cipher_encrypt = AES.new(key, AES.MODE_EAX)

  # converting the secret data to bytes 
  ciphertext = cipher_encrypt.encrypt(secret_data_bytes)
  nonce = cipher_encrypt.nonce

  cipher_decrypt = AES.new(key, AES.MODE_EAX, nonce)
  decrypted_data_salt = cipher_decrypt.decrypt(ciphertext)

  # ignoring salt
  decrypted_data: bytes = ""
  if len(decrypted_data_salt) > 32:
    decrypted_data = decrypted_data_salt[:-32]
  else: 
    print("no bytes to decrypt, only salt")
    
  ascii_to_data = decrypted_data.decode('utf-8')

  i = 0
  data: str = ""

  while i < len(ascii_to_data) - 2:
    ascii_nbr = ascii_to_data[i] + ascii_to_data[i + 1] + ascii_to_data[i + 2]
    
    if int(ascii_nbr) > ord('z'):
      ascii_nbr = ascii_to_data[i] + ascii_to_data[i + 1]
      print(chr(int(ascii_nbr)))
      data += chr(int(ascii_nbr))
      i = i + 2
      
    else: 
      print(chr(int(ascii_nbr)))
      data += chr(int(ascii_nbr))
      i = i + 3

  # return jsonify({
  #   'ciphertext': ciphertext, 
  #   'nonce': nonce, 
  #   'key': key
  # })

def geo_decryption(request):
  # data = request.json
  # ciphertext = data.get('ciphertext')
  # nonce = data.get('nonce')
  # key = data.get('key')

  # cipher = AES.new(key, AES.MODE_EAX, nonce)
  # data = cipher.decrypt(ciphertext)
  return


if __name__ == "__main__":
  main()


