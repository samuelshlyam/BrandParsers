import json
import re
from bs4 import BeautifulSoup
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("--auto-open-devtools-for-tabs")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
options.add_argument("--start-maximized")
options.add_argument("--incognito")
options.add_argument("--enable-javascript")
options.add_argument('--no-sandbox')
options.add_argument('--disable-setuid-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--headless=new")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
class BrandParsers:
    def __init__(self,html_content,settings,brand_id):
        brand_settings=settings.get(f"{brand_id}")
        self.product_details=self.get_product_details(html_content,brand_settings)
    def get_product_details(self,html_content,brand_settings):
        product_details={}
        original_price=""
        sale_price=""
        soup = BeautifulSoup(html_content, 'html.parser')
        outer_type=brand_settings.get("Outer_Type","")
        outer_class=brand_settings.get("Outer_Class","")
        outer_details_block=soup.find(outer_type,class_=outer_class)
        # Get original price
        original_price_type=brand_settings.get("Original_Price_Type","")
        original_price_class = brand_settings.get("Original_Price_Class","")
        original_price_block=outer_details_block.find(original_price_type, class_=original_price_class)
        if original_price_block:
            original_price=original_price_block.text.strip()
            product_details["Original_Price"]=original_price

        # Get sale price
        sale_price_type = brand_settings.get("Sales_Price_Type","")
        sale_price_class = brand_settings.get("Sales_Price_Class","")
        sale_price_block=outer_details_block.find(sale_price_type, class_=sale_price_class)
        if sale_price_block:
            sale_price = sale_price_block.text.strip()
            product_details["Sale_Price"] = sale_price

        # Fix prices
        if not original_price and sale_price:
            original_price=sale_price
            product_details["Original_Price"] = original_price
        if not sale_price and original_price:
            sale_price = original_price
            product_details["Sale_Price"] = sale_price

        # Get currency
        if "$" in sale_price or "$" in original_price:
            product_details["Currency"] = "USD"
        if "€" in sale_price or "€" in original_price:
            product_details["Currency"] = "Euro"
        currency_type = brand_settings.get("Currency_Type", "")
        currency_class = brand_settings.get("Currency_Class", "")
        currency_block = outer_details_block.find(currency_type, class_=currency_class)
        if currency_block:
            currency = currency_block.text.strip()
            product_details["Currency"] = currency

        # Get name
        name_type = brand_settings.get("Name_Type","")
        name_class = brand_settings.get("Name_Class","")
        name_block=outer_details_block.find(name_type, class_=name_class)
        if name_block:
            name = name_block.text.strip()
            product_details["Name"] = name

        # Get source
        source_type = brand_settings.get("Source_Type","")
        source_class = brand_settings.get("Source_Class","")
        source_block=outer_details_block.find(source_type, class_=source_class)
        if source_block:
            source = source_block.text.strip()
            product_details["Source"] = source

        # Get color
        color_type = brand_settings.get("Color_Type","")
        color_class = brand_settings.get("Color_Class","")
        color_block=outer_details_block.find(color_type, class_=color_class)
        if color_block:
            color = color_block.text.strip()
            product_details["Color"] = color

        # Get composition
        composition_type = brand_settings.get("Composition_Type","")
        composition_class = brand_settings.get("Composition_Class","")
        composition_block=outer_details_block.find(composition_type, class_=composition_class)
        if composition_block:
            composition = composition_block.text.strip()
            product_details["Composition"] = composition

        # Get description
        description_type = brand_settings.get("Description_Type","")
        description_class = brand_settings.get("Description_Class","")
        description_block=outer_details_block.find(description_type, class_=description_class)
        if description_block:
            description = description_block.text.strip()
            product_details["Description"] = description

        #Get images
        images_type = brand_settings.get("Images_Type", "")
        images_class = brand_settings.get("Images_Class", "")
        images_method = brand_settings.get("Images_Method", "")
        images_key = brand_settings.get("Images_Key", "")
        print(images_method)
        images_blocks = outer_details_block.find_all(images_type, class_=images_class)
        print(images_blocks)
        for images_block in images_blocks:
            if images_block:
                product_details["Images"]=[]
                if images_method=="Dictionary":
                    images=images_block[images_key]
                    print(images)
                    product_details["Images"].append(images)
                else:
                    images = images_block.text.strip()
                    product_details["Images"].append(images)

        # Get product id
        pid_type = brand_settings.get("Product_ID_Type","")
        pid_class = brand_settings.get("Product_ID_Class","")
        pid_method = brand_settings.get("Product_ID_Method", "")
        pid_number=brand_settings.get("Product_ID_Number", "")
        if pid_method=="List":
            pid_blocks = outer_details_block.find_all(pid_type, class_=pid_class)
            pid_block=pid_blocks[pid_number]
            if pid_block:
                pid = pid_block.text.strip()
                product_details["Product ID"] = pid
        else:
            pid_block=outer_details_block.find(pid_type, class_=pid_class)
            if pid_block:
                pid = pid_block.text.strip()
                product_details["Product ID"] = pid

        return product_details



if __name__=="__main__":
    settings = json.loads(open("parsing_settings.json").read())
    brand_id = "0"
    URL="YOUR_PRODUCT_PAGE_URL_HERE"
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    brand_html_content = driver.execute_script("return document.documentElement.outerHTML;")
    product_details=BrandParsers(brand_html_content,settings,brand_id).product_details
    print(product_details)

