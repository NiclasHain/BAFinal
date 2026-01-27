import os

# Dieses Script filtert die Kommentare aus den Dateien mit den Reden

# iteriert über alle Parteien der Wahlperiode und ruft die Filter Funktion auf
def iterierer(pfad, speicherpfad):
    print(pfad)

    #iteriert über alle parteien der Wahlperiode
    for partei in os.listdir(pfad):
        # erstellt ordner im neuen speicherpunkt, falls nicht vorhanden
        if not os.path.exists(os.path.join(speicherpfad, partei)):
            os.makedirs(os.path.join(speicherpfad, partei))

        # iteriert über alle TXT Dateien mit den Reden
        for datei in os.listdir(os.path.join(pfad, partei)):
            filtern(os.path.join(pfad, partei, datei), os.path.join(speicherpfad, partei, datei))

# filtert die Kommentare
def filtern(path, speicherpfad):

    # öffnet die TXT Dateien der einzelnen Redner*innen mit den Reden
    fs = open(path, "r", encoding="utf-8")
    data = fs.readlines()

    # öffnet den writer für die fertigen Dateien
    l = open(speicherpfad, "w", encoding="utf-8")

    # gibt den state an (sind wir im kommentar oder nicht?)
    kommentar = False

    # iteriert über alle zeilen der TXT Datei
    for line in data:

        # eröffnung wird geskipped
        if "Bundestag" in line and "Wahlperiode" in line and "Sitzung" in line:
            print(line)
            continue

        # falls Kommentar state, dann skip
        if kommentar:

            #  check ob kommentar wieder geschlossen
            if ")" in line:
                kommentar = False
                continue

            # check ob kommentar geöffnet
        if line[0] == "(":
            kommentar = True

            # check ob kommentar in der gleichen Zeile wieder geschlossen
            if line[-1] == ")":
                kommentar = False
                continue
            else:
                continue

        # schreibt alle Zeilen, welche keinen Kommentar enthalten
        l.write(line)

    fs.close()
    l.close()

def main():

    # pfad der Dateien mit Reden
    pfad = "reden/analizethis"

    # iteriert über alle Wahlperioden
    for ordner in os.listdir(pfad):
        print(ordner)

        # ruft funktion auf die über alle dateien iteriert und im Pfad(zweite Variable) speichert
        iterierer(os.path.join("reden/analizethis", ordner), os.path.join("reden/temp", ordner))

    return



main()