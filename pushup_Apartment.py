from libraries import *


token = config("PUSH_UP_TOKEN")
pb = Pushbullet(token)
url = "https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/wroclaw/?" \
      "search%5Bfilter_float_price%3Afrom%5D=400000&search%5Bfilter_enum_market" \
      "%5D%5B0%5D=secondary&search%5Bfilter_float_m%3Ato%5D=40&search%5Bfilter_enum_rooms%5D%5B0%5D=two"
page = get(url)
content_html = Bfs(page.text, "html.parser")
apartaments = content_html.find_all(class_="offer-wrapper")
print(page)


def write_json(data):
    with open(r"/home/marek/snap/pycharm/pushup_notyfication/found_products.json", "w") as products_json:
        json.dump(data, products_json)


def load_json():
    with open(r"/home/marek/snap/pycharm/pushup_notyfication/found_products.json", "r") as products_file:
        return json.load(products_file)


def main():
    for apartament in apartaments:
        title = apartament.select_one(".title-cell h3").text.strip()
        price = apartament.select_one(".td-price .price strong").text
        id_apart = apartament.select_one("table")["data-id"]
        price_digit = price[:-3]
        price_num = int(price_digit.replace(" ", ""))
        link = apartament.select_one(".title-cell a")["href"][:-1]
        if id_apart not in datas_apartment:
            datas_apartment[id_apart] = price_num
            write_json(datas_apartment)
            pb.push_link(title, link, price)


datas_apartment = load_json()
prices_sorted = list(datas_apartment.values())
main()
