import requests
import re
import numpy as np


class Oscars():
  """
    Hits yipitdata API - http://oscars.yipitdata.com -
    and returns every Oscar winning movie and its budget.
    Also returns the average budget of them all.
  """

  def __init__(self):
    self.base_url = 'http://oscars.yipitdata.com'
    # winning_films - list of dictionaries that stores film title, year, url, and budget
    self.winning_films = []


  def crawl(self):
    '''
    Crawls the API to return winning movies from the main API page.
    Will add each winner to self.winning_films list
    '''
    main_page = requests.get(self.base_url).json()
    yearly_list = main_page['results']
    # loop through the results from the main page to get each year's nominations
    for year in yearly_list:
      yearly_films = year['films']
      # loop through each film every year to find the winners
      for films in yearly_films:
        # if the film is a winner add to winning_films list
        if films['Winner'] == True:
          winner = {}
          winner['title'] = films['Film']
          winner['year'] = year['year']
          winner['url'] = films['Detail URL']
          self.winning_films.append(winner)


  def get_budget(self):
    '''
    Returns budget of each winning film from its Detail URL page
    '''
    for film in self.winning_films:
      movie_page = requests.get(film['url']).json()
      # if there is no budget data, will set value as None
      film['budget'] = movie_page.get('Budget', None)


  def clean_info(self):
    '''
    Cleans the data. Removes several unnecessary characters.
    Removes currency symbol, and does foreign exchange calculation if needed.
    Turns word million into numeric value.
    If given a budget range, it will us the high value of that range.
    '''
    # loop through winning films
    for film in self.winning_films:
      # clean title value
      title = film['title']
      film['title'] = re.sub("\[[^\]][\]]", '', title)
      # clean year value
      year = film['year']
      film['year'] = re.sub("\[[^\]][\]]", '', year)

      # if the film budget is not None - this cleans budget value
      if film['budget'] != None:

        s = film['budget']

        #if the first character is not $, clean the value
        if s[0] != '$':
          # if GBP, clean and multiply by exchange rate on Sept. 12, 2016 to USD
          if s[0] == '£':
            remove_currency_s = re.sub('£', '', s)
            remove_footnotes_s = re.sub("[\(\[].*?[\)\]]", '', remove_currency_s)
            currency = re.sub('million.*', ' 1330000', remove_footnotes_s)

            try:
              step1 = [float(x.replace(',', '')) for x in currency.split( )]
              step2 = int(np.prod(np.array(step1)))
              film['budget'] = step2

            except ValueError:
              range_value = currency[0].split('-')
              high_value = int(range_value[1]) * int(range_value[2])
              film['budget'] = high_value



          elif s[0] == 'U':
            remove_currency_s = re.sub('[US$ ]', '', s)
            remove_footnotes_s = re.sub("[\(\[].*?[\)\]]", '', remove_currency_s)
            currency = re.sub('million.*', ' 1000000', remove_footnotes_s)

            try:
              step1 = [float(x.replace(',', '')) for x in currency.split( )]
              step2 = int(np.prod(np.array(step1)))
              film['budget'] = step2

            except ValueError:
              range_value = currency[0].split('-')
              high_value = int(range_value[1]) * int(range_value[2])
              film['budget'] = high_value

        #if first character is $, clean value
        elif s[0] == '$':
          remove_currency_s = re.sub('[$]', '', s)
          remove_footnotes_s = re.sub("[\(\[].*?[\)\]]", '', remove_currency_s)
          currency = re.sub('million.*', ' 1000000', remove_footnotes_s)

          try:
            step1 = [float(x.replace(',', '')) for x in currency.split( )]
            step2 = int(np.prod(np.array(step1)))
            film['budget'] = step2

          except ValueError:
            range_value = re.split('\-|\–|  ',currency)
            high_value = int(range_value[1]) * int(range_value[2])
            film['budget'] = high_value

  def average_budget(self):
    '''
    Calculates the average budget of the winning movies that have budget data
    '''
    total_movies = 0
    total_dollars = 0
    for film in self.winning_films:
      if film['budget'] != None:
        total_movies += 1
        total_dollars += film['budget']

    average = int(total_dollars/total_movies)
    return average



  def list_all(self):
    '''
    Prints results
    '''
    for film in self.winning_films:
      print(film['title'], film['year'], film['budget'])
    print("Average budget of all winners: $", self.average_budget())







  def run(self):
    '''
    run function
    '''
    self.crawl()
    self.get_budget()
    self.clean_info()
    self.list_all()



go = Oscars()

go.run()
