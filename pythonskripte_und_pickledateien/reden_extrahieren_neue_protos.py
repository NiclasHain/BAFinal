import os
from bs4 import BeautifulSoup
import re

# Dieses Script iteriert über alle Ordner der einzelnen Wahlperioden,welche einzelne Protokolldateien beinhalten
# und filtert die reden aus diesen heraus. Nach jeder Wahlperiode werden diese dann gespeichert

# Die Speicherung der Reden in diesem Script ist sehr rudimentär, aber praktisch für die händische Korrektur von Fehlern
# Die Speicherstruktur ist Ordner(Wahlperioden) -> Ordner(Parteien) -> TXT-Datei(Einzelne Redner*innen)
# Die Daten wurden später(nach der Korrektur der Relevanten Wahlperioden) mit dem Script ConvertToXML in eine XML Datei umgewandelt
# An diesem Punkt war bereits bekannt, das Kommentare nicht analysiert werden, deswegen werden sie geskipped

# Die Protokolle ab der 19. Wahlperiode sind ordentlich strukturierte XML Dateien, weshalb einige Funktionen des anderen Scripts entfallen konnten

# Dieses Dict tracked alle angelegten RenderIn Instanzen
tracker = {
}

# Dieses Dict dient der Zwischenspeicherung während der extraktion
# wird nach jeder rede in RenderInnen gespeichert und dann gecleared
rednerInDict = {
    "id" : "",          # ID der Render*in im Protokoll(neu in den XML Protos), wird für den Tracker benutzt(keine Namensdopplungen)
    "rednerIn" : "",    # Name der Redner*in
    "partei" : "",      # Partei der Redner*in (Bei fehlender Erwähnung als N_A gespeichert)
    "rede" : "",        # Text der aktiven Rede
    "datum" : "",       # Datum des Protokolls, aus dem die Rede extrahiert wurde
    "protokollnr" : ""  # Nummer des Protokolls
}

# in dieser Klasse werden alle Reden plus Metadaten der Redner*innen gespeichert
class RednerInnen:
    def __init__(self, name, partei):
        self.name = name
        self.partei = partei
        self.reden = []

    # Fügt die fertige Rede an die Reden-Liste der Person an
    def redeanfuegen(self):
        self.reden.append(rednerInDict["rednerIn"] + "  "+ rednerInDict["datum"] + "  " + rednerInDict["protokollnr"] + "\n" + rednerInDict["rede"])

    # speichert die Reden in einer TXT Datei
    def speichern(self, pfad):

        # check ob der Ordner der Partei existiert, wenn nicht, dann lege an
        if not os.path.exists(os.path.join(pfad, re.sub(r'[^a-zA-Z0-9-ZäöüÄÖÜß]', '', self.partei))):
            os.makedirs(os.path.join(pfad, re.sub(r'[^a-zA-Z0-9-ZäöüÄÖÜß]', '', self.partei)))

        # Erstellen einer TXT Datei zur Speicherung von Reden
        l = open(os.path.join(pfad, re.sub(r'[^a-zA-Z0-9-ZäöüÄÖÜß]', '', self.partei), re.sub(r'[^a-zA-Z0-9-ZäöüÄÖÜß]', '', self.name.lower()) + ".txt"), "w", encoding="utf-8")
        # Schreiben der Reden
        for rede in self.reden:
            l.write("~~~ \n" + rede + "\n~~~")

    # printed alle Metadaten und Redeninhalte des class members
    def ausgabe(self):
        print(self.name + " " + self.partei + "\n")
        for rede in self.reden:
            print(rede + "\n\n")

# Fügt die fertige Rede an das entsprechende Member der RednerInnen Klasse an
def updaterednerinnen():

    # überprüft, ob die RednerIn im Tracker bereits vorhanden ist, fügt Rede an, falls Ja
    if rednerInDict["id"] in tracker:
        tracker[rednerInDict["id"]].redeanfuegen()

    # Wenn noch nicht im Tracker, dann wird ein neuer Member der RednerInnen Klasse erstellt und die Rede angefügt
    else:
        tracker.update({rednerInDict["id"]: RednerInnen(rednerInDict["rednerIn"], rednerInDict["partei"])})
        tracker[rednerInDict["id"]].redeanfuegen()

# iteriert über alle Members der RednerInnen Klasse im Tracker und ruft die Speichern Funktion auf
def speichern(pfad):
    for rednerin in tracker:
        tracker[rednerin].speichern(pfad)

    # cleared die Referenzen zu den Members - löscht die Members
    tracker.clear()

# Checkt die Rede auf Mentions der Konfliktparteien oder spezifischen Konfliktevents
def thema_check(rede):

    # glossar an Worten, welche das Thema zeichnen, um herauszufinden, wenn eine Rede über das Thema spricht.
    themenworteworte = ["israel", "palästin", "gaza", "westjordanland", "hamas", "fatah", "hisbollah", "zion",
                        "intifada", "bds", "nakba", "nahost",
                        "nah-ost"]

    # Falls Wort in Rede, dann True, ansonsten False
    if any(wort in rede for wort in themenworteworte):
        return True
    else: return False

# Erhält einen XML Eintrag mit dem Tag "rede" und filter den Text heraus
def extrahierer(eintrag):


    rede = ""   # wird returned
    unterbrechung = False   # State Indicator, ob die Rede durch einen Kommentar unterbrochen ist

    # iteriert über jede zeile im eintrag und filtert den Text nach Tag der Zeile
    for zeile in eintrag:
        if unterbrechung:   # Falls Unterbrochen, check ob unterbrechung noch aktiv
            if "</redner>" in str(zeile):
                unterbrechung = False   # Hauptredner*in sprich wieder
            else: continue

        # Kommentare werden geskipped
        if "<kommentar>" in str(zeile):
            continue

        # Falls Render*in spricht, dann anfügen
        if "</redner>" in str(zeile):
            text = re.search(r'</redner>(.*?)</p>', str(zeile)) # Text mit Regex filtern
            if text is not None:                    # Falls Textvorhanden
                text = text.group(1).split(":")     # teilweise wird noch ein "Render*in(Partei):" genannt, aber nicht immer, wir filtern es heraus
                if text[1] != "":
                    rede += "".join(text[1:])       # Text anfügen
            continue

        # Check ob andere Redner*in benannt wird (check auf Namensnennung)
        if "<name>" in str(zeile) and "</redner>" not in str(zeile):
            unterbrechung = True
            continue
        if zeile.text.rstrip() != "":   # Falls bisherige Fälle nicht eingetreten, dann nur Text anfügen
            rede += zeile.text + "\n"

    # Return Inhalt der Rede
    return rede

# iteriert über ein einzelnes Protokoll und started die extraktion pro Redeneintrag
def controller(pfad):

    #Import Protokoll
    with open(pfad, 'r', encoding="utf8") as fs:
        data = fs.read()

    # wir convertieren zu datentyp mit XML Charakteristik
    b_data = BeautifulSoup(data, "xml")
    # erstellt eine Liste mit allen Einträgen mit dem Tag "rede"
    b_reden = b_data.find_all("rede")

    # getted Protokolldatum
    rednerInDict["datum"] = b_data.find("datum").get("date")

    # iteriert über jeden Eintrag in der Liste an Reden
    for eintrag in b_reden:

        # holt sich den Text der Rede über die "extrahierer" Funktion
        rede = extrahierer(eintrag)

        # check auf Erwähnungen, falls True, dann wird Rede gespeichert
        if thema_check(rede):
            rednerInDict["id"] = eintrag.find("redner").get("id")       # ID für Tracker
            rednerInDict["rednerIn"] = eintrag.find("vorname").text + " " + eintrag.find("nachname").text   # speichern Name
            if eintrag.find("fraktion") is None:    # Falls Partei nicht gegeben, dann wollen wir Rolle
                if eintrag.find("rolle") is not None:   # Falls nur Rolle angegeben, dann speichern wir diese anstatt Partei
                    rednerInDict["partei"] = eintrag.find("rolle_kurz").text
            else:   # Wenn partei vorhanden
                rednerInDict["partei"] = eintrag.find("fraktion").text  # Partei speichern
            rednerInDict["rede"] = rede # Inhalt der Rede speichern
            updaterednerinnen()         # Rede und Metadaten im Class Member/Instanz speichern

    fs.close()

# main
def main():

    # Pfad zum Ordner mit den Ordnern der einzelnen Wahlperioden, welche die Protokolle beinhalten
    wahlperioden_zu_scannen = "code/daten_gefiltert_neue_wps/"

    # Pfad in dem die Reden gespeichert werden sollen
    speicherpfad = "reden/extrahiert/"

    # iteriert über alle Wahlperioden-Ordner und führt dann pro Protokoll das Script aus
    for ordner in os.listdir(wahlperioden_zu_scannen):  # Pro Wahlperiode / Ordner
        os.makedirs(speicherpfad + ordner)  # Ordner für Wahlperiode im Zielpfad anlegen

        for file in os.listdir(os.path.join(wahlperioden_zu_scannen, ordner)):  # Pro protokoll in Wahlperiode
            rednerInDict["protokollnr"] = file  # Protkoll Nummer eintragen
            controller(os.path.join(wahlperioden_zu_scannen, ordner, file))  # Protokollscanner aufrufen

        speichern(speicherpfad + ordner)  # speicherfunktion wird aufgerufen
    return


main()