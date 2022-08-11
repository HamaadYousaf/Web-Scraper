from bs4 import BeautifulSoup
import requests
import re

# Newegg


def site1Products(product):
    found_products = {}

    try:
        url = f"https://www.newegg.ca/p/pl?d={product}&N=4131"
        page = requests.get(url).text
        doc = BeautifulSoup(page, "html.parser")

        num_Pages_Element = doc.find(
            class_="list-tool-pagination-text").strong.text
        num_pages = int(num_Pages_Element.split('/')[1])
    except:
        return False

    for page in range(1, num_pages + 1):
        url = f"https://www.newegg.ca/p/pl?d={product}&N=4131&page={page}"
        page = requests.get(url).text
        doc = BeautifulSoup(page, "html.parser")

        results_div = doc.find(
            class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
        check = product.split(" ")
        product_titles = results_div.find_all(
            text=re.compile(check[0] or check[1], re.IGNORECASE))

        for title in product_titles:
            parent = title.parent

            if parent.name != "a":
                continue

            link = parent['href']
            next_parent = title.find_parent(class_="item-container")

            try:
                price = next_parent.find(
                    class_="price-current").find("strong").string
                found_products[title] = {"price": int(
                    price.replace(",", "")), "link": link}
            except:
                pass

    return found_products
