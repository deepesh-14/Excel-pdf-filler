import pdfplumber
import re

def extract_prices(pdf_path):
    """Extract chemical names and prices from PDF"""
    price_data = {}
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split('\n')
            
            for line in lines:
                # Pattern: code + name + price + packing
                # Example: 107335 Guanidine Nitrate 540.00 250 gm
                match = re.search(r'^\d+\s+([\w\s\-\(\),\.\']+?)\s+(\d+\.\d{2})\s+', line)
                
                if match:
                    chemical_name = match.group(1).strip()
                    price = float(match.group(2))
                    
                    # Store multiple prices if exists
                    if chemical_name in price_data:
                        price_data[chemical_name].append(price)
                    else:
                        price_data[chemical_name] = [price]
    
    return price_data

# Test it
if __name__ == "__main__":
    prices = extract_prices("pricelist.pdf")
    for chemical, price_list in list(prices.items())[:5]:  # Show first 5
        print(f"{chemical}: {price_list}")