import time
import requests
import bs4


class ParoScraper:

    def __init__(self):
        self.url = "https://datosmacro.expansion.com/paro"
        self.data = []


    def __download_site(self):
        """ Download the site provided on the self.url as a request object

        :return: request object with the html of the site
        """
        html = requests.get(self.url)
        return html


    def __get_soup(self, html):
        """ Returns a BeautifulSoup object from the html

        :param html: requests object with the information from the self.url
        :return: BeautifulSoup object from the html provided
        """
        soup = bs4.BeautifulSoup(html.content)
        return soup


    def scrape(self):
        """ Scrapes the website looking for the data needed

        :return:
        """

        start_time = time.time()

        print(f"Starting to parse the site {self.url} ...")

        # Download the first url
        html = self.__download_site()
        # Get the first soup
        soup = self.__get_soup(html)

        print(soup)

        end_time = time.time()
        total_time = end_time - start_time

        print(f"The process took {total_time} seconds.")

    def to_csv(self, filename):
        """ Saves the file inside the data/ folder according to the filename provided

        :param filename: Filename to save the file, including the .csv
        :return: None
        """
        file = open("../data/" + filename, "w+")

        # Trabajar la parte de insertar las filas de data a csv ##
