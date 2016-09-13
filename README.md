
Run challenge.py with Python 3. Requirements.txt file is included.

The average budget of the winners - $17,257,657*
  *This is calculated by using only movies that budget data is given. It also calculates all budgets into USD if budget is in another currency.

The main Oscars API page is easy to navigate and to get the winner from each year. The detail URL for each movie is not as clean - more specifically the budget for each film is given in a variety of formats. Mixed currencies, numeric and word values for numbers, and footnote noise are all problems that had to be accounted for. My approach to this was to get it done in a simple way - cut the noise and get the values I needed. While working on the problem, I needed to add a few catches as each function would filter out a limited number of problem cases - until I was left with no outliers.

I decided to turn all currency values that were in GBP into dollars at today's exchange rate. If a film's budget was not given, I did not include its value in the average calculation. If a range was given for a budget, I selected the high value.
