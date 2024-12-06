# api key TAAV7tfSDQX6liwJzxA1YeC05176YZpt

import pip._vendor.requests 
import random
from Cryptodome.Cipher import AES
from crypto.Random import get_random_bytes

payload = {}
headers= {
  "apikey": "TAAV7tfSDQX6liwJzxA1YeC05176YZpt"
}

country_codes_list: list = [
    "ven", "can", "dza", "arm", "bhs", "bgr", "chn", "flk", "gum", "ita", "lby", "mli", "nzl", "png", "zaf" 
]

country: str = random.choice(country_codes_list)

url = "https://api.apilayer.com/geo/country/code/"+country

response = pip._vendor.requests.request("GET", url, headers=headers, data = payload)

if response.status_code == 200: 
  response_data = response.json()

  capital = response_data[0].get("capital")

  secret_data = capital.encode('utf-8')

  # source https://onboardbase.com/blog/aes-encryption-decryption/

  # using  a 16 byte key which is equivalent to a 128 bit key 
  key = get_random_bytes(16)

  cipher = AES.new(key, AES.MODE_EAX)

  print(capital)
else:
  print("An error occured while getting the data. Status code:"+response.status_code)