import csv
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver
driver = webdriver.Chrome()

def extract_field(plasmid, field_name, default='N/A', column_class='col-xs-10', tag='div', link=False):
    """Helper function to extract a field's value."""
    label = plasmid.find(string=field_name)
    if label:
        field = label.find_next(tag, class_=column_class)
        if field:
            if link and field.find('a'):
                return field.find('a').get('href', default)
            return field.text.strip() if field.text.strip() else default
    return default


def scrape_page(soup):
    plasmids = []
    plasmid_elements = soup.select(".search-result-item")

    for plasmid in plasmid_elements:
        try:
            title = plasmid.select_one(".search-result-title a").text.strip()
            catalog_number = plasmid.select_one(".col-xs-10").text.strip()

            plasmid_info = {
                "Title": title,
                "Catalog Number": catalog_number,
                "Purpose": extract_field(plasmid, "Purpose"),
                "Depositor": extract_field(plasmid, "Depositor", tag='a'),
                "Article Name": extract_field(plasmid, "Article", column_class='col-xs-10', tag='a'),
                "Article Link": extract_field(plasmid, "Article", default='N/A', column_class='col-xs-10', tag='a', link=True),
                "Type": extract_field(plasmid, "Type"),
                "Use": extract_field(plasmid, "Use", column_class='col-xs-4'),
                "Expression": extract_field(plasmid, "Expression", column_class='col-xs-4'),
                "Promoter": extract_field(plasmid, "Promoter", column_class='col-xs-4'),
                "Availability": extract_field(plasmid, "Availability"),
                "Mutation": extract_field(plasmid, "Mutation", column_class='col-xs-4'),
                "Tags": extract_field(plasmid, "Tags", column_class='col-xs-4')
            }

            plasmids.append(plasmid_info)
        except Exception as e:
            print(f"Error extracting data for a plasmid: {e}")

    return plasmids

def main():
    url = "https://www.addgene.org/search/catalog/plasmids/?q=&page_size=50&plasmid_type=Empty+backbone&page_number=1"
    driver.get(url)
    plasmids_full = []

    while True:
        url = driver.current_url
        soup = BeautifulSoup(driver.page_source, "html.parser")
        plasmids_full.extend(scrape_page(soup))

        try:
            if url == "https://www.addgene.org/search/catalog/plasmids/?q=&page_size=50&plasmid_type=Empty+backbone&page_number=180#" or url == "https://www.addgene.org/search/catalog/plasmids/?q=&page_size=50&plasmid_type=Empty+backbone&page_number=180":
                break
            else:
                next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="next-btn"]/a')))
                driver.execute_script("arguments[0].click();", next_button)
                
        except Exception as e:
            print(f"Error navigating to next page: {e}")
            break

    driver.quit()

    csv_file = "plasmid_data.csv"
    csv_columns = ["Title", "Catalog Number", "Purpose", "Depositor", "Article Name", "Article Link", "Type", "Use", "Expression", "Promoter", "Availability", "Mutation", "Tags"]

    try:
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            writer.writerows(plasmids_full)
        print(f"Data successfully written to {csv_file}")
    except IOError as e:
        print(f"I/O error({e.errno}): {e.strerror}")
    except Exception as e:
        print(f"Error writing to CSV file: {e}")

if __name__ == "__main__":
    main()