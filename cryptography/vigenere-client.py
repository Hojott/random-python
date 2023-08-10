#!/usr/bin/env python3
""" Client implementation for Vigenère encryption
"""

# For getting command arguments
import sys

# For getting system env
import os
import dotenv

from vigenere import Vigenere

class Client:
    """ Client for Vigenère encryption
    """
    def __init__(self):
        self._vigenere = Vigenere()

        # Default values for config
        self._alphabet = ""
        self._cipher = ""
        self._mode = ""

    @property
    def vigenere(self):
        """ Vigenere class for encryption
        """
        return self._vigenere

    def run(self):
        """ Run the client, asking user for temporary configs
            (cipher type, usage mode and input texts)
        """
        old_alphabet = self.vigenere.alphabet

        alphabet = self.__input_alphabet()

        cipher = self.__input_cipher()
        mode = self.__input_mode()

        self.__set_alphabet(alphabet)
        match mode:
            case "encrypt":
                self.__encrypt(cipher)
            case "decrypt":
                self.__decrypt(cipher)

        # Resets the alphabet to the original
        self.__set_alphabet(old_alphabet)

    def start(self):
        """ Start the client with configured options
        """
        if self.check_config():

            self.__set_alphabet(self.alphabet)
            match self.mode:
                case "encrypt":
                    self.__encrypt(self.cipher)
                case "decrypt":
                    self.__decrypt(self.cipher)

        else:
            raise TypeError("Not configured or configured incorrectly! \
                            Must have alphabet, cipher and mode.")

    def __encrypt(self, cipher: str):
        """ Input texts to encrypt, with cipher given to function
        """
        plaintext = input("Input plaintext: ")
        key = input("Input key: ")
        match cipher:
            case "autokey":
                ciphertext = self.vigenere.encrypt(key, plaintext, autokey=True)
            case "vigenere":
                ciphertext = self.vigenere.encrypt(key, plaintext, autokey=False)
        print("ciphertext:", ciphertext)

    def __decrypt(self, cipher: str):
        """ Input texts to decrypt, with cipher given to function
        """
        ciphertext = input("Input ciphertext: ")
        key = input("Input key: ")
        match cipher:
            case "autokey":
                plaintext = self.vigenere.decrypt(key, ciphertext, autokey=True)
            case "vigenere":
                plaintext = self.vigenere.decrypt(key, ciphertext, autokey=False)
        print("Plaintext:", plaintext)

    def __cryptanalysis(self):
        """ Analyse ciphertext and attempt to decrypt it
        """
        # TODO: Implement cryptanalysis
        raise NotImplementedError

    # Functions on configuration
    # TODO: Modify so that you dont have to have the previous ones for the later ones to work
    # e.g. ["_", "ciphre", "_"]
    def config(self, configs: list = None):
        """ Config the client, adding options as properties of client object
            Arguments can be passed as function arguments in list or dict
        """
        if configs is None:
            configs = []

        for index, arg in enumerate(configs):
            match index:
                case 0:
                    self.alphabet = self.__validate_alphabet(arg)
                case 1:
                    self.cipher = self.__validate_cipher(arg)
                case 2:
                    self.mode = self.__validate_mode(arg)
                case _:
                    raise ValueError(f"Too many arguments! \
                                        Passed {len(configs)}, but function takes 3.")

        if self.alphabet == "":
            self.alphabet = self.__input_alphabet()

        if self.cipher == "":
            self.cipher = self.__input_cipher()

        if self.mode == "":
            self.mode = self.__input_mode()

    def check_config(self) -> bool:
        """ Check if configs are correct
        """
        alphabet = self.__validate_alphabet(self.alphabet)
        cipher = self.__validate_cipher(self.cipher)
        mode = self.__validate_mode(self.mode)

        if alphabet != "invalid" and cipher != "invalid" and mode != "invalid":
            return True

        return False

    def check_args(self) -> list:
        """ Check if arguments have been passed when running client
            Note they must be passed in order of alphabet, cipher, mode.
        """
        sys_args = []
        for i, arg in enumerate(sys.argv):
            match i:
                case 1:
                    alphabet = self.__validate_alphabet(arg)
                    sys_args.append(alphabet)

                case 2:
                    cipher = self.__validate_cipher(arg)
                    sys_args.append(cipher)

                case 3:
                    mode = self.__validate_mode(arg)
                    sys_args.append(mode)

                case _:
                    pass

        return sys_args

    def check_env(self) -> list:
        """ Check environment variables, named VIGENERE_ALPHABET,
            VIGENERE_CIPHER and VIGENERE_MODE.
        """

        dotenv.load_dotenv()

        envs = []
        alphabet = os.getenv("VIGENERE_ALPHABET")
        if alphabet is not None:
            envs.append(self.__validate_alphabet(alphabet))

        cipher = os.getenv("VIGENERE_CIPHER")
        if cipher is not None:
            envs.append(self.__validate_cipher(cipher))

        mode = os.getenv("VIGENERE_MODE")
        if mode is not None:
            envs.append(self.__validate_mode(mode))

        return envs

    # Functions on alphabet
    def __input_alphabet(self) -> str:
        """ Input which alphabet to use
        """
        input_alphabet = True
        while input_alphabet:
            alphabet = input("Alphabet: (Finnish/English) ")
            match self.__validate_alphabet(alphabet):
                case "finnish":
                    input_alphabet = False
                    return "finnish"
                case "english":
                    input_alphabet = False
                    return "english"
                case "invalid":
                    print("Invalid input!")

    def __validate_alphabet(self, alphabet: str) -> str:
        """ Validate if given alphabet is correct, and returns it in correct format
            EVERY INPUT MUST BE VALIDATED, because the code only uses values returned by validation
        """
        if alphabet.lower() == "finnish" or alphabet.lower() == "f" or alphabet.lower() == "fi":
            return "finnish"

        if alphabet.lower() == "english" or alphabet.lower() == "e" or alphabet.lower() == "en":
            return "english"

        return "invalid"

    def config_alphabet(self) -> None:
        """ Config alphabet, asking and setting it
        """
        alphabet = self.__input_alphabet()
        self.alphabet = alphabet
        self.__set_alphabet(self.alphabet)

    def __set_alphabet(self, alphabet: str) -> None:
        """ Set Vigenere alphabet
        """
        self.vigenere.set_alphabet(alphabet)

    @property
    def alphabet(self):
        """ Alphabet client uses: Finnish/English
        """
        return self._alphabet

    @alphabet.setter
    def alphabet(self, alphabet: str):
        self._alphabet = alphabet

    # Functions on cipher
    def __input_cipher(self) -> str:
        """ Input which cipher to use. Currently accepts old Vigenére and Autokey Vigenére
        """
        input_cipher = True
        while input_cipher:
            cipher = input("Cipher: (Autokey/Vigenere) ")
            match self.__validate_cipher(cipher):
                case "autokey":
                    input_cipher = False
                    return "autokey"
                case "vigenere":
                    input_cipher = False
                    return "vigenere"
                case "invalid":
                    print("Invalid input!")

    def __validate_cipher(self, cipher: str) -> str:
        """ Validate if given cipher is correct, and returns it in correct format
            EVERY INPUT MUST BE VALIDATED, because the code only uses values returned by validation
        """
        if cipher.lower() == "autokey" or cipher.lower() == "a":
            return "autokey"

        if cipher.lower() == "vigenere" or cipher.lower() == "v":
            return "vigenere"

        return "invalid"

    def config_cipher(self) -> None:
        """ Config cipher, asking and setting it
        """
        cipher = self.__input_cipher()
        self.cipher = cipher

    @property
    def cipher(self):
        """ Cipher client uses: Autokey/Vigenère
        """
        return self._cipher

    @cipher.setter
    def cipher(self, cipher: str):
        self._cipher = cipher

    # Functions on mode
    def __input_mode(self) -> str:
        """ Input which mode to use. Currently accepts encryption and decryption,
            but cryptanalysis is planned
        """
        input_mode = True
        while input_mode:
            mode = input("Mode: (Encrypt/Decrypt) ")

            match self.__validate_mode(mode):
                case "encrypt":
                    input_mode = False
                    return "encrypt"
                case "decrypt":
                    input_mode = False
                    return "decrypt"
                case "invalid":
                    print("Invalid input!")

    def __validate_mode(self, mode: str) -> str:
        """ Validate if given mode is correct, and returns it in correct format
            EVERY INPUT MUST BE VALIDATED, because the code only uses values returned by validation
        """
        if mode.lower() == "encrypt" or mode.lower() == "e" or mode.lower() == "en":
            return "encrypt"

        if mode.lower() == "decrypt" or mode.lower() == "d" or mode.lower() == "de":
            return "decrypt"

        return "invalid"

    def config_mode(self) -> None:
        """ Config mode, asking and setting it
        """
        mode = self.__input_mode()
        self.mode = mode

    @property
    def mode(self):
        """ Mode client uses: Encryption/Decryption
        """
        return self._mode

    @mode.setter
    def mode(self, mode: str):
        self._mode = mode

if __name__ == "__main__":
    client = Client()

    args = client.check_env()
    if args:
        client.config(args)
    else:
        client.config()
    client.start()
