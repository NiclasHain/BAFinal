
import nltk
import re
import pickle

import unicodedata
from lxml import etree

# Dieses Script nimmt die Reden aus der XML Datei und erzeugt ein dict mit den Reden der Parteien, geteilt in einzelne Sätze
# sortiert nach Periode und Partei

# Dieses Dict wird gefüllt mit Dicts, welche die Dicts der einzelnen Parteien in der Periode beinhalten, welche eine Liste an sätzen enthalten
sentences_per_periode = {}

# Diese Funktion nimmt einen Input String und gibt eine Liste an Sätzen wieder
def pre_processor(process_me):
    process_me = unicodedata.normalize("NFKD", process_me)  # Normalisierung für die Umlaute
    sentences = nltk.sent_tokenize(re.sub(r'([a-z])\.([A-Z])', r'\1. \2', re.sub(r'([a-z])!([A-Z])', r'\1! \2', process_me)))  # wir holen uns die sätze und fügen ein leerzeichen an Punkte an, welche direkt von einem Großbuchstaben gefolgt werden
    print(sentences)

    return  sentences

# Funktion um den XML Tree in schöner Form zu printen
def prettyprint(element, **kwargs):
    xml = etree.tostring(element, encoding="UTF-8", pretty_print=True, **kwargs)    #String erstellen
    print(xml.decode(), end='') # printing

def main():
    tree = etree.parse("xml_tests/bt_corpus.xml")   # Wir importieren den XML Tree
    root = tree.getroot()                           # Wir sourcen die Root um davon aus zu iterieren

    for periode in root:                            # Iteration über alle Perioden
        sentences_per_periode.update({periode.tag : {}})    # Leere Dicts in die Perioden einfügen
        print(periode.tag)
        for partei in periode:                      # Iteration über alle Parteien in der Periode
            sentences_per_periode[periode.tag].update({partei.tag : []})    # Parteien Dictionaries anlegen
            print(partei.tag)
            for rede in partei:                     # Iteration über alle reden der Partei
                sentences_per_periode[periode.tag][partei.tag].extend(pre_processor(rede.text)) # Pre_processing aufrufen und Liste erweitern



main()

# Speichern als Pickle
with open('sentences.pickle', 'wb') as output:
   pickle.dump(sentences_per_periode, output, pickle.HIGHEST_PROTOCOL)
