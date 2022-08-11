from bs4 import BeautifulSoup
import requests

# Micro Center


def site2Products(product):
    found_products = {}

    try:
        url = f"https://www.microcenter.com/search/search_results.aspx?N=&cat=&Ntt={product}&searchButton=search"
        page = requests.get(url).text
        doc = BeautifulSoup(page, "html.parser")

        num_Pages_Element = doc.find(
            class_="pages inline").findAll("li")

        if(len(num_Pages_Element) > 2):
            num_pages = int(num_Pages_Element[-2].text)
        else:
            num_pages = int(num_Pages_Element[1].text)
    except:
        return False

    for page in range(1, num_pages + 1):
        url = f"https://www.microcenter.com/search/search_results.aspx?NTX=mode+MatchPartial&NTT={product}&NTK=all&page={page}"
        page = requests.get(url).text
        doc = BeautifulSoup(page, "html.parser")

        results_container = doc.find(
            id="productGrid").find("ul").find_all(class_="details")

        for result in results_container:
            title = result.find(
                class_="normal").find("h2").find("a").text
            price = result.find(class_="price").find("span").text
            url = (result.find(class_="normal").find("h2").find("a")["href"])
            link = "https://www.microcenter.com" + url

            check = product.split(" ")

            if check[0].casefold() in title.casefold() or check[1].casefold() in title.casefold():
                found_products[title] = {"price": int(
                    float(price.replace(",", "").replace("$", ""))), "link": link}

    return found_products
