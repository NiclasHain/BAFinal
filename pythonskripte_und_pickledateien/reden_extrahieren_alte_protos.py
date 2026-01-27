import os
import re

# Dieses Script iteriert über alle Ordner der einzelnen Wahlperioden,welche einzelne Protokolldateien beinhalten
# und filtert die reden aus diesen heraus. Nach jeder Wahlperiode werden diese dann gespeichert
# Dieses Script funktioniert nur für Wahlperioden 1 - 18! Ab Wahlperiode 19 ändert sich die Protokollstruktur!
# Für Wahlperioden 19 bis 21 das Script "reden_extrahieren_neue_protos.py" benutzen

# Die Speicherung der Reden in diesem Script ist sehr rudimentär, aber praktisch für die händische Korrektur von Fehlern
# Die Speicherstruktur ist Ordner(Wahlperioden) -> Ordner(Parteien) -> TXT-Datei(Einzelne Redner*innen)
# Die Daten wurden später(nach der Korrektur der Relevanten Wahlperioden) mit dem Script ConvertToXML in eine XML Datei umgewandelt


# Dieses Dict tracked alle angelegten RenderIn Instanzen
tracker = {
}

# Dieses Dict dient der Zwischenspeicherung während der extraktion
# wird nach jeder rede in RenderInnen gespeichert und dann gecleared
rednerInDict = {
    "rednerIn" : "",    # Name der Redner*in
    "partei" : "",      # Partei der Redner*in (Bei fehlender Erwähnung als N_A gespeichert)
    "rede" : "",        # Text der aktiven Rede
    "getroffen" : False,    # Indicator, ob Themenrelevante Worte genannt wurden
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
        if not os.path.exists(os.path.join(pfad, re.sub(r'[^a-zA-Z0-9-ZäöüÄÖÜ]', '', self.partei))):
            os.makedirs(os.path.join(pfad, re.sub(r'[^a-zA-Z0-9-ZäöüÄÖÜ]', '', self.partei)))

        # Erstellen einer TXT Datei zur Speicherung von Reden
        f = open(os.path.join(pfad, re.sub(r'[^a-zA-Z0-9-ZäöüÄÖÜ]', '', self.partei), re.sub(r'[^a-zA-Z0-9-ZäöüÄÖÜ]', '', self.name.lower()) + ".txt"), "w", encoding="utf-8")
        # Schreiben der Reden
        for rede in self.reden:
            f.write("~~~ \n" + rede + "\n~~~")

    # printed alle Metadaten und Redeninhalte des class members
    def ausgabe(self):
        print(self.name + " " + self.partei + "\n")
        for rede in self.reden:
            print(rede + "\n\n")

# iteriert über alle Members der RednerInnen Klasse im Tracker und ruft die Speichern Funktion auf
def speichern(pfad):
    for rednerin in tracker:
        tracker[rednerin].speichern(pfad)

    # cleared die Referenzen zu den Members - löscht die Members
    tracker.clear()

# Fügt die fertige Rede an das entsprechende Member der RednerInnen Klasse an
def updaterednerinnen():

    # überprüft, ob die RednerIn im Tracker bereits vorhanden ist, fügt Rede an, falls Ja
    if rednerInDict["rednerIn"] in tracker:
        tracker[rednerInDict["rednerIn"]].redeanfuegen()

    # Wenn noch nicht im Tracker, dann wird ein neuer Member der RednerInnen Klasse erstellt und die Rede angefügt
    else:
        tracker.update({rednerInDict["rednerIn"]: RednerInnen(rednerInDict["rednerIn"], rednerInDict["partei"])})
        tracker[rednerInDict["rednerIn"]].redeanfuegen()

# Filtert nach der Mention der Partei in der Notation der Redner*in, wird als erstes ausgeführt, weil einfachstes Kriterium
def parteienfilter(gespalten, inhalt):

    parteien = ["(al)","(grüne)", "(bhe/dg)", "(bp)", "(cdu/csu)", "(cdu)", "(csu)", "(csus)", "(cvp)", "(da)", "(dfu)", "(dp)",
                "(dpb)", "(dps)",  # Alle Parteien, welche bisher im Bundestag vertreten waren
                "(drp)", "(dzp)", "(f.d.p.)", "(fdp)", "(fdv)", "(fu)", "(fvp)", "(gb/bhe)", "(gr k/o)", "(gvp)",
                "(kpd)", "(nr)", "(pds)","(pds/linke liste)" ,
                "(pds/ll)", "(spd)", "(srp)", "(ssw)", "(wav)", "(z)", "(bündnis 90/die grünen)","(bündnis 90/grüne)", "(die grünen)",
                "(die linke)", "(fraktionslos)", "(afd)"]

    # iteriert durch die Liste und überprüft auf Treffer, falls Partei gefunden, dann fast 100 Prozent eine neue Rede, oder weiterführung der bisherigen rede
    for partei in parteien:
        if partei in gespalten.lower():
            if rednerInDict["rednerIn"] == re.sub("[(].+[)]", '',
                                  gespalten):  # wenn wir schon in der rede von der person sind
                rednerInDict["rede"] += inhalt  # Inhalt an die existierende Rede anfügen
            else:  # wenn wir eine neue rede beginnen
                if rednerInDict["getroffen"]:   # Falls Konfliktakteure benannt wurden
                    updaterednerinnen()     # Wir schreiben die bisherige Rede in den entsprechenden Klassenmenmber
                    rednerInDict["getroffen"] = False   # wir setzten die Erwähnung der Konfliktparteien zurück

                rednerInDict["rednerIn"] = re.sub("[(].+[)]", '', gespalten)    # Neuer Name wird festgelegt
                rednerInDict["partei"] = partei                                             # Neue Partei festlegen
                rednerInDict["rede"] = "" + inhalt                                          # alte rede wird durch erste Zeile der neuen ersetzt
            return True
    return False

# filtert nach String, welche häufig in der Erwähnung von Redner*innen benutzt werden, wird nach dem Parteienfilter benutzt, falls keine Parteienerwähnung vorhanden ist
def hitwortfilter(gespalten, inhalt):
    hitworte = ["dr.", "präsident", "minister", "kanzler", "sekretär"]  # sehr häufige Worte für die Benennung von Redner*innen

    # wir iterieren über die Liste und filtern auf Treffer, dann sehr sicher neue Rede oder Weiterführung bisheriger Rede
    if any(wort in gespalten.lower() for wort in hitworte):

        if rednerInDict["rednerIn"] == re.sub("[(].+[)]", '',
                              gespalten):  # wenn wir schon in der rede von der person sind
            rednerInDict["rede"] += inhalt  # inhalt an existierende Rede anfügen
        else:  # wenn wir eine neue rede beginnen
            if rednerInDict["getroffen"]:   # Falls Konflikt Partei erwähnt
                updaterednerinnen()         # Wir schreiben die bisherige Rede in den entsprechenden Klassenmenmber
                rednerInDict["getroffen"] = False   # zurücksetzen der Erwähnung von Konflikt Parteien
            rednerInDict["rednerIn"] = re.sub("[(].+[)]", '', gespalten)    # neuer Name wird festgelegt
            rednerInDict["partei"] = "N_A"                                              # Partei wird auf Not Available gesetzt, weil keine Erwähnung
            rednerInDict["rede"] = "" + inhalt                                          # alte rede wird durch erste Zeile der neuen ersetzt
        return True
    return False

# Durchsucht eine Zeile auf Erwähnung einer Redner*in
def redenfinder(line):
    ausschlussworte = ["frage", "drucksache", "punkt", "beschluß", "beschluss", "kriterium", "richtlinie", "gesetz", "zeitung", "durch ", " ich ",
                       " wir ", " sie ", " nur ", " ich", "wir ", "sie ", "dazu", " eine ", " wie ",
                       " mit ", " hat ", " auch ", " gesagt", " sagte", " geführt", " haben ", " gestellt", "erklärt", "ihnen", "sage ", " hat ", "betont ", " fragt ",
                       " was ", " i ", " ii", " iii", "vor allem"]  # einfache Worte um eine Nennung von Render*innen auszuschließen, welche zu häufigen Fehlern führen

    # Zeile wird in zwei Teile gespalten
    gespalten = line.split(":")[0]          # Erwähnung der Render*in vor dem Doppelpunkt
    inhalt = "".join(line.split(":")[1:])   # Inhalt nach dem Doppelpunkt
    if len(gespalten.split(".")) > 2 or len(gespalten.split(",")) > 2:  # Ausschluss von richtigen Sätzen mit mehreren Satzzeichen
        if "(f.d.p.)" not in line.lower() and "dr." not in line.lower():    # Überprüfung der einzigen Validen Strings, die fälschlich geflagged werden
            rednerInDict["rede"] += line    # Anfügen der Zeile an bisherige Rede
            return
    if any(wort in gespalten.lower() for wort in ausschlussworte):  # überprüfung der Ausschlussworte, return, falls True
        rednerInDict["rede"] += line        # Anfügen der Zeile an bisherige Rede
        return

    if parteienfilter(gespalten, inhalt):
        return                              # Falls gefunden Return

    elif hitwortfilter(gespalten, inhalt):
        return                              # Falls gefunden Return

    else:                                   # Falls nichts gefunden
        rednerInDict["rede"] += line        # Anfügen der Zeile an bisherige Rede
        return

# setzt das Dict mit den Daten der derzeitigen Rede zurück
def resetrednerindict():
    rednerInDict["rednerIn"] = ""
    rednerInDict["partei"] = ""
    rednerInDict["rede"] = ""
    rednerInDict["getroffen"] = False
    rednerInDict["datum"] = ""

    return

# findet das Datum im Protokoll
def datumsfinder(content):
    for line in content:
        if "<DATUM>" in line:       # sucht XML Tag für Datum in der Zeile
            rednerInDict["datum"] = re.search("<DATUM>(.*)</DATUM>", line).group(1) # Filtert Datum aus Zeile
            return

# Iteriert über das komplette Protokoll und ruft andere Funktionen auf
def protokollscanner(pfad):

    fs = open(pfad, "r", encoding="utf-8")
    content = fs.readlines()

    # glossar an Worten, welche das Thema zeichnen, um herauszufinden, wenn eine Rede über das Thema spricht
    themenworte = ["israel", "palästin", "gaza", "westjordanland", "hamas", "fatah", "hisbollah", "zion",
                        "intifada", "bds", "nakba", "nahost", "nah-ost", "westbank", "west bank"]

    datumsfinder(content)
    gestartet = False   # gibt an ob die Sitzung gestartet wurde
    kommentar = False   # gibt an, ob wir uns in einem Kommentar befinden

    for line in content:
        if not gestartet:
            if "sitzung" in line.lower() and "eröffne" in line.lower() or "beginn:" in line.lower():
                gestartet = True  # Im protokoll ist der Start der Sitzung immer mit den Worten "Sitzung" und "eröffnet" markiert,
                # oder mit "Beginn:"
            else:
                continue
        # wir checken, ob wir auf einen Kommentar treffen, um diese nicht aus Versehen als redner*innen auszulesen.
        if kommentar:  # Redner*innen werden auch in Kommentaren angegeben, aber die noch nicht relevant für uns
            if ")" in line:                     # Falls kommentar wieder geschlossen wird
                kommentar = False               # Kommentar state zurücksetzen
                rednerInDict["rede"] += line    # wir filtern Kommentare erstmal raus, aber übernehmen sie. An diesem Punkt ist noch nicht klar, ob die analysiert werden
                continue
            else:
                rednerInDict["rede"] += line    # wir sind noch im kommentar und übernehmen die Zeile
                continue

        if line[0] == "(":                      # Check, ob kommentar geöffnet wird
            if ")" in line:                     # Check, ob kommentar in der gleichen Zeile wieder geschlossen wird
                rednerInDict["rede"] += line    # Zeile wird übernommen
                continue
            kommentar = True                    # Wir bleiben im Kommentar
            rednerInDict["rede"] += line        # Zeile wird übernommen
            continue

        # check ob Redner*in genannt wird
        if ":" in line:  # Redner*innen werden immer mit ":" gelistet
            redenfinder(line)                   # Zeile wird mit Funktion auf Erwähnung von Redner*in gescannt
        else:
            rednerInDict["rede"] += line        # Falls keine Erwähnung oder Kommentar, dann Zeile an Rede anfügen

        # Wenn eins der Konfliktspezifischen Worte vorkommt, dann wollen wir die Rede übernehmen
        if any(word in line.lower() for word in themenworte):
            rednerInDict["getroffen"] = True    # Falls Erwähnung gefunden wird, dann True -> Rede wird später gespeichert

    fs.close()
    resetrednerindict()     # Funktion resettet das Dict in dem die Reden zur Laufzeit zwischengespeichert werden
    return

# Main
def main():
    # Pfad zum Ordner mit den Ordnern der einzelnen Wahlperioden, welche die Protokolle beinhalten
    wahlperioden_zu_scannen = "daten_gefiltert/"

    # Pfad in dem die Reden gespeichert werden sollen
    speicherpfad = "reden/"

    # iteriert über alle Wahlperioden-Ordner und führt dann pro Protokoll den Scanner aus
    for ordner in os.listdir(wahlperioden_zu_scannen):     # Pro Wahlperiode / Ordner
        os.makedirs(speicherpfad + ordner)      # Ordner für Wahlperiode im Zielpfad anlegen

        for file in os.listdir(os.path.join(wahlperioden_zu_scannen, ordner)):     # Pro protokoll in Wahlperiode
            rednerInDict["protokollnr"] = file                          # Protkoll Nummer eintragen
            protokollscanner(os.path.join(wahlperioden_zu_scannen, ordner, file))  # Protokollscanner aufrufen

        speichern(speicherpfad + ordner)    # speicherfunktion wird aufgerufen

    return

main()

