from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pandas as pd
import os


def load_plasmid_list(file_path):
    """
    Loads a plasmids file into a Pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pd.DataFrame: DataFrame containing the CSV data.
    """
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    # Keep only columns with the name 'Catalog Number'
    df_filtered = df.filter(like='Catalog Number', axis=1)
    
    # Remove the first letter from every value in these columns
    df_filtered = df_filtered.apply(lambda col: col.astype(str).str.slice(start=1))

    # Convert the filtered DataFrame values to integers
    df_filtered = df_filtered.apply(pd.to_numeric, errors='coerce')
 
    # Return the filtered DataFrame
    return df_filtered

def init_soup():
    # Initialize WebDriver
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome()
    


def extract_seq(plasmid_list):
    plasmid_seq = []
    driver = init_soup()
    for gene_number in plasmid_list[:100]: #First 100 genes
        url = f'https://www.addgene.org/{gene_number}/sequences/'
        driver.get(url)        
        """
        # Random sleep time between 1 and 5 seconds
        sleep_time = random.randint(1, 3)
        time.sleep(sleep_time)
        """
        soup = BeautifulSoup(driver.page_source, "html.parser")
        #pl_full = soup.find(id='depositor-full')
        pl_full = soup.find_all('div', class_="col-lg-7 col-xs-8", limit=1)
        for seq in pl_full:
            text = seq.get_text().strip()
            plasmid_info = {
                "Catalog Number": gene_number,
                "Full Gene Seq": text}
            plasmid_seq.append(plasmid_info)
    driver.quit()
    return plasmid_seq


def main():
    df = load_plasmid_list('plasmid_data.csv')
    plasmid_list = df.values.flatten()
    plasmid_data = extract_seq(plasmid_list)
    plasmid_df = pd.DataFrame(plasmid_data)
    
    # Define columns to include (optional)
    columns_to_save = ["Catalog Number", "Full Gene Seq"]
    file_path = r"user path" #Add your complete file path here
    # Save DataFrame to CSV, including only specified columns
    plasmid_df.to_csv(file_path, columns=columns_to_save, mode='w', index=False, lineterminator='')
    
if __name__ == "__main__":
    main()