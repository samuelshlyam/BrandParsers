# README

## Notes for New Brands
When adding a new brand, create a new object in parsing_settings.json with the brand ID provided in the spreadsheet.  
Use underscores if your brand name has multiple words (e.g., "My_New_Brand").  
Identify the outer HTML element (type and class) that wraps all product info.  
Fill in the fields for price, name, color, composition, etc.  
If some fields do not exist (like a sale price or composition), leave them empty strings: "".  
If the product ID is in a list, set "Product_ID_Method": "List", and pick the correct index with "Product_ID_Number".

Also note that there may be multiple product IDs, and all these Product IDs must be saved.

## Structure of parsing_settings.json
Each brand has an entry, labeled with a brand ID (for example, 201, 310, 229). Inside each entry, there are several fields describing the HTML structure:

- **Brand_Name**: The name of the brand, written with underscores if it has multiple words (e.g., Fendi or Alexander_Mcqueen).  
- **Outer_Type / Outer_Class**: The outermost HTML element that contains all product data.  
  - Example: A `<div>` with class "product-detail"  
- **Original_Price_Type / Original_Price_Class**: The HTML tag and class where the original price is found.  
  - Example: `<span class="value"> $690.00 </span>`  
- **Sales_Price_Type / Sales_Price_Class**: The HTML tag and class where the sale price is found. If no sale price exists, this can be empty.  
- **Currency_Type / Currency_Class**: The HTML tag and class where the currency might be found, if it is not included in the text of the price.  
- **Name_Type / Name_Class**: The HTML tag and class for the product name.  
- **Source_Type / Source_Class**: The HTML tag and class for the source URL or any additional data describing the source (sometimes this is found in a `<span>` that is visually hidden).  
- **Color_Type / Color_Class**: The HTML tag and class for the color of the product.  
- **Composition_Type / Composition_Class**: The HTML tag and class for composition or material information.  
- **Description_Type / Description_Class**: The HTML tag and class for the product description.  
- **Image_Type / Image_Class**: The HTML tag and class for the product image(s).  
- **Images_Method** and **Images_Key** explain how the image data is stored. For instance, "Dictionary" with `src` or `srcset`.  
- **Product_ID_Type / Product_ID_Class**: The HTML tag and class where the product ID is found.

Sometimes, **Product_ID_Method** can be "List", which means the product ID might appear in a list of similar blocks, and we must look at **Product_ID_Number** (the position of the correct block in the list).

## Example
"2": {  
  "Brand_Name": "Loewe",  
  "Outer_Type": "div",  
  "Outer_Class": "capds-product-container",  
  "Original_Price_Type": "span",  
  "Original_Price_Class": "capds-product__price--active",  
  ...  
  "Product_ID_Type": "p",  
  "Product_ID_Class": "capds-sm-label",  
  "Product_ID_Method": "List",  
  "Product_ID_Number": 15  
}

Here, to find the product ID for Loewe items, the parser:

- Locates all `<p>` elements with the class "capds-sm-label".  
- Takes the 15th element from that list.  
- Gets the text inside that element as the Product ID.

## Special Cases
If a brand’s Product ID, URL, or prices are stored in a completely different way than the ones covered in the script, skip that brand and write a note about the issue.  
If a brand stores data in a part of the HTML that the script cannot handle with current methods (for example, data hidden in JavaScript or in a special tag), write a note explaining the brand and how it stores data. This alerts us that all_parsers.py may need changes.

## When to Skip a Brand
If you can’t get Product ID, URL, or prices with existing methods (like finding the text in a simple HTML tag), skip it.  
Write a note in the code or in your documentation explaining why (e.g., “Brand X stores its product ID in a hidden JavaScript variable, which we cannot read without changing the parser.”).

## How to Use
Open all_parsers.py.

Check the `__main__` block at the bottom of all_parsers.py. You will see something like:

```python
if __name__=="__main__":
    settings = json.loads(open("parsing_settings.json").read())
    brand_id = "201"  # Example for Fendi
    URL="https://www.fendi.com/us-en/woman/shoes/..."
    ...
Set the brand_id to the correct number from parsing_settings.json (this number matches the brand entry you want to parse).

Set the URL to the product page you want to parse.

Run all_parsers.py.

The script will open the page in a headless Chrome browser and extract data using the rules from parsing_settings.json.

Finally, it prints the extracted product details in the console (or terminal).

Explanation of the Parsing Code
BrandParsers class:
You give it html_content, settings, and a brand_id.
It picks the correct brand’s rules from settings.
get_product_details looks in the HTML for each piece of information (price, color, name, images, etc.).
It returns a dictionary with keys like "Original_Price", "Sale_Price", "Color", "Product ID", and so on.

Handling Errors or Missing Data
If prices are missing, the script sets them to empty strings initially.
If only sale price is found but not original price, we set both to the same value.
If the brand uses dollar signs or euro signs, the script guesses the currency.
If the brand has a separate currency block in HTML, the parser reads it, too.

How It Works
You enter a product URL for the brand you want to parse (for example, a Fendi product URL).
The script reads brand-specific rules from parsing_settings.json to guide how the HTML is parsed.
Using these rules, the code in all_parsers.py extracts the required data from the HTML content.

Important Files and Their Purposes
parsing_settings.json
Holds the parsing rules for each brand, including the HTML tags and classes to look for.

all_parsers.py
Uses BeautifulSoup (a Python library) to parse HTML. It reads the settings from parsing_settings.json and attempts to gather product information based on those settings.

Overview
This project aims to extract product data from several brands’ product pages. It looks for:

Product ID
Source URL (not the user-provided URL, but one found again in the HTML source)
All prices (original price and sale price, if present. original price will always be larger)
Other product information like color, composition, description, and images is also collected if it can be found on the product page. Each brand must provide at least Product ID, URL, and all prices to be considered complete.

Summary
This project uses simple HTML parsing (through BeautifulSoup and Selenium) to collect product information. The instructions for each brand live in parsing_settings.json. If a brand changes its website or uses a format not covered by the existing methods, you will need to update parsing_settings.json or possibly modify all_parsers.py. Always document any issues you find or any special cases that require additional code changes.

Feel free to add more details in the JSON settings as you discover them. The main goal is to consistently capture the Product ID, URL, and prices for every brand.
