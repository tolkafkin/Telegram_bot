import requests
from bs4 import BeautifulSoup 
import re
from config import wiki, url

class WikiParser:
    @staticmethod
    def parser():
        response = requests.get(url)
        result = response.content
        soup = BeautifulSoup(result, 'lxml')
        table = soup.find('table')
        dict_data = dict()

        rows = table.find_all('tr')
        for row in rows[1:]:
            cells = row.find_all('td')
            city = cells[1].find('a').text
            link = wiki + cells[1].find('a').get('href')
            population = re.search(r'\d*\s\d*', cells[4].text)[0]
            if population == ' ':
                population = re.search(r'\d\d*', cells[4].text)[0]
            else:
                population = re.split(r'\s', population)[0] + re.split(r'\s', population)[1]
            dict_data[city] = {
                    'url' : link, 
                    'population' : population
                }
        
        return dict_data
