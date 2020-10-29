from scraper import ParoScraper

output_file = "unemployment.csv"

scraper = ParoScraper()

scraper.scrape()
scraper.to_csv()
