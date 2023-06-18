import sys
import requests
from bs4 import BeautifulSoup


def main():
    price_usd = get_usd_price()
    price_jpy = get_jpy_price()
    bm_index = bm_index_calculator(price_jpy, price_usd)
    off_rate = off_ex_rate()
    varience = price_varience(off_rate, bm_index)
    print(f"According to the Big Mac Index, there should be {bm_index} to the dollar.")
    print(f"The official exchange rate is {off_rate} yen to the dollar.")
    print(f"Going by the Big Mac index, the official rate is too high by about {varience}!")

    # Prompt the user if they want to convert JPY to USD based on the Big Mac Index.
    while True:
        decision = input("Would you like to convert some amount of yen to USD going by the Big Mac Index? [y/n] ").lower()
        if decision == "y":
            try:
                yen = int(input("Enter yen amount: "))
                usd = calc(yen, bm_index)
                print(f"That comes to about {usd} USD.")
                continue
            except ValueError:
                print("Please enter a valid number.")
                continue
        elif decision == "n":
            sys.exit("Goodbye.")
        else:
            continue


def get_usd_price() -> float:
    """Gets USD info for Big Mac from the web"""
    URL = "https://wisevoter.com/country-rankings/big-mac-index-by-country/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    usd_price = soup.find("td", {"class": "shdb-on-page-table-body-Data", "data-order": "6"})
    usd_price = usd_price.text.replace("$", "")  # cleans the results and returns it as a float
    return float(usd_price)


def get_jpy_price() -> int:
    """Gets Japanese Yen info for Big Mac from the web"""
    URL = "https://www.mcdonalds.co.jp/en/products/1210/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    jpy_price = soup.find("span", {"class": "font-speedee font-bold product-section-price-primary-val"})
    return int(jpy_price.text.replace("~", ""))  # cleans the result and returns it as an int


def bm_index_calculator(price_jpy: int, price_usd: float) -> float:
    """Calculates the Big Mac index for JPY to USD
    JPY / USD"""
    n = price_jpy / price_usd
    return round(n)


def off_ex_rate() -> int:
    """Gets official JPY to USD exchange rate web"""
    URL = "https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=JPY"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    off_exchange = soup.find("p", {"class": "result__BigRate-sc-1bsijpp-1 iGrAod"})
    off_exchange = off_exchange.text.replace(" Japanese Yen", "")
    return round(float(off_exchange))


def price_varience(official_rate: float, bm_index: float) -> str:
    """Calculates (as a percent) how far off the official exchange rate
    is compared to the Big Mac Index"""
    ratio = round(official_rate / bm_index, 2)
    varience = round((ratio - 1) * 100)
    return str(varience) + "%"


def calc(yen, bm_index):
    """Convert a given JPY sum to USD base on the Big Mac Index"""
    return round(yen / bm_index)


if __name__ == "__main__":
    main()
