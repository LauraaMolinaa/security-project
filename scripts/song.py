import random
from flask import jsonify
from lyricsgenius import Genius


def song_encrypt(request):
    #getting the message to encrypt
    data = request.json
    message = data.get('message')

    #Getting the random song id number
    nbr = random.randint(1, 249990)
    
    #Getting the song using the genuis api
    genius = Genius("ytTQBFpeW9m1wOxySiu-h1mIJ_0qiv2E52oRSqoYR8NV5wE9Xka-Ngh2ugLUU88y")
    song = genius.search_song(song_id=nbr)

    if song is None:
        return jsonify({'error': 'Failed to retrieve song lyrics.'}), 500
    

    #getting the lenght of the song title
    titleLenght = len(song.title)

    #CeaserCipher
    newMessage = ceaserCipher(message, titleLenght, True) #true == add

    #vigenere Cipher
    encryptedMessage = addCipher(newMessage, song.lyrics)
    
    encryptedMessageLenght = len(encryptedMessage)

    encryptedTitle = ceaserCipher(song.title, encryptedMessageLenght, True)
    encryptedArtist = ceaserCipher(song.artist, encryptedMessageLenght, True)

    
    return jsonify({
        'ciphertext': encryptedMessage,
        'title': encryptedTitle,
        'artist': encryptedArtist})

def song_decrypt(request):
    data = request.json
    ciphertext = data.get('ciphertext')
    titleKey = data.get('titleKey')
    artistKey = data.get('artistKey')

    #Getting the message lenght
    ciphertextLenght = len(ciphertext)
    
    #Decrypting the title and artist
    title = ceaserCipher(titleKey, ciphertextLenght, False)
    artist = ceaserCipher(artistKey, ciphertextLenght, False)

    genius = Genius("ytTQBFpeW9m1wOxySiu-h1mIJ_0qiv2E52oRSqoYR8NV5wE9Xka-Ngh2ugLUU88y")
    song = genius.search_song(title,artist)

    return jsonify({
        'message': ciphertext,
        'title': title,
        'artist': artist})



def ceaserCipher(message, number, add):
    #making the shift stay in the alphabets range
    number = number % 26
    shiftedMessage = ""

    for letter in message:
        if letter.isalpha():
            #we need to set it to a base of 0 so the rapping atound works correctly
            if letter.isupper():
                base = ord('A')
            else:
               base = ord('a')

            position = ord(letter) - base
            if(add):
                #Need modulo to loop it back to the start
                newPosition = (position + number) % 26
            else:
                #Need modulo to loop it back to the start
                newPosition = (position - number) % 26

            newLetter = chr(newPosition + base)

            shiftedMessage += newLetter
        else:
            shiftedMessage += letter
    
    return shiftedMessage

def addCipher(message, lyrics):
    #skipping the first line
    lines = lyrics.split('\n')
    songLyrics = '\n'.join(lines[1:])
    encryptedMessage = ""

    counter = 0

    for letter in message:
        if counter < len(songLyrics):
            # modulo 256 for valid ASCII chars
            newLetter = chr((ord(letter) + ord(songLyrics[counter])) % 256)
            encryptedMessage += newLetter
            counter += 1
        else:
            encryptedMessage += letter

    return encryptedMessage