import csv
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# setup plasmids array (store all plasmid info in this array)
# array is set up as a list of dictionaries
plasmids_full = []

def scrape_page(soup):
    plasmids = []
    # Extract plasmid information
    plasmid_elements = soup.select(".search-result-item")


    for plasmid in plasmid_elements:
        try:
            # Extract the plasmid title
            title = plasmid.select_one(".search-result-title a").text.strip()

            # Extract the catalog number
            catalog_number = plasmid.select_one(".col-xs-10").text.strip()

            # Extract the purpose
            purpose_label = plasmid.find(string="Purpose")
            if purpose_label is None:
                purpose = 'N/A'
            else:
                purpose = purpose_label.find_next("div", class_="col-xs-10").text.strip()
                if purpose == "": purpose = 'N/A'

            # Extract the depositor
            depositor_label = plasmid.find(string="Depositor")
            depositor = depositor_label.find_next("div", class_="col-xs-10").find("a").text.strip()
            if depositor == "": depositor = 'N/A'

            # Extract the type
            type_label = plasmid.find(string="Type")
            plasmid_type = type_label.find_next("div", class_="col-xs-10").text.strip()
            if plasmid_type == "": plasmid_type = 'N/A'

            # Extract the use
            use_label = plasmid.find(string="Use")
            use = use_label.find_next("div", class_="col-xs-4").text.strip()
            if use == "": use = 'N/A'

            # Extract the expression
            expression_label = plasmid.find(string="Expression")
            expression = expression_label.find_next("div", class_="col-xs-4").text.strip()
            if expression == "": expression = 'N/A'
            
            # Extract the promoter
            promoter_label = plasmid.find(string="Promoter")
            promoter = promoter_label.find_next("div", class_="col-xs-4").text.strip()
            if promoter == "": promoter = 'N/A'

            # Extract the mutation
            mutation_label = plasmid.find(string="Mutation")
            mutation = mutation_label.find_next("div", class_="col-xs-4").text.strip()
            if mutation == "": mutation = 'N/A'

            # Extract the tags
            tags_label = plasmid.find(string="Tags")
            tags = tags_label.find_next("div", class_="col-xs-4").text.strip()
            if tags == "": tags = 'N/A'

            # Extract the availability
            availability_label = plasmid.find(string="Availability")
            availability = availability_label.find_next("div", class_="col-xs-10").text.strip()
            if availability == "": availability = 'N/A'

            article_label = plasmid.find(string="Article")
            if article_label is None:
                article_name = 'N/A'
                article_link = 'N/A'
            else:
                article_div = article_label.find_next("div", class_="col-xs-10")
                article_anchor = article_div.find("a")
                article_name = article_anchor.text.strip()
                if article_name == "": article_name = 'N/A'
                article_link = "https://addgene.org/" + article_anchor.get("href")
                if article_link == "": article_link = 'N/A'

            plasmid_info = {
                "Title": title,
                "Catalog Number": catalog_number,
                "Purpose": purpose,
                "Depositor": depositor,
                "Article Name": article_name,
                "Article Link": article_link,
                "Type": plasmid_type,
                "Use": use,
                "Expression": expression,
                "Promoter": promoter,
                "Availability": availability,
                "Mutation": mutation,
                "Tags": tags
            }
            plasmids.append(plasmid_info)
        except Exception as e:
            print(f"Error extracting data for a plasmid: {e}")
            # print("Previous plasmid_id " + plasmids[-1]["Title"])
            # print("Previous promoter name " + plasmids[-1]["Promoter"])
            # print("Title: "+title)
            # print("ID: "+catalog_number)
            # if purpose == plasmids[-1]["Purpose"]:
            #     print("same purpose as last one!")
            # else:
            #     print("Purpose: "+purpose)
            # print("Depositor: "+depositor)
            # print("Article Name: "+article_name)
            # print("Article Link: "+article_link)
            # print("Plasmid Type: "+plasmid_type)
            # print("Use: "+use)
            # print("Expression: "+expression)
            # print("Promoter: "+promoter)
            # print("Availability: "+availability)
            # print("Mutation: "+mutation)
            # print("Tags: "+tags+"\n")

    return plasmids

# Setup Chrome WebDriver
driver = webdriver.Chrome()  # Ensure chromedriver is in your PATH

# URL to be accessed
url = "https://www.addgene.org/search/catalog/plasmids/?q=&page_size=50&plasmid_type=Empty+backbone"
driver.get(url)


# full while loop (only run when there is time to do so lol)
# while True:
#     # Get page source and close the driver
#     page_source = driver.page_source

#     # Parse the HTML content using BeautifulSoup
#     soup = BeautifulSoup(page_source, "html.parser")

#     plasmids_full.extend(scrape_page(soup, plasmids_full))

#     next_button = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/main/div/div[1]/div[3]/ul/li[5]/a')))
#     if next_button:
#         next_button.click()
#     else:
#         break

while True:
    # Wait for the page to load
    #time.sleep(1)

    # Get page source and close the driver
    page_source = driver.page_source

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(page_source, "html.parser")

    plasmids_full.extend(scrape_page(soup))

    # check to see if reached max page number (currently 180) -> this is not the ideal way of checking but it should work
    url = ""+driver.current_url
    if url == "https://www.addgene.org/search/catalog/plasmids/?q=&page_size=50&plasmid_type=Empty+backbone&page_number=180#" or url == "https://www.addgene.org/search/catalog/plasmids/?q=&page_size=50&plasmid_type=Empty+backbone&page_number=180":
        break
    else:
        next_button = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="next-btn"]/a')))
        driver.execute_script("arguments[0].click();", next_button)

driver.quit()

# Specify the CSV file name
csv_file = "plasmid_data.csv"

# Specify the CSV column names
csv_columns = ["Title", "Catalog Number", "Purpose", "Depositor", "Article Name", "Article Link", "Type", "Use", "Expression", "Promoter", "Availability", "Mutation", "Tags"]

# Write the data to a CSV file
try:
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for plasmid in plasmids_full:
            writer.writerow(plasmid)
    print(f"Data successfully written to {csv_file}")
except IOError as e:
    print(f"I/O error({e.errno}): {e.strerror}")
except Exception as e:
    print(f"Error writing to CSV file: {e}")