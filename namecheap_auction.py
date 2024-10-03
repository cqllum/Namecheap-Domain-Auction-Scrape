                    
##################################################################
#        Title: Namecheap Domain Auction Scrape
#          URL: https://github.com/cqllum/Namecheap-Domain-Auction-Scrape
#         Date: 2024-10-03
#       Author: cqllum
#  Description: Gathers a list of expiring domains on NameCheap 
#               auction, and gathers details based on if domains
#               are potentially rare.
###################################################################

# Imports
import requests
import pandas as pd
import nltk
from nltk.corpus import words

# Downloads the words data set
nltk.download('words')

# Function to scrape data from Namecheap
def scrape_namecheap(url, output_file):
    response = requests.get(url)
    if response.status_code == 200:
        with open(output_file, 'wb') as f:
            f.write(response.content)
        print(f"Data successfully saved to {output_file}")
    else:
        print("Failed to retrieve data from Namecheap")

# Function to load the NLTK word list
def load_valid_words():
    return set(words.words())

# Function to prepare domain information
def prepare_domain_info(domain_info, allowed_tlds, valid_words):
    valid_domains = []

    for domain in domain_info:
        word = domain['name'].split('.')[0]  # Get the domain name excl. the TLD
        full_domain = domain['name']
        domain_tld = full_domain.split('.')[-1]  # Get TLD
        domain_length = len(word)
        valid_word_flag = word in valid_words

        if (allowed_tlds is None or domain_tld in allowed_tlds):
            valid_domains.append({
                **domain,
                'domain_length': domain_length,
                'valid_word': valid_word_flag
            })

    return valid_domains

# Main function
def main(namecheap_domain_url, output_file, allowed_tlds=None):
    # Step 1: Scrape the data
    scrape_namecheap(namecheap_domain_url, output_file)

    # Step 2: Read the CSV file into a DataFrame
    df = pd.read_csv(output_file)

    # Ensure the DataFrame has a column named 'name'
    if 'name' not in df.columns:
        print("Column 'name' not found in the CSV.") # if this error occurs, there could be an error with the file, or a change is found from namecheaps side
        return

    # Extract relevant domain information
    domain_info = df[['url', 'name', 'endDate', 'price', 'startPrice', 'renewPrice', 'registeredDate']].dropna().to_dict(orient='records')

    # Load valid words only once
    valid_words = load_valid_words()

    # Step 3: Prepare domain information
    valid_domains = prepare_domain_info(domain_info, allowed_tlds, valid_words)

    # Convert to DataFrame for sorting
    valid_df = pd.DataFrame(valid_domains)

    # Step 4: Sort by endDate, valid_word, domain_length, and registeredDate
    valid_df['endDate'] = pd.to_datetime(valid_df['endDate'], errors='coerce')
    valid_df['registeredDate'] = pd.to_datetime(valid_df['registeredDate'], errors='coerce')
    valid_df.sort_values(by=['endDate', 'valid_word', 'domain_length', 'registeredDate'], 
                    ascending=[True, False, True, True], inplace=True)

    # Step 5: Output valid domains to a new CSV
    if not valid_df.empty:
        valid_df.to_csv('valid_domains.csv', index=False)
        print(f"Valid domains exported to valid_domains.csv")
    else:
        print("No valid domains found.")

if __name__ == "__main__":
    namecheap_domain_url = "https://nc-aftermarket-www-production.s3.amazonaws.com/reports/Namecheap_Market_Sales.csv"
    output_file = "namecheap_domains.csv"

    # Set allowed TLDs
    allowed_tlds = {'com', 'net'}  # Add other TLDs as needed

    main(namecheap_domain_url, output_file, allowed_tlds)
