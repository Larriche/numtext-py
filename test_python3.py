from numtext import Numtext

converter = Numtext()

while True:
    num = input("Enter the number or text to convert:")
    print(converter.convert(num))
