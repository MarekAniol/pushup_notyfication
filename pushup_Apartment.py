from libraries import *
from os import getcwd

HERE = getcwd()
TOKEN = config("PUSH_UP_TOKEN")
pb = Pushbullet(TOKEN)


def get_apartments(www):
    """Take url as argument and return iterable bs4 object.
    - html parts with tiles and offer links
    """
    page = get(www)
    content_html = Bfs(page.text, "html.parser")
    apartments = content_html.find_all(class_="offer-wrapper")
    return apartments


def write_json(data):
    """Writes offer apart_id to json file if it was pushed up to phone already."""
    with open(HERE + r"/found_products.json", "w") as products_json:
        json.dump(data, products_json)


def load_apartments_id():
    """Load all offers that was sending to phone as notification."""
    with open(HERE + r"/found_products.json", "r") as products_file:
        d = json.load(products_file)
        return d


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


def main():
    """Set title, price and link for phone push up notification.
    Check by apart_id if offer was visited.
    """
    apartment_ids = load_apartments_id()
    for apartment in get_apartments(url):
        title = apartment.select_one(".title-cell h3").text.strip()
        link = apartment.select_one(".title-cell a")["href"][:-1]
        price = apartment.select_one(".td-price .price strong").text

        if check_id(apartment, price, apartment_ids):
            pb.push_link(title, link, price)


if __name__ == "__main__":
    url = "https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/wroclaw/?" \
          "search%5Bfilter_float_price%3Afrom%5D=400000&search%5Bfilter_enum_market" \
          "%5D%5B0%5D=secondary&search%5Bfilter_float_m%3Ato%5D=40&search%5Bfilter_enum_rooms%5D%5B0%5D=two"
    main()
