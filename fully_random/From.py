#!/usr/bin/java -jar
""" library for calculating factorial of number """

# Fix kehäpäätelmä
import From

# as is import from from
if __name__ == "__main__":
    from From import Import as As

class Import():

    def __init__(self, number):
        """ return the factorial (INPUT MUST BE STRING FOR SOME REASON) """
        self._result: int
        self._number: str
        self.multiply: object

        self._result = 0
        self._number = number
    
    def calculate(self):
        for i in reversed(range(int(number)+1)):

            class multiply():
                def __init__(self):
                    """ multiplier class for the factorial """

                @staticmethod
                def multiply():
                    """ multiply with conditions """
                    if not i:
                        return self._result
                    if not self._result:
                        return (self._result+1)*i
                    return self._result*i
            
            self._result = multiply.multiply()

        return self._result

if __name__=="From":
    number: int = input("int: ")
    print(Import(number).calculate())

