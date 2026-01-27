import os
from lxml import etree

# Dieses Script nimmt die Reden aus dem vorläufigen Format in den TXT Dateien
# und wandelt sie in eine XML Datei um

# zur zwischenspeicherung
redenDict = {
}

# iteriert über einzelne TXT Dateien einzelner Redner*innen
def pro_person(path):
    return_me = []


    fs = open(path, "r", encoding="utf-8")  # Datei mit reden der Person öffenen
    content = fs.read().split("~")  # Datei einlesen und in einzelne Reden splitten
    content = [x for x in content if x] # liste an Reden anlegen und leere Reden skippen

    for rede in content:                # iterieren über alle reden der Person
        append_me = rede.split(".xml")  # String in Rede und Metadaten trennen
        if len(append_me) < 2 or append_me is None: # leere daten skippen
            continue
        return_me.append([append_me[0], append_me[1]])  # Metadaten und Inhalt der rede als Toupel anfügen

    fs.close()
    return return_me

# iteriert über den Ordner einer Partei
def pro_partei(path):
    return_me = []
    for rednerIn in os.listdir(path):   # über die TXT Dateien der Redner*innen iterieren
        return_me.extend(pro_person(os.path.join(path, rednerIn)))  # Reden und Metadaten aus der TXT Datei extrahieren und anfügen

    return return_me

# Iteriert über den Ordner einer Periode
def pro_periode(path):
    return_me = {}
    for partei in os.listdir(path):     # iteriert über die Ordner der Parteien
        return_me.update({partei : pro_partei(os.path.join(path, partei))}) # fügt ergebnisse der Parteien an
    return return_me


def main():
    for ordner in os.listdir("reden/analizethis"):  # Iteriert durch die Perioden Ordner
        redenDict.update({ordner : pro_periode(os.path.join("reden/analizethis", ordner))}) # Startet Verarbeitung der Periode und fügt ergebnisse an dict an

    to_xml()
    return

# nimmt das Dictionary, wandelt es in einen XML Tree um und speichert diesen
def to_xml():
    root = etree.Element("root")    # legt den Elementtree beginnend an der Wurzel an
    for key in redenDict.keys():    # iteriert über die einzelnen Wahlperioden
        temp = etree.SubElement(root, "periode" + str(key)) # legt die Periode im Tree an
        for partei in redenDict[key].keys():        # iteriert über die einzelnen Parteien der Periode
            par = etree.SubElement(temp, partei)    # legt Partei im Tree an
            for rede in redenDict[key][partei]:     # iteriert über die einzelnen Reden
                re = etree.SubElement(par, "rede", metadata=rede[0].replace("\n", "")) # fügt metadaten in Reden Tree element ein
                # print(rede)
                re.text = rede[1].replace("\n", "") # fügt Text in den Tree ein

    save_me = etree.ElementTree(root)               # holt sich den Element tree zum speichern
    save_me.write("bt_corpus.xml", pretty_print=True, encoding="UTF-8") # speichert als XML Datei
    return

main() # Main

