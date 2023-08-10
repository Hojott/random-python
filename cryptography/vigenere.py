""" Barebones implementation for Vigenère encryption
"""
class Vigenere:
    """ Vigenère encryption with Finnish alphabet
    """
    def __init__(self, alphabet: str = "finnish"):
        self._alphabet: str
        self.set_alphabet(alphabet)

    @property
    def alphabet(self) -> str:
        """ Alphabet to use with encryption
        """
        return self._alphabet

    @alphabet.setter
    def alphabet(self, alphabet: str) -> str:
        self._alphabet = alphabet

    def set_alphabet(self, alphabet: str):
        """ Set the alphabet, currently either finnish or english
        """
        match alphabet.lower():
            case "finnish":
                self.alphabet: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"
            case "english":
                self.alphabet: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def alphabet_index(self, letter_to_find: str) -> int:
        """ Finds index in alphabet of given letter
        """
        for index, letter_in_alphabet in enumerate(self.alphabet):
            if letter_to_find == letter_in_alphabet:
                return index

        raise ValueError("Illegal letter: " + letter_to_find)

    def validate_text(self, validetable_text: str) -> None:
        """ Validates text doesn't have illegal letters
        """
        for letter in validetable_text:
            # Check for illegal letters
            if letter not in self.alphabet:
                raise ValueError("Illegal letter: " + letter)

    def encrypt(self, key: str, plaintext: str, autokey = False) -> str:
        """ Encrypt with Vigenère cipher, plaintext and key must only consist of
            letters in Finnish alphabet
            Also supports Vigenère autokey cipher
        """
        plaintext = plaintext.upper()
        self.validate_text(plaintext)
        key = key.upper()
        self.validate_text(key)


        ciphertext = ""
        for index, letter in enumerate(plaintext):
            letter_index: int = self.alphabet_index(letter)

            if len(key)-1 >= index or not autokey:
                key_letter = key[index%len(key)]
                key_index: int = self.alphabet_index(key_letter)
            else:
                key_index: int = self.alphabet_index(plaintext[(index-1)-(len(key)-1)])

            new_index: int = (letter_index + key_index) % len(self.alphabet)
            ciphertext += self.alphabet[new_index]

        return ciphertext

    def decrypt(self, key: str, ciphertext: str, autokey = False) -> str:
        """ Decrypt Vigenère cipher, ciphertext and key must only consist of
            letters in Finnish alphabet
            Also supports Vigenère autokey cipher
        """
        ciphertext = ciphertext.upper()
        self.validate_text(ciphertext)
        key = key.upper()
        self.validate_text(key)

        plaintext = ""
        for index, letter in enumerate(ciphertext):
            letter_index: int = self.alphabet_index(letter)

            if len(key)-1 >= index or not autokey:
                key_index: int = self.alphabet_index(key[index%len(key)])
            else:
                key_index: int = self.alphabet_index(plaintext[(index-1)-(len(key)-1)])

            new_index: int = (letter_index - key_index) % len(self.alphabet)
            plaintext += self.alphabet[new_index]

        return plaintext
