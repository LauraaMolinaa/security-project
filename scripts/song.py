import random
from flask import jsonify
from lyricsgenius import Genius


def song_encrypt(request):
    #getting the message to encrypt
    data = request.json
    message = data.get('message')

    #Getting the random song id number
    nbr = random.randint(1, 249000)
    
    #Getting the song using the genuis api
    genius = Genius("ytTQBFpeW9m1wOxySiu-h1mIJ_0qiv2E52oRSqoYR8NV5wE9Xka-Ngh2ugLUU88y")
    song = genius.search_song(song_id=nbr)

    if song is None:
        return jsonify({'error': 'Failed to retrieve song lyrics.'}), 500
    

    #getting the lenght of the song title
    titleLenght = len(song.title)

    #CeaserCipher
    #newMessage = ceaserCipher(message, titleLenght, True) #true == add

    #vigenere Cipher
    encryptedMessage = asciiCipher_encrypt(message, song.lyrics)
    
    encryptedArtistLenght = len(song.artist)

    encryptedTitle = ceaserCipher(song.title, encryptedArtistLenght, True)
    encryptedArtist = ceaserCipher(song.artist, encryptedArtistLenght, True)

    print(song.title)
    print(song.artist)
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
    artistLenght = len(artistKey)

    #Decrypting the title and artist
    title = ceaserCipher(titleKey, artistLenght, False)
    artist = ceaserCipher(artistKey, artistLenght, False)

    genius = Genius("ytTQBFpeW9m1wOxySiu-h1mIJ_0qiv2E52oRSqoYR8NV5wE9Xka-Ngh2ugLUU88y")
    song = genius.search_song(title,artist)

    if song is None:
        return jsonify({'error': 'Failed to retrieve song lyrics.'}), 500

    plaintext = asciiCipher_decrypt(ciphertext, song.lyrics)

    return jsonify({
        'message': plaintext,
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

def asciiCipher_encrypt(message, lyrics):
    #skip the first line
    lines = lyrics.split('\n')
    songLyrics = ''.join(lines[1:])

    if len(songLyrics) < len(message):
        songLyrics += "a" * (len(message) - len(songLyrics))

    encryptedMessage = ""
    counter = 0

    for letter in message:
        messageAscii = ord(letter)
        lyricAscii = ord(songLyrics[counter])

        newAscii = messageAscii + lyricAscii
        encryptedMessage += str(newAscii)
        encryptedMessage += "-"
        counter = counter + 1

    return encryptedMessage

def asciiCipher_decrypt(encryptedMessage, lyrics):
    lines = lyrics.split('\n')
    songLyrics = ''.join(lines[1:])

    if len(songLyrics) < len(encryptedMessage):
        songLyrics += "a" * (len(encryptedMessage) - len(songLyrics))

    encryptedNumbers = encryptedMessage.split('-')

    decryptedMessage = ""
    counter = 0

    for value in encryptedNumbers:
        if value != "":
            number = int(value)

            lyricLetter = songLyrics[counter]
            lyricAscii = ord(lyricLetter)

            originalAscii = number - lyricAscii

            decryptedMessage += chr(originalAscii)

            counter += 1

    return decryptedMessage
