Python implementation of my text to number and number to text
conversion class,Numtext

eg. Usage
converter = Numtext()
print converter.convert(2016)
You get two thousand and sixteen

print converter.convert("one million, six hundred and two)
You get 1000602

It also handles cases where the input is semi-word form
eg.'1 million' , '123 thousand' are all catered for.

The highest denomination catered for is quadrillion.I believe
that range is enough to make it useful but it can be extended 
if desired.

Applications:
1.You can use it in a small program that kids can use to learn
numbers and their equivalents in words

2.In data mining/scraping projects where your data has numbers
in word format but you need it in numeric format to do arithmetic
with it


Cheers,
Larry