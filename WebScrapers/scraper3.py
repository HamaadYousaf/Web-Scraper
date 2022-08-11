from bs4 import BeautifulSoup
import requests

# Memory Express


def site3Products(product):
    found_products = {}

    try:
        url = f"https://www.memoryexpress.com/Search/Products?Search={product}"
        page = requests.get(url).text
        doc = BeautifulSoup(page, "html.parser")

        num_Pages_Element = doc.find(
            class_="AJAX_List_Pager AJAX_List_Pager_Compact").find("ul").find_all("li")

        if len(num_Pages_Element) > 2:
            num_pages = int(num_Pages_Element[-2].text)
        else:
            num_pages = int(num_Pages_Element[-1].text)
    except:
        return False

    for page in range(1, num_pages + 1):
        url = f"https://www.memoryexpress.com/Search/Products?Search={product}&Page={page}"
        page = requests.get(url).text
        doc = BeautifulSoup(page, "html.parser")

        try:
            results_div = doc.find(
                class_="c-shca-container").find_all(class_="c-shca-icon-item")

            for result in results_div:
                product_title = result.find(
                    class_="c-shca-icon-item__body-name").find("a").text
                price = result.find(
                    class_="c-shca-icon-item__summary-list").find("span").text
                link = result.find(
                    class_="c-shca-icon-item__body-name").find("a")['href']

                check = product.split(" ")

                if check[0].casefold() in product_title.casefold() or check[1].casefold() in product_title.casefold():
                    title_text = product_title.replace("  ", "").replace(
                        "\n", "").replace('\r', "")
                    found_products[title_text] = {"price": int(float(price.replace(
                        "$", "").replace(",", ""))), "link": "https://www.memoryexpress.com/" + link}
        except:
            pass

    return found_products
