# Addgene Webscraper

This repository contains Python scripts for scraping plasmid data from the Addgene website. It includes two main scripts: `webscraper.py` for collecting general plasmid information, and `plasmid_scraper.py` for extracting full gene sequences.

## Features

### webscraper.py
- Scrapes multiple pages of plasmid data from Addgene
- Extracts various fields including title, catalog number, purpose, depositor, and more
- Handles pagination automatically
- Saves data to a CSV file for easy analysis

### plasmid_scraper.py
- Loads plasmid catalog numbers from a CSV file
- Scrapes full gene sequences for each plasmid
- Supports batch processing (currently set to the first 100 plasmids)
- Saves extracted sequences to a new CSV file

## Requirements

- Python 3.x
- BeautifulSoup4
- Selenium
- Chrome WebDriver
- Pandas

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/addgene-webscraper.git
cd addgene-webscraper
``` 

3. Install the required Python packages:
```
pip install beautifulsoup4 selenium pandas
```

5. Download and install the Chrome WebDriver that matches your Chrome browser version.

## Usage

1. Run the script:
```
python webscraper.py
```
2. The script will start scraping data from Addgene, beginning with the first page of empty backbone plasmids.

3. Once complete, the data will be saved to `plasmid_data.csv` in the same directory.

### plasmid_scraper.py

1. Ensure you have a CSV file named `plasmid_data.csv` with a column containing plasmid catalog numbers.

2. Update the file path in the `main()` function to specify where you want to save the output.

3. Run the script:
```
python plasmid_scraper.py
```
4. The script will extract full gene sequences for the specified plasmids and save the results to the specified CSV file.

## Output

### webscraper.py
Generates `plasmid_data.csv` with columns:
- Title, Catalog Number, Purpose, Depositor, Article Name, Article Link, Type, Use, Expression, Promoter, Availability, Mutation, Tags

### plasmid_scraper.py
Generates a CSV file (path specified in the script) with columns:
- Catalog Number, Full Gene Seq

## Notes

- `webscraper.py` is set to stop after reaching page 180 or when there are no more pages to scrape.
- `plasmid_scraper.py` is currently set to process only the first 100 plasmids. Adjust this limit in the `extract_seq()` function if needed.
- Web scraping may be subject to Addgene's terms of service. Ensure you have permission to scrape their website.
- Use responsibly and consider implementing delays between requests to avoid overloading the server.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/yourusername/addgene-webscraper/issues) if you want to contribute.

## License

[MIT](https://choosealicense.com/licenses/mit/)
