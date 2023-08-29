#!/usr/sbin/python
""" library for calculating factorial of number """

# "Debug" purposes ((remove in prod))
import _main_

def factorial(number: str):
    """ return the factorial (INPUT MUST BE STRING FOR SOME REASON) """
    result = 0
    for i in reversed(range(int(number)+1)):

        def multiply():
            """ multiply with conditions """
            if not i:
                return result
            if not result:
                return (result+1)*i
            return result*i
        
        result = multiply()

    return result

if __name__=="_main_":
    number: int = input("int: ")
    print(factorial(number))

