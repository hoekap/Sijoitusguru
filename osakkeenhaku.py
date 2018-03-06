import urllib.request
import urllib.error
import re


def suorita_kutsu(osake):
    url = "https://finance.google.com/finance?q={:s}".format(osake)
    kutsu = urllib.request.Request(url)
    vastaus = urllib.request.urlopen(kutsu)
    return vastaus.read()


def hae_osakkeen_tiedot(osake):
    """
    Hakee osakkeiden tiedot Googlen Finance-palvelusta. Tämän jälkeen html
    koodista otetaan vain tarpeellinen ja se palautetaan
    :param osake: Osakkeen virallinen kaupankäyntitunnus
    :return: Palauttaa ilman virheitä tarvittavat tiedot: hinta, valuutta, nimi
    Jos virheitä, palauttaa stringin virhe, joka käsitellään kutsuvassa
    funktiossa
    """
    try:
        raaka_data = suorita_kutsu(osake)
        raaka_hinta = re.findall(r"<span id=(.*?)</span>",
                                 str(raaka_data))

        raaka_valuutta = re.findall(r"<div>Currency in (.*?)</div>",
                                    str(raaka_data))

        raaka_nimi = re.findall(r"</script><title>(.*?):", str(raaka_data))

        indeksi = raaka_hinta[3].index(">") + 1
        strhinta = raaka_hinta[3][indeksi:]
        if strhinta.find(",") != -1:
            strhinta = strhinta.replace(",", "")
        hinta = float(strhinta)
        valuutta = raaka_valuutta[0]
        nimi = raaka_nimi[0]

    except IndexError:
        return str("virhe")
    except urllib.error.URLError:
        return str("virhe")

    return hinta, valuutta, nimi

def hae_osakkeen_hinta(osake):
    """
    Sama funktio hieman karsittuna kuin hae_osakkeen_tiedot. Hakee pelkän
    hinnan ja virhekäsittelyä ei ole.
    :param osake: Osakkeen virallinen kaupankäyntitunnus
    :return: Palauttaa osakkeen hinnan
    """
    raaka_data = suorita_kutsu(osake)
    raaka_hinta = re.findall(r"<span id=(.*?)</span>",
                             str(raaka_data))
    indeksi = raaka_hinta[3].index(">") + 1
    strhinta = raaka_hinta[3][indeksi:]
    if strhinta.find(",") != -1:
        strhinta = strhinta.replace(",", "")
    hinta = float(strhinta)
    hinta = round(hinta, 2)

    return hinta