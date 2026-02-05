from fuzzywuzzy import fuzz

def match_products_to_prices(products, price_data, threshold=80):
    """Match product names with chemical names from PDF"""
    matched_prices = {}
    unmatched = []
    
    for product in products:
        best_match = None
        best_score = 0
        
        # Try to find best match
        for chemical in price_data.keys():
            score = fuzz.partial_ratio(product.lower(), chemical.lower())
            
            if score > best_score:
                best_score = score
                best_match = chemical
        
        # If match is good enough
        if best_score >= threshold:
            matched_prices[product] = price_data[best_match]
        else:
            unmatched.append(product)
    
    return matched_prices, unmatched

# Test
if __name__ == "__main__":
    from pdf_parser import extract_prices
    from excel_handler import read_products
    
    prices = extract_prices("pricelist.pdf")
    products = read_products("sample.xlsx")
    
    matched, unmatched = match_products_to_prices(products, prices)
    
    print("Matched:")
    for prod, price_list in matched.items():
        print(f"  {prod}: {price_list}")
    
    print("\nUnmatched:")
    for prod in unmatched:
        print(f"  {prod}")