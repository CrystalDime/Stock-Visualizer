import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import matplotlib.pyplot as plt



## A program that retrieves three months of nasdaq stock data and reformats it as a graph
## Possibly add the option to select the length of data collected (3 months, year , two years)

class Stock(object): # Generates a stock object when given a string as an argument
    def __init__(self,symbol):
        self.symbol = symbol.upper()

    def __repr__(self):
        return str(self.symbol)

    def data(self,types): # Retrieves historic chart data from website and stores it within a dictionary
        r = requests.get('https://www.nasdaq.com/symbol/' + self.symbol + '/historical')
        soup = bs(r.content, "html.parser")
        web_content = soup.find_all('tr')
        name = soup.find_all('h1')[0].text.rsplit('Common')[0]
        raw_chart = [x.text.split() for x in web_content[4:69]] # 4-69
        opens = [x[1] for x in raw_chart[::-1]]
        high = [x[2] for x in raw_chart[::-1]]
        low = [x[3] for x in raw_chart[::-1]]
        closing = [x[4] for x in raw_chart[::-1]]
        volume = [x[5] for x in raw_chart[::-1]]
        for i in volume:
            volume[volume.index(i)] = i.replace(',','')
        indices = [x[0] for x in raw_chart[::-1]]
        data = {'Open': opens, 'High': high, 'Low': low, 'Closing': closing, 'Volume': volume}
        if types == 'data':
            return data
        elif types == 'indices':
            return indices
        elif types == 'name':
            return name
    def dataframe(self): # Uses data from 'def data' to generate a pandas data frame
        columns = ['Open', 'High', 'Low', 'Closing', 'Volume']
        data = self.data('data')
        indices = self.data('indices')
        chart = pd.DataFrame(data, columns=columns, index=indices)
        return chart
    def graph(self): # Uses the information from 'def data_frame' to form a graph
        print ('Processing...')
        chart = self.dataframe()
        name = self.data('name')
        chart = chart.astype(float)
        plt.figure(figsize = (20,20))
        plt.scatter(chart.index, chart['Closing'])
        plt.plot(chart.index, chart['Closing'])
        plt.xticks(rotation=90)
        plt.title('Historic Stock Prices for %s' % name)
        plt.ylabel('Price in dollar per stock')
        plt.show()





state = True

while state:
    symbol = input('Please enter a stock symbol...   ')
    stocks = Stock(symbol)
    try:
        stocks = Stock(symbol)
        stocks.graph()
        state = False
    except IndexError as error:
        print ('Invalid Stock Symbol. Please try again.')







