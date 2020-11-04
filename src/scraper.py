import time
import datetime
import requests
import bs4
import numpy


class OilScraper:

    def __init__(self):
        self.url = "https://datosmacro.expansion.com/materias-primas/"
        # Materials to which look data for
        self.attr = ['opec', 'brent', 'petroleo-wti']
        # IDs used on the website to identify the source tables
        self.id_table = {'opec': 'tb1_1463', 'brent': 'tb1_295', 'petroleo-wti': 'tb1_20108'}
        # Periods of time to consider in our scrapping
        self.years = list(range(2000, 2021))
        self.months = list(range(1, 13))
        # Creates a list of year-month combinations which are before our current year-month
        self.year_months = [str(a) + '-' + str(b).zfill(2) for a in self.years for b in self.months if
                            str(a) + '-' + str(b).zfill(2) < datetime.datetime.today().strftime('%Y-%m')]
        self.data = {}
        self.array = None

    def __download_site(self, attr, year_month):
        """ Download the site provided on the self.url as a request object

        :return: request object with the html of the site
        """
        html = requests.get(self.url + attr + '?dr=' + year_month)
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
        :param year_month: Year-Month to filter our search for.
        """
        print(f"Starting to parse the site {self.url + attr + '?dr=' + year_month} ...")

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

    def __get_array(self):
        """ Gets an array from the data stored in self.data and stores it in self.array

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

            # Sorting array by date_column
            sorted_array = np_array[numpy.argsort(np_array[:, 0])][::-1]
        self.array = sorted_array

    def __clean_array(self):
        """ Cleans our array according to NA treatment and date filters

        :return: None
        """
        # Imputing '-' as an empty value
        self.array = numpy.where(self.array == '-', '', self.array)
        # Leaving only data from the 2000s
        self.array = self.array[numpy.where(self.array[:, 0] >= '2000')]

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
        self.__get_array()
        self.__clean_array()
        numpy.savetxt(filename, self.array, delimiter=",", fmt='%s')
