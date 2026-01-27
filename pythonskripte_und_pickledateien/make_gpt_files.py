import os
import pickle
import re
# Dieses Skript macht die einzelnen Dateien, welche die Sätze einer Partei in einer Wahlperiode beinhalten.
# Diese werden dann als Input für die Analyse mit ChatGPT benutzt

# speichert die Sätze einer Partei in einer WP als TXT Datei
def speichern(saetze, periode, partei):

    # legt TXT Datei an
    f = open(periode + "/" + partei + ".txt", "w", encoding="utf-8")

    # schreibt alle Sätze
    for saetz in saetze:
        print(saetz + "\n")
        f.write(saetz + "\n")



    return


def main():

    with open("sentences.pickle", "rb") as input:
        data = pickle.load(input)

    # Wir rufen pro Periode alle Sätze der Parteien auf und speichern sie in einzelnen Dateien
    for periode in data:

        per = "".join(re.findall(r'\d+', periode))
        for partei in data[periode]:
            speichern(data[periode][partei], per, partei)


main()

