from scraper import OilScraper

output_file = "data/oil_prices.csv"

scraper = OilScraper()

scraper.scrape()
scraper.to_csv(output_file)
