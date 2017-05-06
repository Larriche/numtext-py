# Numtext
#
# This code is open source according to the MIT License as follows.
#
# Copyright (c) 2016 Richman Larry Clifford
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
A simple library for converting numbers from their numeric to word forms                        
or from their word forms to numeric forms for numbers less than or equal to
999 quadrillion

I believe this range is enough to make it useful 

Definitions
The defintions for the following phrases as used in my comments

number text - the text form of a number eg. 'six' , 'six thousand'

denomination - a number denomination eg. thousand , million ,billion

denomination descriptor - the labels that identify denominations
eg. 'sixty thousand' is a number text consisting of a smaller
     number text 'sixty' and a denomination descriptor 'thousand'
"""

class Numtext:
    def __init__(self):
        """
        Initialize the Numtext object with the properties it needs
        """          
        self.numbers = [ i for i in range(21) ]

        for i in range(30,91,10):
            self.numbers.append(i)

        self.textValues = ["zero" , "one" , "two" ,"three" , "four" ,"five" ,"six" ,"seven",
              "eight" ,"nine" ,"ten","eleven", "twelve", "thirteen", "fourteen",
              "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty",
              "thirty", "fourty", "fifty", "sixty", "seventy", "eighty", "ninety" ]

        self.maxDigitMappings = {6 : 'thousand', 9 : 'million', 12:'billion' , 15:'trillion' ,
                                 18 : 'quadrillion' }

        self.powers = { 'hundred' : 2,'thousand' : 3,'million' : 6 ,
                             'billion' : 9 , 'trillion' : 12 ,'quadrillion' : 15}
    
    def getText(self,number):
        """
        Get the text form of a number in numeric format.This method uses recursion
        to obtain the word forms of more complex numbers using smaller denominations
        as building blocks
        """

        if int(number) in self.numbers:
            return self.textValues[ self.numbers.index(int(number))]

        else:
            if len(number) < 3:
                return self.getText(str(int(number[0]) * 10)) + "-" + self.getText(number[1])

            elif len(number) == 3:

                text = ""

                if number[0] != '0':
                    text = self.getText(number[0]) + " hundred "

                rem = int(number) - (int(number[0]) * 100)

                if rem != 0:
                    if number[0] != '0':
                        text += "and "

                    text += self.getText(str(rem))
                return text

            else:

                if len(number) % 3 != 0:
                    padLength = len(number) + (3 - len(number) % 3)
                    number = self.padDigits(number , padLength)

                maxDigits = len(number)
                name = self.maxDigitMappings[maxDigits]
                
                text = self.getText(number[0:3]) + " {} ".format(name)
                
                rem = int(number[3:len(number)])

                if rem > 100:
                    text += ", "
                else:                
                    if rem != 0:
                        text += "and "
                        
                if rem != 0:
                    text += self.getText(str(rem))

                return text

    def getNumericValue(self,numStr):
        """
        Get numeric value of a number when given a correctly written word form
        """
        numStr = numStr.replace(',',' ').replace('-',' ').lower()

        numValue = 0

        if numStr in self.textValues:
            return self.numbers[self.textValues.index(numStr)]

        parts = []

        for i in numStr.split(" "):
            if len(i) != 0:
                if i.isdigit():
                    text = self.getText(i)
                    text = text.replace(',',' ').replace('-',' ').lower()
                    subParts = [ j for j in text.split(" ") if len(j) != 0 ]

                    for j in subParts:
                        parts.append(j)
                else:
                    parts.append(i)       
        
        i = 0

        while i < len(parts):
            curr = parts[i]
            
            if (i + 1) < len(parts) and parts[i + 1] in self.powers.keys():
                desc = parts[i + 1]
                

                temp = self.numbers[self.textValues.index(curr)] * (10 ** self.powers[desc])

                if (i + 2) < len(parts):
                    if parts[i + 1] == 'hundred' and parts[i + 2] == 'and':
                        i += 3

                        while i < len(parts) and not parts[i] in self.powers.keys():

                            temp += self.numbers[self.textValues.index(parts[i])]

                            i += 1

                        if i < len(parts):
                            temp *= 10 ** self.powers[parts[i]]

                    elif parts[i + 2] in self.powers.keys():
                        
                        temp *= (10 ** self.powers[parts[ i + 2]])

                        i += 2

                    else:
                        i += 1

                else:
                    i += 1
                        
            else:
                temp = self.numbers[self.textValues.index(curr)]

                if (i + 2) < len(parts):            
                    temp += self.numbers[self.textValues.index(parts[i + 1])]
                    temp *= (10 ** self.powers[parts[i + 2]])
                    i += 2

            if (i + 1) < len(parts) and parts[i + 1] == 'and':
                i += 1

            numValue += temp

            i += 1


        return numValue          
        

    def padDigits(self,number,length):
        """
        Pad zeroes in front of the digits in a number to make
        the number occupy a certain digits space eg. make numbers
        in thousand range occupy 6 positions
        """
        pad = ""
        
        for i in range(length - len(number)):
            pad += "0"

        return pad + number

    def convert(self,number):
        """
        Converts a number to its alternative format
        """
        if str(number).isdigit():
            try:
                return self.getText(str(number))
            except:
                raise InvalidNumberException("Unknown number: " + str(number))
  
        else:
            try:
                return self.getNumericValue(number)
            except:
                raise InvalidNumberWordException("Unknown number text: " + str(number))
               


class InvalidNumberException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg  + "\nNumber must be less than 999 quadrillion")
        

class InvalidNumberWordException(Exception):
    def __init(self,msg):
        Exception.__init__(self,msg)

        


