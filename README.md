

# 📝 Namecheap Domain Auction Scrape

Gathers a list of expiring domains on NameCheap auction, and gathers details based on if domains
are potentially rare.

## 🌟 Features

- ✍️ **Output to CSV**: Data is cleansed, sorted and massaged, then otuput to a CSV file
- 🔗 **Contains Namecheap Market URL**: Quickly place your next bid, using the namecheap direct bid URL
- ⏳ **Sorted based on expiration**: Focus on the nearest domains expiring
- 💰 **Valuable data massaging**: Domains are checked against an English word lists, domains exc TLD length - both useful for assessing value of domains
## 👋 Gallery 
<img src="https://i.imgur.com/SiLlhCe.png">


🚀 Usage

1. **Clone the repository**:
    ```bash
    git clone https://github.com/cqllum/Namecheap-Domain-Auction-Scrape.git
    cd Namecheap-Domain-Auction-Scrape
    ```

2. **Run the application**:
    ```bash
    python namecheap_auction.py
    ```

The script contains a variable controller to filter on TLD 
```allowed_tlds = {'com', 'net'}  # Add other TLDs as needed``` - Will only show domains that are com or net in the otuput




