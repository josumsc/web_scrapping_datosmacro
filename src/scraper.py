import time
import datetime
import requests
import bs4
import numpy


class OilScraper:

    def __init__(self):
        self.url = "https://datosmacro.expansion.com/materias-primas/"
        self.attr = ['opec', 'brent', 'petroleo-wti']
        self.id_table = {'opec': 'tb1_1463', 'brent': 'tb1_295', 'petroleo-wti': 'tb1_20108'}
        self.current_year_month = datetime.datetime.today().strftime('%Y-%m')
        self.years = list(range(2010, 2021))
        self.months = list(range(1, 13))
        self.year_months = [str(a) + '-' + str(b).zfill(2) for a in self.years for b in self.months if
                            str(a) + '-' + str(b).zfill(2) < self.current_year_month]
        self.data = {}

    def __download_site(self, attr, year_month):
        """ Download the site provided on the self.url as a request object

        :return: request object with the html of the site
        """
        html = requests.get(self.url + attr + '?df=' + year_month)
        return html

    def __get_soup(self, html):
        """ Returns a BeautifulSoup object from the html

        :param html: requests object with the information from the self.url
        :return: BeautifulSoup object from the html provided
        """
        soup = bs4.BeautifulSoup(html.content, 'html.parser')
        return soup

    def __add_attr(self, attr, year_month):
        """ Adds one of the attributes to the data set scraping the web.

        :param attr: Attribute to add to the data set.
        """
        print(f"Starting to parse the site {self.url + attr + '?df=' + year_month} ...")

        html = self.__download_site(attr, year_month)
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

    def scrape(self):
        """ Scrapes the website provided looking for the data

        :return: None
        """

        start_time = time.time()

        for attr in self.attr:
            for year_month in self.year_months:
                self.__add_attr(attr, year_month)

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
            # Check in case we didn't retrieve any data for some attr
            for attr in self.attr:
                if not self.data[key].get(attr):
                    self.data[key][attr] = '-'
            np_array = numpy.vstack(
                (np_array, [key, self.data[key]['opec'], self.data[key]['brent'], self.data[key]['petroleo-wti']]))

        numpy.savetxt(filename, np_array, delimiter=",", fmt='%s')