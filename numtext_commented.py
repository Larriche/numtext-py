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
or from their word forms to numeric forms for numbers less than or equal
to 999 quadrillion

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
        # numbers whose text forms are fundamental in number to text conversion
	# they are 0 - 20 and then 30 , 40 , 50 ... 90      
        self.numbers = [ i for i in range(21) ]

        for i in range(30,91,10):
            self.numbers.append(i)

        # corresponding word forms for the numbers
        self.textValues = ["zero" , "one" , "two" ,"three" , "four" ,"five" ,"six" ,"seven",
              "eight" ,"nine" ,"ten","eleven", "twelve", "thirteen", "fourteen",
              "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty",
              "thirty", "fourty", "fifty", "sixty", "seventy", "eighty", "ninety" ]

        # a mapping of the maximum spaces occupied by numbers  from thousand    
        # onwards and the corresponding label applied to their first three digits
        self.maxDigitMappings = {6 : 'thousand', 9 : 'million', 12:'billion' , 15:'trillion' ,
                                 18 : 'quadrillion' }

        # mapping of denominations and their corresponding powers of 10 
        self.powers = { 'hundred' : 2,'thousand' : 3,'million' : 6 ,
                             'billion' : 9 , 'trillion' : 12 ,'quadrillion' : 15}
    
    def getText(self,number):
        """
        Get the text form of a number in numeric format.This method uses recursion
        to obtain the word forms of more complex numbers using smaller denominations
        as building blocks
        """

        if int(number) in self.numbers:
            # if we have the number in our list of fundamental numbers,
            # we simply return its equivalent text form
            return self.textValues[ self.numbers.index(int(number))]

        else:
            if len(number) < 3:
                # two digit numbers that are not in our fundamental list
                return self.getText(str(int(number[0]) * 10)) + "-" + self.getText(number[1])

            elif len(number) == 3:
                # numbers in the hundreds denomination

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
                # numbers in higher denominations

                # If the number doesn't occupy the maximum digits for its denomination,
                # we pad it with zeros at the front to attain that form      
                if len(number) % 3 != 0:
                    padLength = len(number) + (3 - len(number) % 3)
                    number = self.padDigits(number , padLength)

                # get the descriptor for the number based on number of digits
                maxDigits = len(number)
                name = self.maxDigitMappings[maxDigits]
                
                # The first three digits of the number after padding make up the number that
                # carries the denomination descriptor
                # eg. in 050000 , 50 is the part that carries the descriptor thousand                
                text = self.getText(number[0:3]) + " {} ".format(name)
                
                rem = int(number[3:len(number)])

                # if the remainder is not less than 100 we need a ',' not an 'and'
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

        # accumulates the numeric value 
        numValue = 0

        if numStr in self.textValues:
            # if the number text form already exists in our fundamental list,
            # no need to worry ourselves
            return self.numbers[self.textValues.index(numStr)]

        # Break the text string into a list that doesn't have any spaces as an item
        # We convert substrings that are written in numeric form to their text forms
        # while generating the parts
        parts = []

        for i in numStr.split(" "):
            if len(i) != 0:
                if i.isdigit():
                    #handling numeric substrings
                    text = self.getText(i)
                    text = text.replace(',',' ').replace('-',' ').lower()
                    subParts = [ j for j in text.split(" ") if len(j) != 0 ]

                    for j in subParts:
                        parts.append(j)
                else:
                    parts.append(i)       
        
        # the current index in the list of parts
        i = 0

        while i < len(parts):
            # let's hold on to the current item in the list
            curr = parts[i]
            
            # we want to know whether the next item is a denomination descriptor
            # and not a number or 'and' but we have to place in a check for whether
            # we have reached the end of the list or not
            if (i + 1) < len(parts) and parts[i + 1] in self.powers.keys():
                # the next item is a denomination descriptor
                desc = parts[i + 1]
                
                # We multiply the numeric value of the current item by 10 raised to the
                # power x where x depends on the denomination descriptor
                # eg. x is 3 for thousand and 6 for million

                # We don't add this result to the accumulated value yet.We hold on to it.            
                temp = self.numbers[self.textValues.index(curr)] * (10 ** self.powers[desc])

                # check if we can get more items
                if (i + 2) < len(parts):
                    # check if the item at the next position is a 'hundred' and the item
                    # two places from the current item is an 'and'
                    if parts[i + 1] == 'hundred' and parts[i + 2] == 'and':
                        # advance the index to the position after the 'and'
                        i += 3

                        while i < len(parts) and not parts[i] in self.powers.keys():
                            # We try to get all text forms after the 'and' 
                            # until we either come across a label or the end of the 
                            # list

                            # Get subunits linked by the 'and' so that
                            # a common label can be applied to them if necessary
                            temp += self.numbers[self.textValues.index(parts[i])]

                            # We move the current index along as we go since we are
                            # actually continuing the iteration
                            i += 1

                        if i < len(parts):
                            # if we terminated because we saw a descriptor
                            # multiply by the appropriate power of 10
                            temp *= 10 ** self.powers[parts[i]]

                    elif parts[i + 2] in self.powers.keys():
                        # If the item at two places from the current item is also a
                        # denomination descriptor , we multiply again.
                        # eg. as seen in 'six hundred thousand'
                        
                        temp *= (10 ** self.powers[parts[ i + 2]])

                        # since we handled parts[i + 2] in the process, we move the
                        # current index forward to reflect that
                        i += 2

                    else:
                        # We do nothing to temp
                        # However,we increment the index variable to reflect the fact 
			# that we handled one item in advance 
                        i += 1

                else:
                    # We do nothing to temp
                    # However,we increment the index variable to reflect the fact 
		    # that we handled one item in advance 
                    i += 1
                        
            else:
                temp = self.numbers[self.textValues.index(curr)]

                # Check if the next two items are a number text and a denomination
                # descriptor
                # eg. as in 'sixty five thousand'
                if (i + 2) < len(parts):            
                    temp += self.numbers[self.textValues.index(parts[i + 1])]
                    temp *= (10 ** self.powers[parts[i + 2]])
                    i += 2

            # If we have an 'and' as the next element after all the above,
            # we skip it because this 'and' is not required to build
            # a complete subunit.It's only a separator
            # eg. the 'and' in 'twenty five thousand and two'
            if (i + 1) < len(parts) and parts[i + 1] == 'and':
                i += 1

            # We have finished converting a complete subunit so we accumulate it
            numValue += temp

            # We move to the next item after where we stopped after all the
            # processing above
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

        


