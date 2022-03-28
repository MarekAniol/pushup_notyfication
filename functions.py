from requests import get
from bs4 import BeautifulSoup as Bfs
from pushup_Apartment import write_json


def get_apartments(www):
    """Take url as argument and return iterable bs4 object.
    - html parts with tiles and offer links
    """
    page = get(www)
    content_html = Bfs(page.text, "html.parser")
    apartments = content_html.find_all(class_="offer-wrapper")
    return apartments


def check_id(apart, apart_price, ids):
    """Check if apart apart_id is in loaded data from json file. If not add apart_price
    to found_products.json by call write_json()
    """
    price_digit = int(apart_price.replace(" zł", "").replace(" ", ""))
    apart_id = apart.select_one("table")["data-id"]
    if apart_id not in ids:
        ids[apart_id] = price_digit
        print(ids)
        write_json(ids)
        return True
    else:
        return False
