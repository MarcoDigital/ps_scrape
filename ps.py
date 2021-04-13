import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# Deze scraper werkt alleen met productpagina's van Plantsome waarin de volgende gegevens beschikbaarzijn:

# 1. Latijnse naam zoals "Trachycarpus Fortunei (Chinese Waaierpalm)".
# 2. Plantsome naam zoals "Jackie".
# 3. Een totaalprijs beschikbaar is.

url = input("Wat is de Plantsome URL? ")
filename = input("Hoe heet het product? ")

# Tijd
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
datum = time.strftime("%d/%m/%Y", t)
i = 1


def create_csv():
    """Maakt eerste bestand aan met headers"""
    df = pd.DataFrame({'1': [], "2": [], "3": [], "4": [], "5": [], "6": [], })
    df.columns = ["Datum", "Tijd", "Plantsome", "Product", "URL", "Prijs"]
    df.to_csv("./data/" + filename + ".csv", header=True,
              mode="a", encoding="utf-8", sep="\t", index=False)


def plantsome_scrape(pagina):
    """Generator functie. Vult het bestand van create_csv() aan met gegevens"""
    # Tijd
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    datum = time.strftime("%d/%m/%Y", t)

    # Soup
    req = requests.get(pagina).text
    soup = BeautifulSoup(req, "html.parser")

    # Resultaat
    prijs_str = soup.find("span", id="totalPrice").get_text()
    product = soup.find("h1", id="product_title").get_text()

    prijs = float(prijs_str)  # Prijs
    producttitel = product.strip()  # Latijnse naam
    plantsome_naam = soup.find(
        "h2", class_="product-title__title title black mt0 mb0 f-bold").get_text()  # Plantsome naam

    # Pandas
    df = pd.DataFrame({"Datum": [datum],
                       "Tijd": [current_time],
                       "Plantsome": [plantsome_naam],
                       "Product": [producttitel],
                       "URL": [url],
                       "Prijs": [str(prijs)],
                       })

    # Append rijen aan zonder header
    df.to_csv("./data/" + filename + ".csv", header=False,
              mode="a", encoding="utf-8", sep="\t", index=False)

    # Console log
    print(f"{datum} - {current_time}: Data geschreven voor {producttitel} ({plantsome_naam}). Bestandsnaam: {filename}.csv")


if __name__ == "__main__":
    while 1:
        # Willekeurig aantal seconden tussen x and y.
        interval = random.randint(86400, 90000)
        try:
            if i == 1:
                create_csv()
                i += 1
        except:
            print(
                f"{datum} - {current_time}: Er kon geen CSV bestand gemaakt worden. Bestaat de \"data\" map nog?")
        try:
            plantsome_scrape(url)
        except:
            print(
                f"{datum} - {current_time}: Geen product gevonden. Wellicht uit voorraad of een verkeerde URL.")
        time.sleep(interval)
