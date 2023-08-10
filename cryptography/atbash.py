ciphertext = input()

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"

plaintext = ""
# I agree, the slowest method possible
# Using a hash-table would be faster
for letter in ciphertext:
    for index, aakkonen in enumerate(alphabet):
        if letter == aakkonen:
            plaintext += alphabet[-(index+1)]
            break

print(plaintext)
