ciphertext = input()

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"

def decrypt(key, ciphertext):
    plaintext = ""
    for letter in ciphertext:
        for index, aakkonen in enumerate(alphabet):
            if letter == aakkonen:
                plaintext += alphabet[(index + key)%len(alphabet)]
                break    
    
    return plaintext

for key in range(len(alphabet)):
    print(len(alphabet) - (key), decrypt(key, ciphertext))