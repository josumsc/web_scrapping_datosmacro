# Web Scrapping datosmacro - Oil Prices
This repository has been made to realize the PRA1 from the subject "Tipología y ciclo de vida de los datos", for the online university "UOC".

The work consist in one small web scrapping program that scrappes the website https://datosmacro.expansion.com/ in order to obtain data about the price of oil by 3 different indexes (OPEC, Brent and West Texas), the resulting dataset from that scrapping, the visualization of the dataset and a pdf document reequired by the UOC's professor.

The website datosmacro is offered by the economics focused newspaper "Expansion" (https://www.expansion.com/), to obtain macro economics information to be used by people from the financial and economical world.

## File Structure
* `src/main.py` - Location of the **main** script executable to get the dataset.
* `src/scraper.py` - Implementation of the **OilScraper** class used to download and scrape the data.
* `data/oil_prices.csv` - Location of the dataset.
* `visualization/plot_date_price.r` - Code to obtain a useful visualization of the dataset.
* `visualization/mean_price_x_month.png` - Visualization obtained with the previous script.

## References
Lawson, R. (2015), Web Scraping with Python, Packt Publishing Ltd.
Subirats & Calvo (2020), Web Scraping, Editorial UOC