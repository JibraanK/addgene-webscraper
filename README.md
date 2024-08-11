# Addgene Webscraper

This repository contains a Python script for scraping plasmid data from the Addgene website. The script collects detailed information about empty backbone plasmids and saves it to a CSV file.

## Features

- Scrapes multiple pages of plasmid data from Addgene
- Extracts various fields including title, catalog number, purpose, depositor, and more
- Handles pagination automatically
- Saves data to a CSV file for easy analysis

## Requirements

- Python 3.x
- BeautifulSoup4
- Selenium
- Chrome WebDriver

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/addgene-webscraper.git
cd addgene-webscraper
``` 

3. Install the required Python packages:
```
pip install beautifulsoup4 selenium
```

5. Download and install the Chrome WebDriver that matches your Chrome browser version.

## Usage

1. Run the script:
```
python webscraper.py
```
3. The script will start scraping data from Addgene, beginning with the first page of empty backbone plasmids.

4. Once complete, the data will be saved to `plasmid_data.csv` in the same directory.

## Output

The script generates a CSV file named `plasmid_data.csv` with the following columns:

- Title
- Catalog Number
- Purpose
- Depositor
- Article Name
- Article Link
- Type
- Use
- Expression
- Promoter
- Availability
- Mutation
- Tags

## Notes

- The script is set to stop after reaching page 180 or when there are no more pages to scrape.
- Web scraping may be subject to Addgene's terms of service. Ensure you have permission to scrape their website.
- Use responsibly and consider implementing delays between requests to avoid overloading the server.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/yourusername/addgene-webscraper/issues) if you want to contribute.

## License

[MIT](https://choosealicense.com/licenses/mit/)
