import time
import requests
import bs4
import numpy

class OilScraper:

    def __init__(self):
        self.url = "https://datosmacro.expansion.com/materias-primas/"
        self.attr = ['opec', 'brent', 'petroleo-wti']
        self.id_table = {'opec': 'tb1_1463', 'brent': 'tb1_295', 'petroleo-wti': 'tb1_20108'}

        self.data = {}

    def __download_site(self, attr):
        """ Download the site provided on the self.url as a request object

        :return: request object with the html of the site
        """
        html = requests.get(self.url + attr)
        return html

    def __get_soup(self, html):
        """ Returns a BeautifulSoup object from the html

        :param html: requests object with the information from the self.url
        :return: BeautifulSoup object from the html provided
        """
        soup = bs4.BeautifulSoup(html.content, 'html.parser')
        return soup

    def __add_attr(self, attr):
        """ Adds one of the attributes to the data set scraping the web.

        :param attr: Attribute to add to the data set.
        """
        print(f"Starting to parse the site {self.url + attr} ...")

        html = self.__download_site(attr)
        soup = self.__get_soup(html)

        tds = soup.find(id=self.id_table[attr])

        date = ''
        for td in tds.find_all('td'):
            if date == '':
                date = td.get_text()
            else:
                if date not in self.data:
                    self.data[date] = {}
                self.data[date][attr] = td.get_text().replace(',', '.').replace('$', '')
                date = ''

    def scrape(self, keywords=""):
        """ Scrapes the website according to the keywords provided

        :param keywords: Keywords to search for. If null looks into the entire site.
        :return:
        """

        start_time = time.time()

        # Modifies the url
        #self.__keyword_modifier(keywords)

        for attr in self.attr:
            self.__add_attr(attr)

        print(self.data)

        end_time = time.time()
        total_time = end_time - start_time

        print(f"The process took {total_time} seconds.")

    def to_csv(self, filename):
        """ Saves the file inside the data/ folder according to the filename provided

        :param filename: Filename to save the file, including the .csv
        :return: None
        """
        np_array = numpy.array(['date', 'opec', 'brent', 'wti'])
        for key in self.data.keys():
            np_array = numpy.vstack(
                (np_array, [key, self.data[key]['opec'], self.data[key]['brent'], self.data[key]['petroleo-wti']]))

        numpy.savetxt(filename, np_array, delimiter=",", fmt='%s')