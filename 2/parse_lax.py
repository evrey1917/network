import urllib.request
from selectolax.parser import HTMLParser
import sys

how_much_get = 0
url = "https://www.muztorg.ru"
root = "/catalog"
pog = "/category/ukulele?page=13"
pog_in = "/product/A053547"

csv_file = "musical3.csv"

file = open(csv_file, "w", encoding="utf-8")

def write_in_csv(data):
    global file
    sep = ","
    next_row = "\n"

    for row in data:
        for string in row:
            file.write(string)
            file.write(sep)
        file.write(next_row)

def open_url(url):
    return HTMLParser(urllib.request.urlopen(url).read().decode("utf-8"))

def get_urls(page, what='c'):
    """Get from HTMLParser categories or products
    
    First argument: HTMLParser;
    Second argument: 'c' - if you look for categories, 'p' - for products.
    """

    categories = []

    if what == 'c':
        for node in page.css(".category"):
            categories.append(node.attributes.get("href"))

    elif what == 'p':
        for node in page.css("[itemprop=url]"):
            categories.append(node.attributes.get("content"))
    
    else:
        sys.exit("Wrong parametr: " + what)

    return categories

def get_next_page(page):
    element = page.css_first("._next")
    if element == None:
        return ""
    element = element.css_first("a")
    if element == None:
        return ""
    return element.attributes.get("href")

def get_important_data(products_on_page):
    global url, how_much_get
    data = []
    for product in products_on_page:
        page = open_url(url + product)
        sub_data = []
        how_much_get = how_much_get + 1
        print(how_much_get)
        for now in page.css(".right-col.col-xs-12.col-sm-6.col-md-8"):
            sub_data.append(now.css_first(".product-category").text())
            sub_data.append(now.css_first(".product-title").text())
            
            if now.css_first("[itemprop=sku]") != None:
                sub_data.append(now.css_first("[itemprop=sku]").text())
            else:
                sub_data.append(now.css_first(".product-info__i").css_first("span").text())

            if sub_data.append(now.css_first(".price-value.origin")) != None:
                sub_data.append(now.css_first(".price-value.origin").text().replace("\xa0", "").replace("\n", "").replace(" ", ""))
            else:
                sub_data.append("No data")
        data.append(sub_data)
    return data

# for node in page.css("[itemprop=url]"):
#     categories.append(node.attributes.get("content"))

# categories = open_url(url + pog)
# print(get_next_page(categories))

# get_important_data(pog_in)

# open_url(url + pog_in)

categories = get_urls(open_url(url + root))

for category in categories:
    sub_categories = get_urls(open_url(url + category))

    for sub_category in sub_categories:
        next_page = sub_category

        while next_page != "":
            page = open_url(url + next_page)
            products_on_page = get_urls(page, 'p')
            data = get_important_data(products_on_page)
            write_in_csv(data)
            next_page = get_next_page(page)
