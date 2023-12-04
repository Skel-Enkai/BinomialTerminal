# BinomialTerminal
BinomialTerminal is a simple Website made in jQuery that allows my little server to return Binomial Probability calculations on Dice!

I use the threading module in Python to multi-thread the calculation, axios to post a JSON file with the data back and forth, and flask to run the backend server!
To keep the calculation accurate I use the Decimal module, and have tried to reduce the calculation time by looping from the threshold down and subtracting from 100% instead of looping up and adding the probablilties. 
This worked for small calculations, however because the way Decimal uses context to set decimal places, it means you lose accuracy significantly for very small probablities in the range of 10^-8 or however large you
set the precision. So instead I settled with multi-threading the process by spliting the loop in two.

The new Feature I have added is a hashmap which stores precomputed values of the binomial expansion and cumulative probabilites.
In theory, this makes the algorithm constant time, so long the value has been precomputed and stored, but there are so many combinations this is unlikely!
When a new combination is requested but not found in the hashmap, an entry for this combination is calculated and added to the hashmap, which is then saved in a file on the server. This file is loaded whenever the flask server is started. 
One worry I have is if this hashmap grows in size it may outsized my RAM on my 1GB RaspberryPi. I could either move the server to my NUC which has 16GB, however theoretically there is an infinite amount of combinations. So eventually this RAM will be ecclipsed too. 

I have an idea to split different Hashmaps into categories stored in files. Say, Probabilites of a single success being greater or equal than 0.5 or less than 0.5. This would split the database into two different files and hashmaps. Where a simple comparison could find which hashmap to load and search. These files probability boundaries could be split an arbitrary amount of times. This would save RAM space but increase load times as each time there is a new request, there possibility that a new file needs to be loaded. Again there is still theoretically and infinite amount of combinations within the files, as the N (number of trials) could be infinitley many, and P (Probability of one Success) could be infinitely small/accurate. To solve problem N we could limit the value of N to a ceiling (this works as N is an integer). To solve problem P we can set P to a minimum value, say 1.0*10^-3, and set the accuracy to a value which would limit the number of combinations to a finite, but still very large value, say 5 decimal places.
