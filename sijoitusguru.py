import osakkeenhaku
import osakkeengrafiikka
from tkinter import *
from tkinter import messagebox


class Osakeikkuna:
    """
    Sisältää kuvaajan ja informaation sisältävän luokan kutsun ja sulkunapin
    Hoitaa myös virhetilanteet mikäli osaketta ei löydy tai internet-yhteys ei
    toimi.
    """
    def __init__(self, pääikkuna, osakkeen_nimi):
        """
        Luokan rakentaja
        :param pääikkuna: Parent-ikkuna
        :param osakkeen_nimi: Osakkeen lyhenne, jolla tieto haetaan netistä
        """
        self.__pääikkuna = pääikkuna
        try:
            hinta, valuutta, nimi = osakkeenhaku.hae_osakkeen_tiedot(osakkeen_nimi)
            self.__pääikkuna.title(nimi)
            kuvaaja = osakkeengrafiikka.Graafinen(self.__pääikkuna, hinta, valuutta, nimi,
                                osakkeen_nimi)
            Button(self.__pääikkuna, text="Lopeta osakkeen seuranta",
                   command=self.lopeta).pack()
        except ValueError:
            self.anna_virheilmoitus()
        except TclError:
            self.anna_virheilmoitus()

    def anna_virheilmoitus(self):
        """
        Antaa hienon virheilmoituksen laatikossa
        :return: ei palauta mitään
        """
        messagebox.showerror("Virhe datan lukemisessa",
                             "Osakkeen tietojen hakeminen epäonnistui. Oletko "
                             "varma, että osakkeen nimi on kirjoitettu oikein?"
                             " Huom. sinun tulee käyttää osakkeen virallista "
                             "kaupankäyntitunnusta esim. Outokumpu = OUT1V. "
                             "Varmista myös, että käytössäsi on toimiva "
                             "internet-yhteys.")
        self.__pääikkuna.destroy()

    def lopeta(self):
        """
        Sulkee ikkunan
        :return: Ei palauta mitään
        """
        self.__pääikkuna.destroy()


class Sijoitusguru:
    """
    Pääikkuna, josta voidaan hakea eri osakkeita. Huom. useita osakkeita voi
    tarkkailla samaan aikaan.
    """
    def __init__(self):
        """
        Luokan rakentaja
        """
        # Luodaan ikkuna, vaihdetaan iconia ja titleä
        self.__pääikkuna = Tk()
        self.__pääikkuna.title("Donald Trump was here")
        # Luodaan labelit, jossa lukee tarvittava tieto
        Label(self.__pääikkuna,
              text="Tervetuloa sijoitusguruun!", font=("Helvetica", 25)).pack(
            fill=BOTH, expand=1)
        Label(self.__pääikkuna, text="Sijoitusgurun avulla voit "
              "seurata minkä tahansa osakkeen reaaliaikaisia "
              "pörssikursseja.\nSijoitusguru käyttää tietolähteenänsä "
              "Googlen Finance-palvelua. Ohjelman käyttö vaatii siis "
              "toimivan internet-yhteyden.\n\n\nSyötä alla olevaan kenttään "
              "haluamasi osakkeen virallinen kaupankäyntitunnus.\n",
              font=("Helvetica", 15)).pack(fill=BOTH, expand=1)

        self.__osake = Entry(self.__pääikkuna)
        self.__osake.pack(expand=1)

        Button(self.__pääikkuna, text="Aloita osakkeen tarkastelu",
               command=self.osakkeen_tarkastelu).pack(expand=1)

        Button(self.__pääikkuna, text="Lopeta rikastuminen",
               command=self.lopeta).pack(expand=1)

        # Laitetaan enter toimimaan osakkeiden haku käskynä
        self.__pääikkuna.bind("<Return>", self.osakkeen_tarkastelu)

    def osakkeen_tarkastelu(self, event=None):
        """
        Avaa uuden ikkunan osakkeen tarkastelua varten
        :param event: Tämä on pakko olla, jotta tämä metodi pystyttiin bindata
        enteriin
        :return: Ei palauta mitään
        """
        self.__uusi_ikkuna = Toplevel(self.__pääikkuna)
        self.__uusi_ikkuna.geometry("800x800")
        self.__avaus = Osakeikkuna(self.__uusi_ikkuna, self.__osake.get())

    def käynnistä(self):
        """
        Käynnistää ohjelman
        """
        self.__pääikkuna.mainloop()

    def lopeta(self):
        """
        Sulkee ohjelman.
        """
        self.__pääikkuna.destroy()


def main():
    """
    Käynnistää graafisen käyttöliittymän
    """
    sijoitusguru = Sijoitusguru()
    sijoitusguru.käynnistä()


main()
