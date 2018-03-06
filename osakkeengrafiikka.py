from tkinter import *
import osakkeenhaku


class Graafinen(Frame):
    """
    Tämä luokka hoitaa kaiken informaation piirtämisen osakeikkunaan. Tässä
    hyödynnetään paljon Tkinterin canvas toimintoa.
    """
    def __init__(self, parent, hinta, valuutta, nimi, osakkeen_lyhenne):
        Frame.__init__(self, parent)

        self.__ikkuna = parent
        self.__valuutta = valuutta
        self.__nimi = nimi
        self.__hinta = hinta
        self.__alkuhinta = hinta
        self.__osakkeen_lyhenne = osakkeen_lyhenne
        self.__hintahistoria = [hinta]

        self.__canvas = Canvas(self)

        self.__pysyva_grafiikka = []
        self.__hinta_prosentti_grafiikka = []
        self.__kuvaaja_grafiikka = []
        self.__y_akselin_grafiikka = []

        self.alustaUI()

    def alustaUI(self):
        """
        Tässä metodissa luodaan varsinainen kuvaaja ja päivitetään sitä
        :return: Ei palauta mitään
        """
        self.pack(fill=BOTH, expand=1)
        # Luodaan y-akselin asteikko
        self.luo_hinta_axis()

        # Tämän hetken kurssi -teksti
        self.__pysyva_grafiikka.append(self.__canvas.create_text(50, 600, anchor=W,
                                  text="Tämän hetkinen kurssi:"))

        self.__hinta_prosentti_grafiikka.append(self.__canvas.create_text(60, 650, anchor=W, text="{:.2f} {:s}"
                                  .format(self.__hinta, self.__valuutta),
                                  font=("Helvetica", 25)))

        # Otsikoidaan ikkuna
        self.__pysyva_grafiikka.append(self.__canvas.create_text(400, 25, text=self.__nimi,
                                  font=("Helvetica", 30)))

        # Laitetaan y-akselin yksikkö näkyviin
        self.__pysyva_grafiikka.append(self.__canvas.create_text(5, 40, anchor=W, text=self.__valuutta))

        # Luodaan y-akseli
        self.__pysyva_grafiikka.append(self.__canvas.create_line(40, 60, 40, 540))

        # Luodaan x-akseli
        self.__pysyva_grafiikka.append(self.__canvas.create_line(40, 540, 540, 540))

        # Luodaan koordinaatiston "pikkuviivat"
        for i in range(60, 540, 20):
            self.__pysyva_grafiikka.append(self.__canvas.create_line(37, i, 43, i))
            self.__pysyva_grafiikka.append(self.__canvas.create_line(i, 537, i, 543))

        # Luodaan x-akselin asteikko
        aika = 0
        for i in range(40, 540, 120):
            self.__pysyva_grafiikka.append(self.__canvas.create_text(i, 555, text=aika))
            aika += 15

        # Laitetaan x-akselin yksikkö näkyviin
        self.__pysyva_grafiikka.append(self.__canvas.create_text(560, 540, text="Viim.\n 60 min"))

        #  Laitetaan y-akselin asteikko paikalleen
        a = 0
        for i in range(521, 80, -40):
            self.__y_akselin_grafiikka.append(self.__canvas.create_text(5, i, anchor=W,
                                      text="{:.2f}"
                                      .format(self.__hintaaxis_arvot[a])))
            a += 1
        # Luodaan muutosprosentin kertova teksti
        self.__pysyva_grafiikka.append(self.__canvas.create_text(500, 600,
                                  text="Muutos prosentteina tarkastelun "
                                       "aloituksesta lähtien:"))

        self.__hinta_prosentti_grafiikka.append(self.__canvas.create_text(500, 650, text="0.00%",
                                  font=("Helvetica", 25)))

        # Laitetaan koordinaatisto näkyviin
        self.__canvas.pack(fill=BOTH, expand=1)

        # Luodaan reaaliaikainen kuvaajan piirto. Tässä hyödynnetään viiveellä
        # varustettua loputonta looppia, joka on toteutettu after-metodilla.
        # Huomaa kuinka sitä kutsutaan uudestaan self.päivitä metodin sisällä!

        self.__ikkuna.after(9950, self.päivitä)

    def luo_hinta_axis(self):
        """
        Luodaan hinta-asteikko käyttäen hyväksi suurinta ja pienintä hintaa
        tarkastelujaksolta
        :return: ei palauta mitään vaan päivittää y-akselilla näytettävät hintatiedot
        """
        hintaaxis_alku = min(self.__hintahistoria) - 0.10
        if hintaaxis_alku < 0:
            hintaaxis_alku = 0
        hintaaxis_loppu = max(self.__hintahistoria) + 0.10
        hintaaxis_koko = round(hintaaxis_loppu - hintaaxis_alku, 2)
        hintaaxis_arvot = []
        i = 0
        while i < 12:
            hintaaxis_arvot.append(hintaaxis_alku)
            hintaaxis_alku = round(hintaaxis_alku + hintaaxis_koko / 12, 2)
            i += 1
        self.__hintaaxis_arvot = hintaaxis_arvot

    def päivitä(self):
        """
        Tämä metodi hoitaa kuvaajan ja muun informaation päivittämisen 10s
        välein.
        :return:
        """
        # Haetaan netistä uusi hinta
        uusi_hinta = osakkeenhaku.hae_osakkeen_hinta(self.__osakkeen_lyhenne)
        self.__hintahistoria.append(uusi_hinta)
        # Lasketaan muutos prosentteina ja muokataan tekstiä sen mukaan
        prosentti = laske_muutos_prosentteina(self.__alkuhinta, uusi_hinta)
        if prosentti > 0:
            self.__canvas.itemconfig(self.__hinta_prosentti_grafiikka[1], text="+{:.2f}%".format(prosentti),
                                     fill="green")
        elif prosentti == 0:
            self.__canvas.itemconfig(self.__hinta_prosentti_grafiikka[1], text="{:.2f}%".format(prosentti),
                                     fill="black")
        else:
            self.__canvas.itemconfig(self.__hinta_prosentti_grafiikka[1], text="{:.2f}%".format(prosentti),
                                     fill="red")

        # Koska kuvaajan x-akseli on vain 60min pitkä, niin poistamme
        # piirrettyjä viivoja ja siirrämme jäljelle jääviä.

        if len(self.__hintahistoria) > 360:
            del self.__hintahistoria[0]
            self.__canvas.delete(self.__kuvaaja_grafiikka[0])
            for i in range(359):
                self.__canvas.move(self.__kuvaaja_grafiikka[i], -50/36, 0)

        # Mikäli kuvaajan skaala ylittyy niin se korjataan.

        if (uusi_hinta < self.__hintaaxis_arvot[0]) or (
                    uusi_hinta > self.__hintaaxis_arvot[11]):
            self.automaattiskaalaus(uusi_hinta)
        else:
            # Piirretään uusi viiva kuvaajaan. X-akselin pituus on 500px ja
            # tunnissa päivityksiä tehdään 360. Siitä tulee 50/36.
            kertaluku = len(self.__hintahistoria)
            vanha_y, uusi_y = self.laske_y_koord(self.__hinta, uusi_hinta)
            self.__kuvaaja_grafiikka.append(self.__canvas.create_line((40 + (kertaluku - 2) * (50 / 36)),
                                      vanha_y, (40 + (kertaluku - 1) * (50 / 36)),
                                      uusi_y, fill="red", activefill="blue"))
            self.__hinta = uusi_hinta
            self.__canvas.itemconfig(self.__hinta_prosentti_grafiikka[0], text="{:.2f} {:s}"
                                     .format(self.__hinta, self.__valuutta))
        # Loputon looppi
        self.__ikkuna.after(9950, self.päivitä)

    def laske_y_koord(self, vanha_hinta, uusi_hinta):
        """
        Laskee hintoja vastaavat y-koordinaatit kuvaajan piirtoa varten
        :param vanha_hinta: Edellinen hinta suoran alkupistettä varten
        :param uusi_hinta: Uusi hinta suoran loppupistettä varten
        :return: Palauttaa y-koordinaatit
        """
        yksiperpix = (self.__hintaaxis_arvot[11] -
                      self.__hintaaxis_arvot[0]) / 440
        vanha_y_koord = 520 - ((vanha_hinta -
                                self.__hintaaxis_arvot[0]) / yksiperpix)
        uusi_y_koord = 520 - ((uusi_hinta -
                               self.__hintaaxis_arvot[0]) / yksiperpix)
        return round(vanha_y_koord, 0), round(uusi_y_koord, 0)

    def automaattiskaalaus(self, uusi_hinta):
        """
        Skaalataan kuvaajaa automaattisesti
        :return: ei palauta mitään.
        """
        for i in self.__kuvaaja_grafiikka:
            self.__canvas.delete(i)

        for i in self.__y_akselin_grafiikka:
            self.__canvas.delete(i)

        # Luodaan y-akselin asteikko
        self.luo_hinta_axis()

        # Tämän hetken kurssi
        self.__canvas.itemconfig(self.__hinta_prosentti_grafiikka[0], text="{:.2f} {:s}"
                                 .format(self.__hinta, self.__valuutta))

        #  Laitetaan y-akselin asteikko paikalleen
        a = 0
        for i in range(521, 80, -40):
            self.__y_akselin_grafiikka.append(self.__canvas.create_text(5, i, anchor=W,
                                             text="{:.2f}".format(self.__hintaaxis_arvot[a])))
            a += 1

        # Piirretään kaikki viivat uudestaan uudessa skaalassa
        for i in range(2, len(self.__hintahistoria) + 1):
            kertaluku = i
            vanha_y, uusi_y = self.laske_y_koord(self.__hintahistoria[i-2],
                                                 self.__hintahistoria[i - 1])
            self.__kuvaaja_grafiikka.append(self.__canvas.create_line((40 + (kertaluku - 2) * (50 / 36)),
                                      vanha_y, (40 + (kertaluku - 1) * (50 / 36)), uusi_y,
                                      fill="red", activefill="blue"))
        self.__hinta = uusi_hinta
        self.__canvas.itemconfig(self.__hinta_prosentti_grafiikka[0], text="{:.2f} {:s}"
                                 .format(self.__hinta, self.__valuutta))


def laske_muutos_prosentteina(alkuhinta, hinta_nyt):
    """
    Laskee muutoksen prosentteina ja lisää etumerkin tarvittaessa
    :param alkuhinta: Alkuperäinen hinta
    :param hinta_nyt: Muuttunut hinta
    :return: Muutosprosentti
    """
    prosentti = abs(alkuhinta - hinta_nyt) / alkuhinta * 100
    if alkuhinta - hinta_nyt > 0:
        return -1 * prosentti
    else:
        return prosentti
