# BinomialTerminal
BinomialTerminal is a simple Website made in jQuery that allows my little server to return Binomial Probability calculations on Dice!
Currently I have no plans for expansion, but I do have a few ideas!

I use the threading module in Python to multi-thread the calculation, axios to post a JSON file with the data back and forth, and flask to run the backend server!
To keep the calculation accurate I use the Decimal module, and have tried to reduce the calculation time by looping from the threshold down and subtracting from 100% instead of looping up and adding the probablilties. 
This worked for small calculations, however because the way Decimal uses context to set decimal places, it means you lose accuracy significantly for very small probablities in the range of 10^-8 or however large you
set the precision. So instead I settled with multi-threading the process by spliting the loop in two.
